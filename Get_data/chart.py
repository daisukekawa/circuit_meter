import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import os

def makedaydf(df1, day_len, colname):
    datetime = pd.DatetimeIndex(df1["TIME"])
    date = np.unique(datetime.date)
    time = np.unique(datetime.time)
 
    df1["TIME"] = datetime.time
    df1 = df1.set_index("TIME")
    df = pd.DataFrame()
    dft = df1[colname]
 
    for i in range(len(date)):
        rows = day_len * i
        rowe = day_len * (i + 1)
        df[date[i]] = dft.iloc[rows:rowe]
    return df
 
 
def daychart(data, customer, date, ylim):    
    sum_p = int(sum(data['POWER']) / len(data) * 24)
    max_p = int(max(data['POWER']))
    min_p = int(min(data['POWER']))
    ave_p = int(sum_p / 24)
    
    print("Total = {} kWh, Max = {} W, Min = {} W, Ave = {} W".format(sum_p, max_p, min_p, ave_p))
    
    st = min(data['TIME'])
    et = max(data['TIME'])
    std = st[11:]
    etd = et[11:]

    xtick = ['0:00', '2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00']
    xu = int(len(data)/12)
    xval = [0, xu, xu*2, xu*3, xu*4, xu*5, xu*6, xu*7, xu*8, xu*9, xu*10, xu*11, xu*12]    

    #plt.xkcd()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(data['POWER'])
    plt.title(customer + '_' + date)
    ax.text(0, ylim[1] - 100, 'Total energy is {:,d} Wh'.format(sum_p))
    ax.set_ylabel("[kW]")
    ax.set_xticks(xval)
    ax.set_xticklabels(xtick, rotation=45)
    ax.set_ylim(ylim)
    fig.subplots_adjust(left=0.14, bottom=0.16, right=0.9, top=0.9, wspace=0.20, hspace=0.2)
    plt.show()
    #plt.savefig(customer + "_" + date + ".png")

def dayschart(df1, ylimit):
    date = len(df1.columns)
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    for i in range(date):
        plt.plot(df1.iloc[:,i], lw = 0.3, color = "gray")
    df_ave = df1.mean(axis=1)
    plt.plot(df_ave, lw = 1, color = "blue")
    
    xtick = ['0:00', '2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00']
    xunit = 7200
    xval = np.arange(0, xunit * 13, xunit)
    ax.set_ylabel("[kW]")
    ax.set_xticks(xval)
    ax.set_xticklabels(xtick, rotation=45)
    plt.title('Energy consumption from {} to {}'.format(df1.columns.min(), df1.columns.max()))
    #ax.text(0, 2400, 'Total energy is {:,d} Wh'.format(len(df1)))
    plt.show()

def linechart(df1, df2, title):
    time = df1.index
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    xtick = ['0:00', '2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00']
    xunit = 7200
    xval = np.arange(0, xunit * 13, xunit)
    ax.set_ylabel("[kW]")
    ax.set_xticks(xval)
    ax.set_xticklabels(xtick, rotation=45)
    plt.title(title)
    plt.plot(time, df1, lw = 1, color = "blue", label = "weekday.ave")
    plt.plot(time, df2, lw = 1, color = "orangered", label = "weekend.ave")
    df1_ave = df1.mean(axis=1).mean()/1000*24
    df2_ave = df2.mean(axis=1).mean()/1000*24
    ax.text(0, 850, 'Weekday: {:.2f} kWh'.format(df1_ave))
    ax.text(0, 800, 'Weekend: {:.2f} kWh'.format(df2_ave))
    plt.legend()    
    plt.show()
 

def barplot(df1, df2, title):
    fig, ax = plt.subplots(figsize=(10,5))
    xval = np.arange(len(df1))
    print(xval)
    plt.bar(df1.index, df1, color="blue")
    plt.title(title)
    plt.ylabel("[kWh]")

    #fig.subplots_adjust(left=0.12, bottom=0.19, right=0.9, top=0.9, wspace=0.15, hspace=0.15)
    #ax.spines['right'].set_color('none')
    #ax.spines['top'].set_color('none')
    plt.show()
 
         
