import numpy as np
import os, gdal, sys, osr
from pandas import Series, DataFrame
import pandas as pd
from scipy import stats

root_dir = '/mnt/win/PM25/PM25_CIESIN/china'
# root_dir = '/mnt/win/PM25/PM25_CIESIN/jjj'
dst_dir = '/mnt/win/PM25/PM25_CIESIN/temporal_trend'

t_series = ['199801_200012', '199901_200112', '200001_200212', '200101_200312', '200201_200412', '200301_200512',
            '200401_200612', '200501_200712', '200601_200812', '200701_200912', '200801_201012', '200901_201112',
            '201001_201212']
t_num = len(t_series)


def rst2arr(rasterfile):
    dataset = gdal.OpenShared(rasterfile)
    if dataset is None:
        print("Failed to open file: " + rasterfile)
        sys.exit(1)
    band = dataset.GetRasterBand(1)
    xsize = dataset.RasterXSize  # xsize means number of columns
    ysize = dataset.RasterYSize  # ysize means number of rows
    # proj = dataset.GetProjection()
    # geotrans = dataset.GetGeoTransform()
    # noDataValue = band.GetNoDataValue()
    print "Output file %s size:" % rasterfile, xsize, ysize
    rastervalue = band.ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize)
    return rastervalue


def timevec(root_dir):
    raw_files = os.listdir(root_dir)
    arr_list = []
    for i in range(t_num):
        for file in raw_files:
            if t_series[i] in file:
                file_dir = os.path.join(root_dir, file)
                rstarr = rst2arr(file_dir)
                arr_list.append(rstarr)
                arr_arr = np.array(arr_list)
    vec_arr = arr_arr.transpose((1, 2, 0))
    return vec_arr


def trend_estimation(record):
    y = record
    num = len(record)
    x = np.arange(num)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err


def arr2rst(ref_tif, arr, dst_file):
    dataset = gdal.OpenShared(ref_tif)
    proj = dataset.GetProjection()
    geotrans = dataset.GetGeoTransform()
    # noDataValue = band.GetNoDataValue()
    # output the array in geotiff format
    xsize, ysize = arr.shape
    dst_format = 'GTiff'
    dst_nbands = 1
    dst_datatype = gdal.GDT_Float32

    driver = gdal.GetDriverByName(dst_format)
    dst_ds = driver.Create(dst_file, ysize, xsize, dst_nbands, dst_datatype)
    dst_ds.SetGeoTransform(geotrans)
    dst_ds.SetProjection(proj)
    # dst_ds.GetRasterBand(1).SetNoDataValue(noDataValue)
    dst_ds.GetRasterBand(1).WriteArray(arr)
    # return dst_file


if __name__ == '__main__':
    vec_arr = timevec(root_dir)
    x_size, y_size, dim_num = vec_arr.shape

    slope_array = np.array([])
    intercept_array = np.array([])
    r_square_array = np.array([])
    p_value_array = np.array([])
    std_err_array = np.array([])


    # timearr_2d = np.array([])
    for i in range(x_size):
        for j in range(y_size):
            # timearr_2d = np.append(timearr_2d, vec_arr[i, j])
            slope, intercept, r_value, p_value, std_err = trend_estimation(vec_arr[i, j])
            slope_array = np.append(slope_array, slope)
            intercept_array = np.append(intercept_array, intercept)
            r_square_array = np.append(r_square_array, r_value ** 2)
            p_value_array = np.append(p_value_array, p_value)
            std_err_array = np.append(std_err_array, std_err)

            # save slope and intercept values with according p_value < 0.05


    # timearr_2d = timearr_2d.reshape(-1, dim_num)
    slope_array = slope_array.reshape([x_size,y_size])
    print np.max(slope_array)
    print np.min(slope_array)

    intercept_array = intercept_array.reshape(x_size,y_size)
    r_square_array = r_square_array.reshape(x_size,y_size)
    p_value_array=p_value_array.reshape(x_size,y_size)
    std_err_array=std_err_array.reshape(x_size,y_size)

    # save to tif for display
    ref_tif = os.path.join(root_dir,'cnPM25_199801_200012.tif')

    # slope file
    dst_slope = os.path.join(dst_dir,'cn_slope.tif')
    arr2rst(ref_tif, slope_array,dst_slope)

    # intercept file
    dst_intercept = os.path.join(dst_dir,'cn_intercept.tif')
    arr2rst(ref_tif, intercept_array,dst_intercept)

    # r_square file
    dst_r_square = os.path.join(dst_dir,'cn_r2.tif')
    arr2rst(ref_tif, r_square_array,dst_r_square)

    # r_square file
    dst_p_value = os.path.join(dst_dir,'cn_p.tif')
    arr2rst(ref_tif, p_value_array,dst_p_value)

    # r_square file
    dst_std_err = os.path.join(dst_dir,'cn_std_err.tif')
    arr2rst(ref_tif, std_err_array,dst_std_err)


