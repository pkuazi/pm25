import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import os, sys, math
import gdal

root_dir = "/mnt/win/PM25/PM25_CIESIN/china"
dem_file = "/mnt/win/dem/china_dem.tif"
aspect_file = "/mnt/win/dem/china_aspect.tif"
slope_file = "/mnt/win/dem/china_slope.tif"
tri_file = "/mnt/win/dem/china_tri.tif"

def raster_to_records(raster_file, dst_file):
    raster = gdal.OpenShared(raster_file)
    if raster is None:
        print("Failed to open file:" + raster_file)
        sys.exit()
    cols = raster.RasterXSize
    rows = raster.RasterYSize
    gt = raster.GetGeoTransform()
    band = raster.GetRasterBand(1)
    noDataValue = band.GetNoDataValue()

    col_list = ['LONGITUDE', 'LATITUDE', 'value']
    df = DataFrame(columns=col_list)
    ix = 0
    for c in range(cols):
        for r in range(rows):
            value = raster.ReadAsArray(c, r, 1, 1)
            if value == noDataValue:
                continue

            x_c = gt[0] + c * gt[1]
            y_c = gt[3] + r * gt[5]
            df.loc[ix] = [x_c, y_c, value]

            print ix
            ix = ix + 1

    df.to_csv(dst_file, index=False)


def add_feature_of_one_value(df, field_name, featurefile):
    rows, cols = df.shape

    # add elevation to the station dataframe
    feature_values = []
    for i in range(rows):
        latitude = df.ix[i]['LATITUDE']
        longitude = df.ix[i]['LONGITUDE']

        if math.isnan(latitude) or math.isnan(longitude):
            feature_value = float('nan')
        else:
            # compute the elevation from DEM data
            feature_raster = gdal.OpenShared(featurefile)
            if feature_raster is None:
                print("Failed to open file:" + featurefile)
                sys.exit()
            gt = feature_raster.GetGeoTransform()
            col = int((longitude - gt[0]) / gt[1])
            row = int((latitude - gt[3]) / gt[5])
            feature_value = feature_raster.ReadAsArray(col, row, 1, 1)
            feature_values.append(feature_value)
    feature_Series = Series(feature_values)
    df[field_name] = feature_Series


if __name__ == "__main__":
    pm_2001_2010 = os.path.join(root_dir, 'cnPM25_200101_201012.tif')
    dst_file = pm_2001_2010[-3] + 'csv'
    raster_to_records(pm_2001_2010, dst_file)

    feature_dict = {'elevation': dem_file, 'aspect': aspect_file, 'slope': slope_file, 'tri': tri_file}
    df = pd.read_csv(dst_file)
    for fea in feature_dict.keys():
        add_feature_of_one_value(df, fea, feature_dict[fea])
    feature_added_file =
    df.to_csv(feature_added_file, index=False)