def data_aggregation(df1):
    day = df1.columns
    df_weekday = pd.DataFrame()
    df_weekend= pd.DataFrame()
    for i in range(len(day)):
        if(datetime.date.weekday(day[i]) < 5):
            df_weekday = df_weekday.append(df1[day[i]])
        else:
            df_weekend= df_weekend.append(df1[day[i]])
    df_weekday = df_weekday.T
    df_weekend= df_weekend.T
    
    df_wd_ave = pd.DataFrame({'POWER': df_weekday.mean(axis=1)})
    df_wd_ave.index = df1.index
    df_we_ave = pd.DataFrame({'POWER': df_weekend.mean(axis=1)})
    df_we_ave.index = df1.index

    wd_ave = df_weekday.mean(axis=1).mean()/1000*24
    we_ave = df_weekend.mean(axis=1).mean()/1000*24
    peak = df1.max().max()/1000
    
    slice1 = int(len(df1)* 1/4)
    slice2 = int(len(df1)* 2/4)
    slice3 = int(len(df1)* 3/4)
    slice4 = int(len(df1)* 4/4)
    
    wd_ave1 = df_wd_ave.iloc[0:slice1,:].mean()/1000*24/4
    wd_ave2 = df_wd_ave.iloc[slice1:slice2,:].mean()/1000*24/4
    wd_ave3 = df_wd_ave.iloc[slice2:slice3,:].mean()/1000*24/4
    wd_ave4 = df_wd_ave.iloc[slice3:slice4,:].mean()/1000*24/4

    wd = [wd_ave1['POWER'], wd_ave2['POWER'], wd_ave3['POWER'], wd_ave4['POWER']]

    we_ave1 = df_we_ave.iloc[0:slice1,:].mean()/1000*24/4
    we_ave2 = df_we_ave.iloc[slice1:slice2,:].mean()/1000*24/4
    we_ave3 = df_we_ave.iloc[slice2:slice3,:].mean()/1000*24/4
    we_ave4 = df_we_ave.iloc[slice3:slice4,:].mean()/1000*24/4
    we = [we_ave1['POWER'], we_ave2['POWER'], we_ave3['POWER'], we_ave4['POWER']]

    df_wd_agg = pd.DataFrame({'TIME': ['0:00-6:00', '6:00-12:00', '12:00-18:00', '18:00-24:00'], 'POWER': wd})
    df_we_agg = pd.DataFrame({'TIME': ['0:00-6:00', '6:00-12:00', '12:00-18:00', '18:00-24:00'], 'POWER': we})

    #linechart(df_wd_ave, df_we_ave, "Weekday and Weekend, {} ~ {}".format(df1.columns.min(), df1.columns.max()))
    barplot(df_wd_agg, df_we_agg, "Title")
    
    print("Peak: {:.2f} kW".format(peak))
    print("Weekdays: {:.2f} kWh".format(wd_ave))
    print("   0:00-6:00: {:.2f} kWh, 6:00-12:00: {:.2f} kWh, 12:00-18:00: {:.2f} kWh, 18:00-24:00: {:.2f} kWh"
          .format(wd_ave1['POWER'], wd_ave2['POWER'], wd_ave3['POWER'], wd_ave4['POWER']))
    print("Weekends: {:.2f} kWh".format(we_ave))
    print("   0:00-6:00: {:.2f} kWh, 6:00-12:00: {:.2f} kWh, 12:00-18:00: {:.2f} kWh, 18:00-24:00: {:.2f} kWh"
          .format(we_ave1['POWER'], we_ave2['POWER'], we_ave3['POWER'], we_ave4['POWER']))
    

if __name__ == '__main__': 
    os.chdir("data")
    customer = "0060_SONYCSL001"
    st_dt = "2017-05-13"
    et_dt = "2017-05-26"
    data = pd.read_csv(customer + "_" + st_dt + "_" + et_dt + ".csv")
    df_day = makedaydf(data, 60*24, "POWER")
    #dayschart(df_day, [0, 2000])
    data_aggregation(df_day)
    #print(data)

    #print(data['time'].apply(lambda x: datetime.datetime.date(x)))
    