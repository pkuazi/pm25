#! /usr/bin/env python
# coding: utf-8
import gdal
import psycopg2
import ogr, os, osr
import sys
import numpy as np
import json

provinceid = [11,12,13,14,15,21,22,23,31,32,33,34,35,36,37,41,42,43,44,45,46,50,51,52,53,54,61,62,63,64,65,71,81,82]
#provinceid = [46]
shpfolder = "/mnt/mfs/zjh/rspm25/shpdata/province_bianjie"

rstfolder = '/mnt/mfs/zjh/rspm25/PM25_CIESIN/pm25_6grades/china'
t_series = ['199801_200012', '199901_200112','200001_200212','200101_200312','200201_200412','200301_200512','200401_200612', '200501_200712','200601_200812', '200701_200912', '200801_201012','200901_201112', '201001_201212']
t_num = len(t_series)

dstfolder = "/mnt/mfs/zjh/rspm25/PM25_CIESIN/province_stats"

classid = [1,2,3,4,5,6]


def prshname(pid):
    conn = psycopg2.connect(host="10.0.138.20", user="postgres", password="", database="gscloud_metadata")
    cur = conn.cursor()
    # sql0 = "select prshname, ST_AsText(the_geom),st_xmin(the_geom), st_ymin(the_geom), st_xmax(the_geom),st_ymax(the_geom) from shp_cn_province where provinceid =  %s" % pid
    sql = "select prshname from shp_cn_province where provinceid =  %s" % pid
    cur.execute(sql)
    (prshname,) = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return prshname

def clip(shp,rst,dst_file):
    shp = os.path.join(shpfolder,shp)
    rst = os.path.join(rstfolder, rst)

    shpdata = ogr.Open(shp)
    shplayer = shpdata.GetLayer(0)
    xmin, xmax, ymin, ymax = shplayer.GetExtent()

    # clip
    dstfile = os.path.join(dstfolder, dst_file)
    cmd = 'gdalwarp -co "COMPRESS=deflate" -co "TILED=YES" -co "BIGTIFF=IF_NEEDED"  -of GTiff -dstnodata none -cutline %s -te %s %s %s %s %s %s' % (
        shp, xmin, ymin, xmax, ymax, rst, dstfile)
    print cmd
    os.system(cmd)

    cmd = "gdaladdo -r nearest -ro --config COMPRESS_OVERVIEW DEFLATE %s 8 16 32" % (dstfile,)
    print cmd
    os.system(cmd)

    return dstfile

def rststats(pid,time,rasterfile):
    dataset = gdal.OpenShared(rasterfile)

    if dataset is None:
        print("Failed to open file: " + rasterfile)
        sys.exit(1)

    band = dataset.GetRasterBand(1)
    xsize = dataset.RasterXSize
    ysize = dataset.RasterYSize
    print "Output file %s size:" % rasterfile, xsize, ysize

    rastervalue = band.ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize)

    count1 = np.sum(rastervalue == 1)
    count2 = np.sum(rastervalue == 2)
    count3 = np.sum(rastervalue == 3)
    count4 = np.sum(rastervalue == 4)
    count5 = np.sum(rastervalue == 5)
    count6 = np.sum(rastervalue == 6)


    data = {}
    data["pid"] = pid
    data["time"] = time
    data["class1"] = count1
    data["class2"] = count2
    data["class3"] = count3
    data["class4"] = count4
    data["class5"] = count5
    data["class6"] = count6


    stats_str = json.dumps(data)
    return stats_str

if __name__ == '__main__':
    f = open("/mnt/mfs/zjh/rspm25/PM25_CIESIN/stats/stats_province1.txt", 'w+')

    raw_files = os.listdir(rstfolder)
    for i in range(t_num):
        for file in raw_files:
            if t_series[i] in file:
                for rid in provinceid:
                    shp = str(rid)+'.shp'
                    rst = file
                    dst_file = str(rid)+ "_" + t_series[i] + ".tif"
                    dstfile = clip(shp,rst,dst_file)

                    stats= rststats(rid, t_series[i], dstfile)
                    print >> f, stats

    f.close()





