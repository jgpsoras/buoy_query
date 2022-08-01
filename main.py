import pandas as pd
import numpy as np
import urllib.request as u
import re
import csv



url = 'https://www.ndbc.noaa.gov/data/realtime2/46254.txt'
response = u.urlopen(url)
raw = response.read()
raw = raw.decode('UTF-8')

regex = ' +'
raw_formatted = re.sub(regex, ' ', raw)

fh = open('new_buoy.txt', 'w')
fh.write(raw_formatted)
fh.close()

df = pd.read_csv('new_buoy.txt', sep=' ')
df = df.drop(columns = ['WDIR', 'WSPD', 'GST', 'PRES', 'ATMP', 'DEWP', 'VIS', 'PTDY', 'TIDE'])
df = df.rename(columns={'#YY':'year', 'MM':'month', 'DD':'day', 'hh':'hour', 'mm':'minute',
                        'WVHT':'WVHT(m)', 'DPD':'DPD(sec)', 'APD':'APD(sec)', 'MWD':'MWD(deg)', 'WTMP':'WTMP(degC)'})
df = df.drop(index = 0)

final_csv = [['PST Input', 'WVHT(m)', 'DPD(sec)', 'APD(sec)', 'MWD(deg)', 'WTMP(degC)']]
months_31days = ['01','03','05','07','08','10','12']
months_30days = ['04','06','09','11']
months_28days = ['02']

while True:
    month = input('Enter two digit month: ')
    day = input('Enter two digit day: ')
    pst_hour = input('Enter two digit hour then am or pm: ')
    minute = input('Enter minute (26 or 56): ')
    done = input('Done? y or n: ')
    req = month+'/'+day+'/'+pst_hour+'/'+minute

    if pst_hour[2:] == 'am':
        pst_hour24 = int(pst_hour[0:2])
    else:
        pst_hour24 = int(pst_hour[0:2]) + 12
    gmt_hour24 = pst_hour24 + 7

    if gmt_hour24 > 23:
        gmt_hour24 = gmt_hour24 - 24
        day = int(day) + 1

        if day == 32 and month in months_31days:
            month = int(month) + 1
            day = 1
            if month == 13:
                month = 1
            if month > 9:
                month = str(month)
            else:
                month = '0' + str(month)
        if day == 31 and month in months_30days:
            month = int(month) + 1
            day = 1
            if month == 13:
                month = 1
            if month > 9:
                month = str(month)
            else:
                month = '0' + str(month)
        if day == 29 and month in months_28days:
            month = int(month) + 1
            day = 1
            if month == 13:
                month = 1
            if month > 9:
                month = str(month)
            else:
                month = '0' + str(month)

        if day > 9:
            day = str(day)
        else:
            day = '0' + str(day)

    if gmt_hour24 > 9:
        final_hour = str(gmt_hour24)
    else:
        final_hour = '0' + str(gmt_hour24)

    df_query = df[(df['month']==month) & (df['day']==day) & (df['hour']==final_hour) & (df['minute']==minute)]
    vals = df_query[['WVHT(m)', 'DPD(sec)', 'APD(sec)', 'MWD(deg)', 'WTMP(degC)']].squeeze().to_list()
    vals.insert(0, req)
    final_csv.append(vals)

    if done == 'y':
        break

with open('buoy.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(final_csv)



