# coding: utf8
'''
Created on Apr 14, 2013

@author: root
'''

from ftplib import * 
import re , os, sys
import time
import subprocess

retry_times = 100
sleep_value = 5
sock_timeout = 60

def curl_file(rfile, lfile):
#     "--max-time", "300",
#     cmds = ["curl", rfile, "-o", lfile, "--connect-timeout", "300", "-C", "-", "--retry", "3"]
    cmds = ["wget", "-t", "10", "-T", "60", "-O", lfile, rfile ]
    print cmds
    proc = subprocess.Popen(cmds, close_fds=True, preexec_fn=os.setsid)
    proc.wait()

# def remove_trail(path):
#     return "/" + "/".join([ p for p in path.split("/") if len(p) > 0 ])

def parse_linux_file(line):
    fr = re.findall(r"^([dl-]([r-][w-][x-]){3}) +(\d*) +(\S+) +(\S+) +(\d+) +([\S ]{12}) +([\S ]+)$", line)
    print fr
    if len(fr) == 1:
        return { "attr": fr[0][0], "nlink": fr[0][2], "user": fr[0][3], "group": fr[0][4], "size": long(fr[0][5]), "date": fr[0][6], "name":fr[0][7].split("->")[0].strip()}
    return None

class term_progress():
    def __init__(self):
        self.prev_pct = -1
    def progress(self, pct):
        pct = int(pct)
        if pct > 100: pct = 100
        if pct < 0 : pct = 0
        cpct = self.prev_pct
        while cpct < pct:
            cpct += 1
            if cpct % 5 == 0:
                sys.stdout.write(str(cpct))
            else:
                sys.stdout.write(".")
            sys.stdout.flush()
        if self.prev_pct < pct: self.prev_pct = pct

# class watch_dog(threading.Thread):
#     def __init__(self, data_conn, total_size):
#         threading.Thread.__init__(self);
#         self.terminated = False
#         self.total_size = total_size
#         self.curr_size = 0
#         self.data_conn = data_conn
#         self.locker = threading.RLock()
#         self.is_first = True
#
#     def terminate(self):
#         self.locker.acquire()
#         try:
#             self.terminated = True
#             self.data_conn = None
#         finally:
#             self.locker.release()
#         print ""
#
#     def notify(self, size):
#         self.locker.acquire()
#         try:
#             self.curr_size = size
#             self.last_tm = time.time()
#         finally:
#             self.locker.release()
#
#     def run(self):
#         start_tm = time.time()
#         curr_tm = time.time()
#         self.last_tm = time.time()
#         while True:
#             time.sleep(0.2)
#             self.locker.acquire()
#             try:
#                 if self.terminated : break
#                 dtv = time.time() - self.last_tm
#                 if dtv > (sock_timeout) :
#                     print "read timeout ..."
#                     if self.data_conn is not None:
#                         self.data_conn.close()
#                         break
#                 dtv = time.time() - curr_tm
#                 if dtv > 1:
#                     if self.is_first :
#                         print ""
#                         self.is_first = False
#                     tm = time.time() - start_tm
#                     if self.total_size > 0:
#                         pct = float(int((self.curr_size * 10000.0) / self.total_size)) / 100.0
#                         spd = "NA"
#                         if tm > 0:
#                             spd = str(self.curr_size / tm) + " bytes/S"
#                         s = "\r" + str(pct) + "%\t" + spd + "\t"
#                     else:
#                         s = "\r" + str(self.curr_size) + " bytes\t"
#                     sys.stderr.write(s)
#                     curr_tm = time.time()
#             finally:
#                 self.locker.release()

class my_ftp:
    def __init__(self, host):
        self.connected = False
        self.file_lines = []

#         self.lprinter = term_progress()

        self.file_handle = None
        self.file_writed = 0
        self.file_size = -1
        self.local_size = -1

        self.host = host
        self.ftp_conn = FTP()
        self.ftp_conn.set_debuglevel(1)
        self.try_conn()

    def _store_ftp_file(self, data, lfile):
        
        if self.file_handle is None:
            to_resume = False
            if self.file_size > 0 and self.local_size > 0 and self.local_size < self.file_size:
                to_resume = True

            if to_resume :
                print "resume downloading at:", self.local_size
                self.file_writed = self.local_size
                self.file_handle = open(lfile, "ab")
