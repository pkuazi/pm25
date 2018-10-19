#
# -*-coding:utf-8 -*-
#
# @Author: zhaojianghua
# @Date  : 2018-10-18 14:54
#

"""

"""
import gdal
import sys, os, json
import numpy as np

dst_dir = '/mnt/win/data/PM25/PM25_CHINA_reclass'

def rststats(time,rasterfile):
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


    data = {}
    data["time"] = time
    data["class1"] = count1
    data["class2"] = count2
    data["class3"] = count3
    data["class4"] = count4
    data["class5"] = count5


    stats_str = json.dumps(data)
    return stats_str

if __name__ == '__main__':
    f = open("/mnt/win/data/PM25/stats/stats_year_reclass.txt", 'w+')

    raw_files = os.listdir(dst_dir)
    for file in raw_files:
        if file.endswith('.tif'):
            year = file[-8:-4]
            file = os.path.join(dst_dir, file)
            stats = rststats(year, file)
            print >> f, stats

    f.close()

