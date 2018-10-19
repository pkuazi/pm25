#! /usr/bin/env python
# coding: utf-8
import gdal
import psycopg2
import ogr, os, osr
import sys
import numpy as np
import json
import matplotlib.pyplot as plt

provinceid = [11,12,13,14,15,21,22,23,31,32,33,34,35,36,37,41,42,43,44,45,46,50,51,52,53,54,61,62,63,64,65,71,81,82]
#provinceid = [46]
p_num = len(provinceid)

t_series = ['199801_200012', '199901_200112','200001_200212','200101_200312','200201_200412','200301_200512','200401_200612', '200501_200712','200601_200812', '200701_200912', '200801_201012','200901_201112', '201001_201212']
t_num = len(t_series)

classid = [1,2,3,4,5,6]
c_num = len(classid)

rstfolder = '/usr/research/PM25_CIESIN/province_stats'
dstfolder = "/usr/research/PM25_CIESIN/province_stats"

def rststats(rasterfile):
    dataset = gdal.OpenShared(rasterfile)
    if dataset is None:
        print("Failed to open file: " + rasterfile)
        sys.exit(1)
    band = dataset.GetRasterBand(1)
    xsize = dataset.RasterXSize
    ysize = dataset.RasterYSize
    print "Output file %s size:" % rasterfile, xsize, ysize
    rastervalue = band.ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize)
    data = np.array([])
    count1 = np.sum(rastervalue == 1)
    count2 = np.sum(rastervalue == 2)
    count3 = np.sum(rastervalue == 3)
    count4 = np.sum(rastervalue == 4)
    count5 = np.sum(rastervalue == 5)
    count6 = np.sum(rastervalue == 6)
    data = np.append(data,[count1,count2,count3,count4,count5,count6])
    return data

def plt_c_year(ax,pid, pdata):
#     plt.title(' province:%s'%str(pid))
#     plt.xlabel('Time')
#     plt.ylabel('Area')
    x = np.arange(t_num)
    color = ['r','g','b','y','b','c']
    for i in range(c_num):
        y = pdata[:,i]
        ax.plot(x, y, color[i], label=str(classid[i]))


if __name__ == '__main__':
    # the dim of stdata is year, province, class
    stdata = np.array([])
    for i in range(t_num):
        for pid in provinceid:
            rst = os.path.join(rstfolder,str(pid)+"_" + t_series[i] + ".tif")
            pidyear = rststats(rst)
            stdata = np.append(stdata,pidyear )
    stdata = stdata.reshape(t_num,p_num,c_num)
    print "the dim:", stdata.shape

    # the dim of pro_of_alltime is province, year,class
    pro_of_alltime = stdata.transpose((1,0,2))
      
    # matplotlib 6classes variation along the 13 years for each province
    fig, axes = plt.subplots(6,6,sharex=True)
    for i in range(p_num):
        x = np.arange(t_num)
        color = ['r','g','b','y','k','c']
        pdata = pro_of_alltime[i]
        ax = axes[i/6,i%6]
        for j in range(c_num):
            y = pdata[:,j]
            ax.plot(x, y, color[j], label=str(classid[j]))
            ax.set_title("province: %s"%provinceid[i])
        
    plt.legend(loc='best')
    plt.show()   

    '''
    # matplotlib class1 (<10) variation along the 13 years for each province
    fig, axes = plt.subplots(6,6,sharex=True, sharey=True)
    for i in range(p_num):
        x = np.arange(t_num)
        color = ['r','g','b','y','b','c']
        pdata = pro_of_alltime[i]
        ax = axes[i/6,i%6]
        for j in range(2,3):
            y = pdata[:,j]
            ax.plot(x, y, color[j], label=str(classid[j]))
            ax.set_title("province: %s"%provinceid[i])
        
    plt.legend(loc='best')
    plt.show()   
    '''
  
#     fig = plt.figure()
#     
#     for i in range(p_num):
#         pdata = pro_of_alltime[i]
#         ax = fig.add_subplot(6,6,i+1)
#        plt_c_year(ax,provinceid[i],pdata)
#     plt.legend(loc='best')
#     plt.show()
    
    
    # the dim of class_of_alltime is class,year, province
#     class_of_alltime = stdata.transpose((2,0,1))
#     print "year of %s is: %s" % (t_series[2],stdata[2,:,:])