#                 self.file_handle.seek(0, os.SEEK_END)
            else:
                print "resume downloading at:", 0
                self.file_handle = open(lfile, "wb")
                self.file_writed = 0
                
        self.file_writed += len(data)
        self.file_handle.write(data) 
        
        pct = float(self.file_writed) / self.file_size * 100
        
        sys.stdout.write("\r%d / %d / %s" % (self.file_writed, self.file_size, pct))
        
        return self.file_writed

    def retr_file(self, rfile, lfile):
        if self.file_handle  is not None:
            self.file_handle.close()
            self.file_handle = None

        if not self.connected: 
            self.try_conn()
            
        if not self.connected: 
            return None
 
        self.ftp_conn.voidcmd("TYPE I")
        self.file_size = self.ftp_conn.size(rfile) 
        
        if self.file_size == 0 :
            return None 

        self.local_size = 0
        if os.path.exists(lfile):
            self.local_size = os.stat(lfile).st_size
 
        cmd = 'RETR ' + rfile 
        conn = self.ftp_conn.transfercmd(cmd, self.local_size)

        while True:
            data = conn.recv(1024 * 16)
            if not data: break
            self._store_ftp_file(data, lfile)
 
        conn.close()
        try:
            self.ftp_conn.voidresp()
        except Exception, e:
            print e  # 451 error if checksum error 
            
        if os.path.exists(lfile):
            self.local_size = os.stat(lfile).st_size
            return self.local_size, self.file_size
        return None

    def close(self):
        self.ftp_conn.close() 

    def _store_ftp_file_lines(self, line):
        self.file_lines.append(line)
        print line

    def _parse_ftp_files(self,):
        files = []
        for line in self.file_lines:
            fo = parse_linux_file(line)
            if fo is not None : files.append (fo)
        return files

    def try_list_files(self, path="/"):
        
        def __inner_do():
            if not self.connected:
                self.try_conn()

            if not self.connected:
                return None 

            try:
                self.ftp_conn.cwd(path)
                self.file_lines = [] 
                self.ftp_conn.dir(self._store_ftp_file_lines)
                return self._parse_ftp_files()
            except Exception, e:
                print e
            return None

        for i in range(5):
            print "try dir", i
            ret = __inner_do()
            if ret is not None:
                return ret

    def try_nlst_files(self, path="/"):
        
        if not self.connected: 
            self.try_conn()
            
        if not self.connected: 
            return None

        try:
            self.ftp_conn.cwd(path) 
            return self.ftp_conn.nlst()
        except Exception, e:
            print e
        return None

    def try_conn(self):
        for i in range(retry_times):
            print(i, "connecting ...", self.host)
            try:
                self.ftp_conn.connect(host=self.host, port=21, timeout=sock_timeout)
                self.ftp_conn.login()

                dump = self.ftp_conn.pwd()
                if len(dump) > 0:
                    self.connected = True
                    return True
            except:
                pass
            
            time.sleep(sleep_value)
        return False

class ladsweb_ftp(my_ftp):
    def __init__(self):
        my_ftp.__init__(self, "ladsweb.nascom.nasa.gov")

    def __del__(self):
        my_ftp.close(self)


class e4ftl01_ftp(my_ftp):
    def __init__(self):
        my_ftp.__init__(self, "e4ftl01.cr.usgs.gov")

    def __del__(self):
        my_ftp.close(self)
        
if __name__ == '__main__':
    lftp = ladsweb_ftp() 
    
    print lftp.try_nlst_files("/allData/6/MOD04_L2/2014/5/MOD03/2009/001")
    
#     lftp.retr_file("/allData/5/MOD03/2009/001/MOD03.A2009001.0000.005.2010257192006.hdf" , "/tmp/MOD03.A2009001.0000.005.2010257192006.hdf")
    
#     res = '''
# total 361572
# drwxr-xr-x      2 90   4096 Jun 20  2012 MOLA
# dr--------      2 90   4096 Nov 19 11:51 MOLT
# drwxr-xr-x      2 90   4096 Jun 20  2012 MOTA
# drwxr-xr-x 3 root root 4096 May 20 17:42 pub 01
# lrwxrwxrwx 1 root root   21 May 21 09:16 test -> /root/anaconda-ks.cfg
# -rwxr-xr-x 1 root root 1574 May 20 17:42 test.py
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2002
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2003
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2004
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2005
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2006
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2007
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2008
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2009
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2010
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2011
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2012
# dr-xr-xr-x   1 ftpuser  ftpusers  1 May 21 03:17 2013
# '''
#
#     eftp = e4ftl01_ftp()
#     for line in res.split("\n"):
#         print parse_linux_file(line)

#     eftp = e4ftl01_ftp()
#     print   eftp.try_list_files("/MOLT/MOD11B1.005/2013.03.26/")

#     rfile = "/MOLT/MOD11C1.005/2009.11.08/MOD11C1.A2009312.005.2009314121440.hdf"
#     lfile = "/tmp/MOD11C1.A2009312.005.2009314121440.hdf"



#     fst = os.stat(lfile)[6]

#     print fst

#     eftp.retr_file(rfile, lfile)

#     cpt = term_progress()
#     cpt.progress(0.009)
#     cpt.progress(0.094)
#     cpt.progress(1.145)
#     cpt.progress(1.155)
#     cpt.progress(2)
#     cpt.progress(3)
#     cpt.progress(100)

    pass


