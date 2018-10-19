# -*- coding: utf-8 -*-
import gdal,sys,os
import numpy as np
#root_dir = "/mnt/mfs/zjh/rspm25/PM25_CIESIN/jjj"
#dst_dir = "/mnt/mfs/zjh/rspm25/PM25_CIESIN/pm25_6grades/jjj"

root_dir = '/mnt/win/data/PM25/PM25_CHINA'
dst_dir = '/mnt/win/data/PM25/PM25_CHINA_reclass'
# root_dir ='/mnt/mfs/zjh/rspm25/PM25_CIESIN/global'
# dst_dir ='/mnt/mfs/zjh/rspm25/PM25_CIESIN/pm25_6grades/global'

def reclassify(rasterfile, dst_file):
    dataset = gdal.OpenShared(rasterfile)
    if dataset is None:
        print("Failed to open file: " + rasterfile)
        sys.exit(1)
    band = dataset.GetRasterBand(1)
    xsize = dataset.RasterXSize
    ysize = dataset.RasterYSize
    proj = dataset.GetProjection()
    geotrans = dataset.GetGeoTransform()
    noDataValue = band.GetNoDataValue()

    print "Output file %s size:" % rasterfile, xsize, ysize
    rastervalue = band.ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize)

    #mask0 = rastervalue==noDataValue
    #rastervalue[mask0] = np.nan

    mask1_1 = rastervalue<10
    mask1_2 = rastervalue>0
    mask1 = np.logical_and(mask1_1, mask1_2)
    rastervalue[mask1] = 1

    mask2_1 = rastervalue >= 10
    mask2_2 = rastervalue<15
    mask2 = np.logical_and(mask2_1, mask2_2)
    rastervalue[mask2] = 2

    mask3_1 = rastervalue>=15
    mask3_2 = rastervalue<25
    mask3=np.logical_and(mask3_1,mask3_2)
    rastervalue[mask3]=3

    mask4_1 = rastervalue >= 25
    mask4_2 = rastervalue < 35
    mask4 = np.logical_and(mask4_1, mask4_2)
    rastervalue[mask4] = 4


    #mask5_1 = rastervalue >= 35
    #mask5_2 = rastervalue < 100
    #mask5 = np.logical_and(mask5_1, mask5_2)
    #rastervalue[mask5] = 5

    # rastervalue[rastervalue >= 35 & rastervalue < 100] = 5
    #
    # mask6 = rastervalue >= 100
    # rastervalue[mask6] = 6

    mask5 = rastervalue >= 35
    rastervalue[mask5] = 5

    # output the array in geotiff format
    dst_format = 'GTiff'
    dst_datatype = gdal.GDT_UInt32
    dst_nbands = 1

    driver = gdal.GetDriverByName(dst_format)
    dst_ds = driver.Create(dst_file, xsize, ysize,dst_nbands,dst_datatype)

    dst_ds.SetGeoTransform(geotrans)
    dst_ds.SetProjection(proj)
    dst_ds.GetRasterBand(1).SetNoDataValue(noDataValue)
    dst_ds.GetRasterBand(1).WriteArray(rastervalue)

    return dst_file

if __name__ == '__main__':
    raw_files = os.listdir(root_dir)
    for name in raw_files:
        if name.endswith(".tif"):
            dstfile = os.path.join(dst_dir, 'rec_' + name)
            if os.path.exists(dstfile):
                print "the reclassified pm2.5 data : %s already exists.." % name
                continue
            filename = os.path.join(root_dir, name)
            reclassify(filename,dstfile)
