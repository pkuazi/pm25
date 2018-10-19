import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm 
import os, gdal, sys, osr
from matplotlib.colors import ListedColormap

vmax = 709.299987793
vmin = 0.0

root_dir ='/mnt/win/data/PM25/PM25_CHINA'
t_series = [str(x) for x in range(1999,2017)]
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
    print( "Output file %s size:" % rasterfile, xsize, ysize)
    rastervalue = band.ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize)
    return rastervalue

def draw(file):
    # 1) opening maido geotiff as an array
    raster = gdal.OpenShared(file)
    data = raster.ReadAsArray()

    # 2) transformation of coordinates
    cols = raster.RasterXSize
    rows = raster.RasterYSize
    gt = raster.GetGeoTransform()

    x = (cols*gt[1])+gt[0]
    y = (rows*gt[5])+gt[3]

    X = np.arange(gt[0], x, gt[1]*600)
    Y = np.arange(gt[3], y, gt[5]*600)

    # 3) creation of a simple grid
    X, Y = np.meshgrid(X,Y)

    plt.title('2000')

    parameters = np.linspace(0,110,10)
    norm = matplotlib.colors.Normalize(vmin=np.min(parameters), vmax = np.max(parameters))

#     choose a colormap
    c_m = matplotlib.cm.cool
#     create a ScalarMappable and initialize a data structure
    s_m = matplotlib.cm.ScalarMappable(cmap=c_m, norm=norm)
    s_m.set_array([])

    fig = plt.figure(figsize=(12, 8))
    plt.imshow(data, cmap=c_m)
    plt.colorbar(s_m)
    # plt.show()

if __name__ == '__main__':
    
    # cmap0 = ListedColormap(['white', 'green', 'blue','red'])
    #
    # fig, axes = plt.subplots(2,2,sharex=True,facecolor = 'w')
    #
    #
    # cmap2 = cm.get_cmap('prism',1000)
    # cmap = cm.get_cmap('rainbow',100)
    # cmap1 = cm.get_cmap('spectral',100)
    # norm = matplotlib.colors.Normalize(vmin=0, vmax=vmax)
    #
    file_tobe_drawn=[]

    raw_files = os.listdir(root_dir)
    for i in range(8,12):
        for file in raw_files:
            if t_series[i] in file and file.endswith('.tif'):
                file_dir = os.path.join(root_dir,file)
                file_tobe_drawn.append(file_dir)
    draw(file_tobe_drawn[0])
#                 rstarr = rst2arr(file_dir)
#                 rstarr[rstarr==0] = np.nan
#                 ax = axes[i/2-4,i%2]
#                 ax.imshow(rstarr,interpolation="nearest",cmap=cmap1,norm=norm)
#
# #                 cbar = plt.colorbar(gci)
# #                 cbar.set_label('mg/m3')
# #                 cbar.set_ticks(np.linspace(vmin,vmax,8))
# #                 cbar.set_ticklabels( ('10', '15', '25', '35', '100',  '500'))
#
# #                 gci=plt.imshow(rstarr, extent=extent, origin='lower',cmap=cmap, norm=norm)
# #                 cb = plt.colorbar()
# #                 cb.axes.tick_params(labelsize=25)
# #                 cb.set_label(r'mg/m3', labelpad=10, y=0.45)
#     #cb = plt.colorbar(mappable=axes, cax=None, ax=None,shrink=0.5)
#     #cb.set_label('(%)')
#
#     #legend
#
#
#     #plt.colorbar()
#     #fig.colorbar(axes).set_label('mg/m3', rotation=270)
#     colormap = ['Spectral, summer, coolwarm, Wistia_r, pink_r, Set1, Set2, Set3, brg_r, Dark2, prism, PuOr_r, afmhot_r, terrain_r, PuBuGn_r, RdPu, gist_ncar_r,     gist_yarg_r, Dark2_r, YlGnBu, RdYlBu, hot_r, gist_rainbow_r, gist_stern, PuBu_r, cool_r, cool, gray, copper_r, Greens_r, GnBu, gist_ncar, spring_r,     gist_rainbow, gist_heat_r, Wistia, OrRd_r, CMRmap, bone, gist_stern_r, RdYlGn, Pastel2_r, spring, terrain, YlOrRd_r, Set2_r, winter_r, PuBu, RdGy_r,     spectral, rainbow, flag_r, jet_r, RdPu_r, gist_yarg, BuGn, Paired_r, hsv_r, bwr, cubehelix, Greens, PRGn, gist_heat, spectral_r, Paired, hsv,    Oranges_r, prism_r, Pastel2, Pastel1_r, Pastel1, gray_r, jet, Spectral_r, gnuplot2_r, gist_earth, YlGnBu_r, copper, gist_earth_r, Set3_r, OrRd,     gnuplot_r, ocean_r, brg, gnuplot2, PuRd_r, bone_r, BuPu, Oranges, RdYlGn_r, PiYG, CMRmap_r, YlGn, binary_r, gist_gray_r, Accent, BuPu_r, gist_gray,     flag, bwr_r, RdBu_r, BrBG, Reds, Set1_r, summer_r, GnBu_r, BrBG_r, Reds_r, RdGy, PuRd, Accent_r, Blues, autumn_r, autumn, cubehelix_r, nipy_spectral_r,     ocean, PRGn_r, Greys_r, pink, binary, winter, gnuplot, RdYlBu_r, hot, YlOrBr, coolwarm_r, rainbow_r, Purples_r, PiYG_r, YlGn_r, Blues_r, YlOrBr_r,     seismic, Purples, seismic_r, RdBu, Greys, BuGn_r, YlOrRd, PuOr, PuBuGn, nipy_spectral, afmhot']
#
#
#     plt.show()

