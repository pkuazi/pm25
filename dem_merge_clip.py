# -*- coding: utf-8 -*-
import subprocess,os
import ogr
import shutil
import zipfile, re,uuid
# merge and clip dem of jingjinji
#for jjj
#dataids = ['srtm_59_04', 'srtm_59_05', 'srtm_60_04', 'srtm_60_05']
#for pingyuan: shannxi, shanxi, henan, jjj
#dataids = ['srtm_58_05','srtm_58_06','srtm_59_06','srtm_60_06','srtm_59_04', 'srtm_59_05', 'srtm_60_04', 'srtm_60_05']
dem_dir = "/mnt/gscloud/DEM/srtm90/TIFF"
dst_dir ='/mnt/mfs/zjh/rspm25/dem'
shpfolder = "/mnt/mfs/zjh/rspm25/shpdata"
DEM_ROOT_DIR = "/mnt/gscloud/DEM"

# merge and clip dem of China
row = ['51','52','53','54','55','56','57','58','59','60','61','62','63']
col = ['02','03','04','05','06','07','08','09']


def extract_gdtm_files(files):
    '''
    dataid.zip --> dataid/
                    /dataid_dem.tif
                    /dataid_num.tif
    '''
    POSTFIX_PTN = r".*(?=.zip)"

    gdtm_files = []
    for path in files:
        zip_filename = os.path.basename(path)
        tmp = re.match(POSTFIX_PTN, zip_filename)
        dataid = tmp.group()

        filedir = os.path.join(dst_dir, "GDTM", dataid)
        if not os.path.exists(filedir):
            tmp_dir = os.path.join(filedir, str(uuid.uuid4()))
            try:
                os.makedirs(tmp_dir)
            except OSError:
                pass
            z = zipfile.ZipFile(path)
            z.extractall(tmp_dir)
            z.close()
            shutil.move(os.path.join(tmp_dir, dataid + "_dem.tif"), filedir)
            shutil.move(os.path.join(tmp_dir, dataid + "_num.tif"), filedir)
            shutil.rmtree(tmp_dir)

        gdtm_files.append(os.path.join(filedir, dataid + "_dem.tif"))

    return gdtm_files


def extract_srtm_files(files):
    '''
    dataid.img.zip --> dataid.img
    '''
    POSTFIX_PTN = r".*(?=.img.zip)"
    CMD_TRANS = 'gdal_translate -of GTiff -co "COMPRESS=DEFLATE" -co "INTERLEAVE=BAND" -co "TILED=YES" %s %s'
    srtm_files = []
    for path in files:
        zip_filename = os.path.basename(path)
        tmp = re.match(POSTFIX_PTN, zip_filename)
        dataid = tmp.group()

        f = os.path.join(dst_dir, "SRTM", dataid + ".tif")
        if not os.path.exists(f):
            filedir = os.path.dirname(f)
            tmp_dir = os.path.join(filedir, str(uuid.uuid4()))
            try:
                os.makedirs(tmp_dir)
            except OSError:
                pass
            z = zipfile.ZipFile(path)
            z.extractall(tmp_dir)
            z.close()

            _src = os.path.join(tmp_dir, dataid + ".img")
            _dst = os.path.join(tmp_dir, dataid + ".tif")
            _cmd = CMD_TRANS % (_src, _dst)
            os.system(_cmd)

            shutil.move(_dst, filedir)
            shutil.rmtree(tmp_dir)

        srtm_files.append(f)

    return srtm_files

def parse_dem_filename(dataid):

    if dataid.startswith("ASTGTM2_"):
        fname = "%s/gdem30v2/gdem30v2/%s.zip" % ( DEM_ROOT_DIR, dataid ) # ASTGTM2_N04E015.zip
        return fname

    if dataid.startswith("ASTGTM_"):
        fname = "%s/gdem30/global/data/gdem_utm/%s.img.zip" % ( DEM_ROOT_DIR, dataid ) # ASTGTM2_N04E015.zip
        return fname

    if dataid.startswith("srtm_"):
        fname = "%s/srtm90/TIFF/%s.img.zip" % ( DEM_ROOT_DIR, dataid ) # srtm_02_01.img.zip
        return fname

if __name__ == '__main__':
    #jjj_boundary = os.path.join(shpfolder, 'zhongyuan.shp')
    shp_boundary = os.path.join(shpfolder,'china.shp')
    shpdata = ogr.Open(shp_boundary)
    shplayer = shpdata.GetLayer(0)
    xmin, xmax, ymin, ymax = shplayer.GetExtent()

    dataids = []
    for r in row:
        for c in col:
            dataids.append('srtm_'+r+'_'+c)

    files = [parse_dem_filename(dataid) for dataid in dataids]
    files = [f for f in files if f is not None and os.path.exists(f)]

    tiffiles = extract_srtm_files(files)

    dstfile = os.path.join(dst_dir, 'china_dem.tif')
    cmd = 'gdalwarp -co "COMPRESS=deflate" -co "TILED=YES" -co "BIGTIFF=IF_NEEDED"  -of GTiff -dstnodata none -cutline %s -te %s %s %s %s %s %s' % ( shp_boundary, xmin, ymin, xmax, ymax, " ".join(tiffiles), dstfile)
    print cmd
    os.system(cmd)

