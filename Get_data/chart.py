import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import os
import datetime

def makechart(data, customer, date, ylim):    
    sum_p = int(sum(data['power']) / len(data) * 24)
    max_p = int(max(data['power']))
    min_p = int(min(data['power']))
    ave_p = int(sum_p / 24)
    
    print("Total = {} kWh, Max = {} W, Min = {} W, Ave = {} W".format(sum_p, max_p, min_p, ave_p))
    
    st = min(data['time'])
    et = max(data['time'])
    std = st[11:]
    etd = et[11:]

    xtick = ['0:00', '2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00']
    xu = int(len(data)/12)
    xval = [0, xu, xu*2, xu*3, xu*4, xu*5, xu*6, xu*7, xu*8, xu*9, xu*10, xu*11, xu*12]    

    #plt.xkcd()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(data['power'])
    plt.title(customer + '_' + date)
    ax.text(0, ylim[1] - 100, 'Total energy is {:,d} Wh'.format(sum_p))
    ax.set_ylabel("[kW]")
    ax.set_xticks(xval)
    ax.set_xticklabels(xtick, rotation=45)
    ax.set_ylim(ylim)
    fig.subplots_adjust(left=0.14, bottom=0.16, right=0.9, top=0.9, wspace=0.20, hspace=0.2)
    plt.show()
    #plt.savefig(customer + "_" + date + ".png")

if __name__ == '__main__': 
    os.chdir("data")
    customer = "0060_SONYCSL001"
    date = "2017-05-22"
    data = pd.read_csv(customer + "_" + date + ".csv")
    makechart(data, customer, date, [0, 2000])
    #print(data)

    #print(data['time'].apply(lambda x: datetime.datetime.date(x)))
    