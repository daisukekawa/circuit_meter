import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import os

def makedaydf(df1, colname):
    datetime = pd.DatetimeIndex(df1["TIME"])
    date = np.unique(datetime.date)
    time = np.unique(datetime.time)
    
    df1["TIME"] = datetime.time
    df1 = df1.set_index("TIME")
    df = pd.DataFrame()
    dft = df1[colname]
 
    for i in range(len(date)):
        rows = len(time) * i
        rowe = len(time) * (i + 1)
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

def linechart(df1, df2, df3, title, ylim):
    time = df2.index
    date = len(df1.columns)
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    xtick = ['0:00', '2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00']
    xunit = 7200
    xval = np.arange(0, xunit * 13, xunit)
    ax.set_ylabel("[W]")
    ax.set_xticks(xval)
    ax.set_xticklabels(xtick, rotation=45)
    #ax.set_ylim(ylim)
    plt.title(title)
    for i in range(date):
        plt.plot(df1.iloc[:,i], lw = 0.3, color = "gray")

    plt.plot(time, df2, lw = 1, color = "blue", label = "weekday.ave")
    plt.plot(time, df3, lw = 1, color = "orangered", label = "weekend.ave")
    df2_ave = df2.mean(axis=1).mean()/1000*24
    df3_ave = df3.mean(axis=1).mean()/1000*24
    ax.text(0, ylim[1]-50, 'Weekday: {:.2f} kWh'.format(df2_ave), color = "blue")
    ax.text(0, ylim[1]-100, 'Weekend: {:.2f} kWh'.format(df3_ave), color = "orangered")
    #plt.legend()    
    plt.show()
 
def linechart2(df_day):
    df_d = df_day.mean(axis=0)*24/1000
    days = len(df_d)
    df_w = weather()
    df_w = df_w[0:days]

    day = df_day.index
    fig, (ax0, ax1, ax2) = plt.subplots(nrows = 3, sharex = False, figsize=(10,8))

    ax0.plot(df_d)
    ax1.plot(df_w['TEMP_AVE'], lw = 1, color = "green", label = "TEMP_AVE")
    ax1.plot(df_w['TEMP_MAX'], lw = 1, color = "green", label = "TEMP_MAX")
    ax1.plot(df_w['TEMP_MIN'], lw = 1, color = "green", label = "TEMP_MIN")
    ax2.plot(df_w['SUN_RADIATION'], lw = 1, color = 'orange')
    ax1.tick_params(top='off', bottom='off', left='on', right='off', labelleft='on', labelbottom='off')    
    ax2.tick_params(top='off', bottom='off', left='on', right='off', labelleft='on', labelbottom='off')    
    ax0.set_ylabel("Demand [kWh]", fontsize = 8)
    ax1.set_ylabel("Temp. [Celsius]", fontsize = 8)
    ax2.set_ylabel("Sun Radiation [MJ/m2]", fontsize = 8)
    for label in (ax0.get_xticklabels() + ax0.get_yticklabels()):
        label.set_fontsize(8)
    for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
        label.set_fontsize(8)
    for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
        label.set_fontsize(8)
    plt.show()

def linechart3(df_day):
    df_d = df_day.mean(axis=0)*24/1000
    days = len(df_d)

    day = df_day.index
    fig, ax0 = plt.subplots(figsize=(10,8))

    ax0.plot(df_d)
    ax0.set_ylabel("Demand [kWh]", fontsize = 8)
    for label in (ax0.get_xticklabels() + ax0.get_yticklabels()):
        label.set_fontsize(8)
    plt.show()
    
def linechart4(df_day1, df_day2, df_day3, df_day4):
    df_d1 = df_day1.mean(axis=0)*24/1000
    df_d2 = df_day2.mean(axis=0)*24/1000
    df_d3 = df_day3.mean(axis=0)*24/1000
    df_d4 = df_day4.mean(axis=0)*24/1000
    days = len(df_d1)

    #day = df_day1.index
    fig, ax0 = plt.subplots(figsize=(10,8))
    
    print(df_d1.iloc[1])
    print(df_d1.index[0])
    print(ax0.get_xticklabels())
    print("house1: {:.2f} kWh".format(df_d1.mean()))
    print("house2: {:.2f} kWh".format(df_d2.mean()))
    print("house3: {:.2f} kWh".format(df_d3.mean()))
    print("house4: {:.2f} kWh".format(df_d4.mean()))
    ax0.plot(df_d1)
    ax0.plot(df_d2)
    ax0.plot(df_d3)
    ax0.plot(df_d4)
    ax0.set_ylabel("Demand [kWh]", fontsize = 9)
    ax0.text(df_d1.index[0], 6.0, 'house1: {:.2f} kWh'.format(df_d1.mean()), color = "blue")
    ax0.text(df_d1.index[0], 5.5, 'house2: {:.2f} kWh'.format(df_d2.mean()), color = "orangered")
    ax0.text(df_d1.index[0], 5.0, 'house3: {:.2f} kWh'.format(df_d3.mean()), color = "green")
    ax0.text(df_d1.index[0], 4.5, 'house4: {:.2f} kWh'.format(df_d4.mean()), color = "red")
    #ax0.text(0, ylim[1]-100, 'Weekend: {:.2f} kWh'.format(df3_ave), color = "orangered")
    plt.legend(['house1', 'house2', 'house3', 'house4'])  
    for label in (ax0.get_xticklabels() + ax0.get_yticklabels()):
        label.set_fontsize(8)
        
    plt.show()  
    
    
