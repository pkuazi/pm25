import numpy as np
import os, gdal, sys, osr, math
from pandas import Series, DataFrame
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

root_dir = "/mnt/win/PM25/PM25_CIESIN/china"
dem_file = "/mnt/win/dem/china_dem.tif"
aspect_file = "/mnt/win/dem/china_aspect.tif"
slope_file = "/mnt/win/dem/china_slope.tif"
tri_file = "/mnt/win/dem/china_tri.tif"


def raster_to_records(pm_file, dem_file):
    raster = gdal.OpenShared(pm_file)
    if raster is None:
        print("Failed to open file:" + pm_file)
        sys.exit()
    cols = raster.RasterXSize
    rows = raster.RasterYSize
    gt = raster.GetGeoTransform()
    band = raster.GetRasterBand(1)
    noDataValue = band.GetNoDataValue()

    dem_raster = gdal.OpenShared(dem_file)
    if dem_raster is None:
        print("Failed to open file:" + dem_file)
        sys.exit()
    dem_gt = dem_raster.GetGeoTransform()

    col_list = ['LONGITUDE', 'LATITUDE', 'value', 'elevation']
    df = DataFrame(columns=col_list)
    ix = 0
    for c in range(cols):
        for r in range(rows):
            value = raster.ReadAsArray(c, r, 1, 1)[0][0]
            if value == noDataValue:
                continue

            x_c = gt[0] + c * gt[1]
            y_c = gt[3] + r * gt[5]

            elev = get_elevation(x_c, y_c, dem_raster, dem_gt)
            df.loc[ix] = [x_c, y_c, value, elev]

            print ix
            ix = ix + 1
    return df


def get_elevation(x, y, dem_raster, dem_gt):
    col = int((x - dem_gt[0]) / dem_gt[1])
    row = int((y - dem_gt[3]) / dem_gt[5])
    elevation = dem_raster.ReadAsArray(col, row, 1, 1)[0][0]
    return elevation


if __name__ == "__main__":
    pm_2001_2010 = os.path.join(root_dir, 'cnPM25_200101_201012.tif')
    dst_file = pm_2001_2010[:-3] + 'csv'

    # df = raster_to_records(pm_2001_2010, dem_file)
    # df.to_csv(dst_file, index=False)

    df = pd.read_csv(dst_file)

    x = np.array(df.LONGITUDE)
    y = np.array(df.LATITUDE)
    z = np.array(df.elevation)
    c = np.array(df.value)

    # create the figure, add a 3d axis, set the viewing angle
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(45,60)

    # ax.plot_surface(x,y,z,facecolors=cm.RdYlGn(c))
    # ax.scatter(x,y,z,c=c, cmap = plt.hot())
    ax.scatter(x,y,z,c=c, cmap = cm.coolwarm)

    plt.show()
