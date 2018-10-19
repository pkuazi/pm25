import os, sys
import numpy as np
import ogr, gdal
from pandas import Series, DataFrame
import pandas as pd

shp_dir = "/mnt/mfs/zjh/rspm25/shpdata/cn_cluster_time"
rst_dir = "/mnt/mfs/zjh/rspm25/PM25_CIESIN/china"
dst_dir = "/mnt/mfs/zjh/rspm25/PM25_CIESIN/cn_clusterclip"
t_series = ['199801_200012', '199901_200112','200001_200212','200101_200312','200201_200412','200301_200512','200401_200612', '200501_200712','200601_200812', '200701_200912', '200801_201012','200901_201112', '201001_201212']
t_num = len(t_series)

def clip():
    for k in range(8):
        # read each shapefile to clip rasters of all years
        shpfile = os.path.join(shp_dir,'cn_cluster_time_c'+str(k)+'.shp')
        shpdata = ogr.Open(shpfile)
        shplayer = shpdata.GetLayer(0)
        xmin, xmax, ymin, ymax = shplayer.GetExtent()

        # read each year's raster data
        rst_files = os.listdir(rst_dir)
        for i in range(t_num):
            for file in rst_files:
                if t_series[i] in file:
                    rstfile = os.path.join(rst_dir, file)
                    dstfile = os.path.join(dst_dir , t_series[i]+'_c'+str(k) + ".tif")
                    cmd = 'gdalwarp -co "COMPRESS=deflate" -co "TILED=YES" -co "BIGTIFF=IF_NEEDED" -of GTiff -dstnodata none -cutline %s -te %s %s %s %s %s %s' % (
                        shpfile, xmin, ymin, xmax, ymax, rstfile, dstfile)
                    print cmd
                    os.system(cmd)
def stats():
    for k in range(8):
        statfile = os.path.join(dst_dir, 'stats'+'_c'+str(k)+'.csv')
        stat_arr = np.array([])
        for t in range(t_num):
            rstname = os.path.join(dst_dir,t_series[t]+'_c'+str(k)+'.tif')
            print("file %s will be statisticed" % rstname)
            dataset = gdal.OpenShared(rstname)

            if dataset is None:
                print("Failed to open file: " + rstname)
                sys.exit(1)

            band = dataset.GetRasterBand(1)
            xsize = dataset.RasterXSize
            ysize = dataset.RasterYSize
            rv = band.ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize)

            if np.sum(rv)==0:
                break

            max = np.max(rv[(rv>0)])
            min = np.min(rv[(rv>0)])
            mean = np.mean(rv[(rv>0)])
            median = np.median(rv[(rv>0)])
            var = np.var(rv[(rv>0)])

            arr = np.array([max, min, mean, median, var])
            stat_arr = np.append(stat_arr,arr)
        stat_arr = stat_arr.reshape(-1,5)

        frame = DataFrame(stat_arr)
        frame.to_csv(statfile)

        print("file %s has been statisticed successfully"% rstname)

if __name__ == '__main__':
    clip()
    stats()


