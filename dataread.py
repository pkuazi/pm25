import csv
import numpy as np
import json

data_dir = "/mnt/mfs/zjh/rspm25/airquality.csv"
day_avg_dir = "/mnt/mfs/zjh/rspm25/day_avg.csv"

#Station ID 	Time 	PM25 	PM10 	NO2 	CO 	O3 	SO2
#001001,2014-05-01 00:00:00,138,159.4,56.3,0.9,50.8,17.2
def csvread(data_dir):
    st_001010 = np.array([])
    with open(data_dir, 'rb') as csvfile:
        aqreader = csv.reader(csvfile)
        for row in aqreader:
            col = len(row)
            if row[0]=='001010':
                date = row[1].split()[0]
                time = row[1].split()[1]
                record = [row[0],date,time,row[2],row[3],row[4],row[5],row[6],row[7]]
                st_001010 = np.append(st_001010, record)
    st_001010 = st_001010.reshape(-1,9)
    return  st_001010


#['001010', '2014-05-01', '00:00:00', '87', '141.9', '47.5', '0.7','113.8', '16.1']

def day_avg(st_data):
    average = {}
    day_name = np.unique(st_data[:,1])
    day_num = len(day_name)
    print 'total days: ',day_num
    for d in range(day_num):
        r_start = d*24
        r_end = (d+1)*25+100
        day = day_name[d]

        day_data = np.array([])
        for row in st_data[r_start:r_end,:]:
            if row[1]==day:
                print row
                hour_record = []
                for i in range(3,9):
                    if row[i] == 'NULL':
                        hour_record.append(np.nan)
                    else:
                        hour_record.append(float(row[i]))
            day_data = np.append(day_data, hour_record)

        day_data = day_data.reshape(-1, 6)
        day_avg = np.nanmean(day_data, axis=0)
        average[day]=np.ndarray.tolist(day_avg)
    return average

if __name__=="__main__":
    st_1001 = csvread(data_dir)
    day_avg = day_avg(st_1001)
    day_avgdata = json.dumps(day_avg)

    f = open(day_avg_dir, 'w+')
    f.write(day_avgdata)
    f.close()
