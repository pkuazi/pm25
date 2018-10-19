import numpy as np
import os, gdal, sys, osr
from pandas import Series, DataFrame
import pandas as pd
from sklearn.cluster import KMeans

#root_dir ='/mnt/mfs/zjh/rspm25/PM25_CIESIN/jjj'
dst_dir ='/mnt/mfs/zjh/rspm25/PM25_CIESIN/timevec_grid'

root_dir = '/usr/research/PM25_CIESIN/china'

t_series = ['199801_200012', '199901_200112','200001_200212','200101_200312','200201_200412','200301_200512','200401_200612', '200501_200712','200601_200812', '200701_200912', '200801_201012','200901_201112', '201001_201212']
t_num = len(t_series)

def rst2arr(rasterfile):
    dataset = gdal.OpenShared(rasterfile)
    if dataset is None:
        print("Failed to open file: " + rasterfile)
        sys.exit(1)
    band = dataset.GetRasterBand(1)
    xsize = dataset.RasterXSize #xsize means number of columns
    ysize = dataset.RasterYSize # ysize means number of rows
    #proj = dataset.GetProjection()
    #geotrans = dataset.GetGeoTransform()
    #noDataValue = band.GetNoDataValue()
    print "Output file %s size:" % rasterfile, xsize, ysize
    rastervalue = band.ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize)
    return rastervalue

def timevec(root_dir):
    raw_files = os.listdir(root_dir)
    arr_list = []
    for i in range(t_num):
        for file in raw_files:
            if t_series[i] in file:
                file_dir = os.path.join(root_dir,file)
                rstarr = rst2arr(file_dir)
                arr_list.append(rstarr)
                arr_arr = np.array(arr_list)
    vec_arr = arr_arr.transpose((1,2,0))
    return vec_arr

def fea_extract(record):
    num = len(record)
    x = np.arange(num)
    y = record
    fea_arr = np.array([])
    for i in range(1,4):
        cof = np.polyfit(x, y, i)
        fea_arr = np.append(fea_arr,cof)
    feadim_num = fea_arr.shape[0]
    return fea_arr, feadim_num

def cluster_kmeans(x_arr):
    y_pred = KMeans(n_clusters=8).fit_predict(x_arr)
    return y_pred

def arr2rst(arr, dst_file):
    rst = "/mnt/mfs/zjh/rspm25/PM25_CIESIN/china/cnPM25_199801_200012.tif"
    dataset = gdal.OpenShared(rst)
    proj = dataset.GetProjection()
    geotrans = dataset.GetGeoTransform()
    #noDataValue = band.GetNoDataValue()
    # output the array in geotiff format
    xsize, ysize = arr.shape
    dst_format = 'GTiff'
    dst_nbands = 1
    dst_datatype = gdal.GDT_UInt32

    driver = gdal.GetDriverByName(dst_format)
    dst_ds = driver.Create(dst_file, ysize, xsize, dst_nbands, dst_datatype)
    dst_ds.SetGeoTransform(geotrans)
    dst_ds.SetProjection(proj)
    #dst_ds.GetRasterBand(1).SetNoDataValue(noDataValue)
    dst_ds.GetRasterBand(1).WriteArray(arr)
    #return dst_file

def array2raster(newRasterfn,array):
#def array2raster(newRasterfn, rasterOrigin, pixelWidth, pixelHeight, array):
    cols = array.shape[1]
    rows = array.shape[0]
    #originX = rasterOrigin[0]
    #originY = rasterOrigin[1]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Byte)
    #outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outRaster.SetGeoTransform((73.487345, 0.09998016476345838, 0.0, 53.561602, 0.0, -0.10005585311871228))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

if __name__ == '__main__':

    vec_arr = timevec(root_dir)
    x_size, y_size, dim_num = vec_arr.shape

    feaarr_2d = np.array([])
    timearr_2d = np.array([])
    for i in range(x_size):
        for j in range(y_size):
            timearr_2d = np.append(timearr_2d,vec_arr[i,j])
            fea_arr,feadim_num = fea_extract(vec_arr[i,j])
            feaarr_2d = np.append(feaarr_2d,fea_arr)
    timearr_2d = timearr_2d.reshape(-1,dim_num)
    
    #get the min and max value of pm25 data to draw legend
    max = np.max(timearr_2d)
    min = np.min(timearr_2d)
    print max
    print min
    
#     feaarr_2d = feaarr_2d.reshape(-1,feadim_num)
# 
#     cluster_time = cluster_kmeans(timearr_2d)
#     cluster_time = cluster_time.reshape(x_size,y_size)
# 
#     cluster_fea = cluster_kmeans(feaarr_2d)
#     cluster_fea = cluster_fea.reshape(x_size,y_size)
# 
#     rst1 = os.path.join(dst_dir, 'cluster_time1.tif')
#     rst2 = os.path.join(dst_dir, 'cluster_fea1.tif')
# 
#     #array2raster(rst1,cluster_time)
#     #array2raster(rst2, cluster_fea)
# 
#     arr2rst(cluster_time,rst1)
#     arr2rst(cluster_fea,rst2)


'''
    save_arr = np.array([])
    loc_label = []
    for i in range(x_size):
        for j in range(y_size):
            if sum(vec_arr[i,j])!=0:
                #save_arr = np.append(save_arr,vec_arr[i,j])
                loc_label.append((i,j))

                fea_arr = fea_extract(vec_arr[i,j])
                save_arr = np.append(save_arr,fea_arr)
    #save_arr = save_arr.reshape(-1,dim_num)
    save_arr = save_arr.reshape(-1, fea_arr.shape[0])

    frame = DataFrame(save_arr)
    frame.to_csv(dst_file)

'''
