import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_trend(x, y):
    """ Plot 1D data """
    #change string to float in y
#     for i in y:
#         if i =='NULL':
            
    fig = plt.figure()
    fig.suptitle('pm25 trend from 2014-05-01 to 2015-04-30', fontsize = 14, fontweight='bold')
    
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel("time")
    ax.set_ylabel("pm25")
    ax.set_xlim(735354,xmax=max(x))
    
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32),interval=15))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)
       
    ax.plot(x,y)
    plt.show()
    
if __name__=='__main__':
    filename = "/root/workspace/airpollution/airquality.csv"
    #Station ID     Time     PM25     PM10     NO2     CO     O3     SO2
    #001001,2014-05-01 00:00:00,138,159.4,56.3,0.9,50.8,17.2
 
    st_id, dates, PM25, PM10, NO2, CO, O3, SO2 = np.genfromtxt(filename,delimiter=",", skip_header =1,unpack= True, missing_values="NULL", filling_values=np.nan, converters={1:mdates.strpdate2num('%Y-%m-%d %H:%M:%S')})
    plot_trend(dates, PM25)