def barplot(df1, df2, title):
    fig, ax = plt.subplots()
    width = 0.5
    colors = ['blue', 'lightblue', 'green', 'darkgray']
    labels = ['0:00-6:00', '6:00-12:00', '12:00-18:00', '18:00-24:00']
    df_plt = pd.concat([df1['POWER'], df2['POWER']], axis=1)
    df_plt = df_plt.T
    bottom = np.zeros(df_plt.shape[0])
    xval = np.arange(len(df_plt))
    
    plt.title(title)
    plt.ylabel("[kWh]")
    for i in range(df_plt.shape[1]):
        plt.bar(xval, df_plt.iloc[:,i], width, bottom, color=colors[i], label=labels[i])
        for j in range(len(df_plt)):
            ann = ax.annotate("{:.2f}".format(df_plt.iloc[j,i]), xy=(xval[j]-width*0.1, bottom[j]+df_plt.iloc[j,i]*0.45),fontsize=12, color="white")
        bottom += df_plt.iloc[:,i]
    
    #fig.subplots_adjust(left=0.12, bottom=0.19, right=0.9, top=0.9, wspace=0.15, hspace=0.15)
    plt.xticks(xval, ["Weekday", "Weekend"])
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles[::-1], labels[::-1], bbox_to_anchor=(0.64, 0.3), fontsize=9)
    #fig.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.15, hspace=0.15)
    plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')    
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.show()

         
def data_aggregation(df1):
    day = df1.columns
    df_all = pd.DataFrame()
    df_weekday = pd.DataFrame()
    df_weekend= pd.DataFrame()
    
    for i in range(len(day)):
        if(datetime.date.weekday(day[i]) < 5):
            df_weekday = df_weekday.append(df1[day[i]])
        else:
            df_weekend= df_weekend.append(df1[day[i]])
        
    df_weekday = df_weekday.T
    df_weekend= df_weekend.T

    #df_all = df1.mean(axis=0)*24/1000
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

    ylim = [0, 1000]
    ylim2 = [0, 15]
    linechart(df1, df_wd_ave, df_we_ave, "Weekday and Weekend, {} ~ {}".format(df1.columns.min(), df1.columns.max()), ylim)
    #barplot(df_wd_agg, df_we_agg, "Energy Consumption")
    
    print("Peak: {:.2f} kW".format(peak))
    print("Weekdays: {:.2f} kWh".format(wd_ave))
    print("   0:00-6:00: {:.2f} kWh, 6:00-12:00: {:.2f} kWh, 12:00-18:00: {:.2f} kWh, 18:00-24:00: {:.2f} kWh"
          .format(wd_ave1['POWER'], wd_ave2['POWER'], wd_ave3['POWER'], wd_ave4['POWER']))
    print("Weekends: {:.2f} kWh".format(we_ave))
    print("   0:00-6:00: {:.2f} kWh, 6:00-12:00: {:.2f} kWh, 12:00-18:00: {:.2f} kWh, 18:00-24:00: {:.2f} kWh"
          .format(we_ave1['POWER'], we_ave2['POWER'], we_ave3['POWER'], we_ave4['POWER']))
    #print(df_all)

def weather():
    wdata = pd.read_csv("weather.csv", usecols=(0,1,8,11,14))
    wdata.columns = ['DAY', 'TEMP_AVE', 'TEMP_MAX', 'TEMP_MIN', 'SUN_RADIATION'] #SUN_RADIATION [MJ/m2]
    #print(wdata)
    return wdata
    
if __name__ == '__main__': 
    os.chdir("data")
    customers = ['0060_SONYCSL001', '0060_SONYCSL002', '0060_SONYCSL003', '0060_SONYCSL004']
    st_dt = "2017-05-13"
    et_dt = "2017-07-14"
    
    house_list = ['house01', 'house02', 'house03', 'house04']
    n = 0   #(Select house number: 0-n)
    
    df = pd.DataFrame() # df for all houses
    
    for i in range(len(customers)):
        data = pd.read_csv(customers[i] + "_" + st_dt + "_" + et_dt + ".csv")
        df[house_list[i]] = data['POWER']
    
    #df_house = pd.DataFrame({'TIME': data['TIME'], 'POWER': df.iloc[:, n]}) # for certain house
    df_com = pd.DataFrame({'TIME': data['TIME'], 'POWER': df.mean(axis=1)})
    
    df_day_h1 = makedaydf(pd.DataFrame({'TIME': data['TIME'], 'POWER': df.iloc[:, 0]}), 'POWER')
    df_day_h2 = makedaydf(pd.DataFrame({'TIME': data['TIME'], 'POWER': df.iloc[:, 1]}), 'POWER')
    df_day_h3 = makedaydf(pd.DataFrame({'TIME': data['TIME'], 'POWER': df.iloc[:, 2]}), 'POWER')
    df_day_h4 = makedaydf(pd.DataFrame({'TIME': data['TIME'], 'POWER': df.iloc[:, 3]}), 'POWER')
    df_day_c = makedaydf(df_com, 'POWER')
    
    
    #linechart2(df_day_h1)  # plot daily consumptions and weather data for the duration.
    #linechart3(df_day_h1) # plot daily consumptions for the duration
    linechart4(df_day_h1, df_day_h2, df_day_h3, df_day_h4)   # plot daily consumptions for the duration
    #data_aggregation(df_day_h1) # plot hourly consumptions and weekday weekend data.
    #print(df.tail())
    #linechart4(df_day_h)