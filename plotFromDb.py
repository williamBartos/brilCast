import sqlite3
import time
from datetime import datetime
from io import StringIO


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num

def plot():
    ids = []
    temps = []
    inTemps = []
    inHums = []
    timeStamps = []
    
    
    conn = sqlite3.connect('brilCast.db')
    conn.row_factory = sqlite3.Row
    
    try:
        cur = conn.cursor()
        cur.execute('select id, temp, inTemp, inHum, time from entries order by id desc')
        rows = cur.fetchall()
    
    finally: 
        cur.close()
    
    for row in rows:
        ids.append(row[0])
        temps.append(row[1])
        inTemps.append(row[2])
        inHums.append(row[3])
        timeStamps.append(row[4])
    
    dates = [datetime.strptime(date,'%Y-%m-%d %H:%M:%S') for date in timeStamps]
    
    
    fig = plt.figure()
    plot0 = fig.add_subplot(3,1,1)
    plot1 = fig.add_subplot(3,1,2)
    plot2 = fig.add_subplot(3,1,3)
    
    plot0.set_ylim([0, 100])
    plot1.set_ylim([0, 100])
    plot2.set_ylim([0, 100])
    
    
    
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=25)
    
    xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    
    plot0.xaxis.set_major_formatter(xfmt)
    plot0.xaxis_date()
    plot0.plot_date(dates, temps, 'b-')
    plot0.set_title('Outside Temperature')
    plt.setp(plot0.get_xticklabels(), visible=False)
    
    
    plot1.xaxis.set_major_formatter(xfmt)
    plot1.xaxis_date()
    plot1.plot_date(dates, inTemps, 'b-')
    plot1.set_title('Inside Temperature')
    plt.setp(plot1.get_xticklabels(), visible=False)
    
    
    
    plot2.xaxis.set_major_formatter(xfmt)
    plot2.xaxis_date()
    plot2.plot_date(dates, inHums, 'b-')
    plot2.set_title('Inside Humidity')
    
    plt.savefig('./images/bar.png')
    
plot()
    
    
    


    
