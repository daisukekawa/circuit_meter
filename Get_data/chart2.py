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


def linechart(df1, df2, title, house, ylim):
    time = df1.index
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    xtick = ['0:00', '2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00']
    xunit = 7200
    xval = np.arange(0, xunit * 13, xunit)
    ax.set_ylabel("[W]")
    ax.set_xticks(xval)
    ax.set_xticklabels(xtick, rotation=45)
    ax.set_ylim(ylim)
    plt.title(title)
    plt.plot(time, df1, lw = 1, label = house)
    plt.plot(time, df2, lw = 1, label = "Community average")
    ax.fill_between(time, df1.iloc[:,0], df2.iloc[:,0], where = df1.iloc[:,0] > df2.iloc[:,0], facecolor='red', interpolate=True, alpha=0.5)
    ax.fill_between(time, df1.iloc[:,0], df2.iloc[:,0], where = df1.iloc[:,0] <= df2.iloc[:,0], facecolor='green', interpolate=True, alpha=0.5)

    df1_ave = df1.mean(axis=1).mean()/1000*24
    df2_ave = df2.mean(axis=1).mean()/1000*24
    ax.text(0, ylim[1]-100, '{}     : {:.2f} kWh'.format(house, df1_ave))
    ax.text(0, ylim[1]-175, 'Community: {:.2f} kWh'.format(df2_ave))
    plt.legend(loc="upper right")    
    plt.show()
    
    
if __name__ == '__main__': 
    os.chdir("data")
    customers = ['0060_SONYCSL001', '0060_SONYCSL002', '0060_SONYCSL003']
    st_dt = "2017-06-25"
    et_dt = "2017-06-25"
    
    house_list = ['house01', 'house02', 'house03']
    n = 0   #(Select house number: 0-n)
    
    df = pd.DataFrame()
        
    for i in range(len(customers)):
        data = pd.read_csv(customers[i] + "_" + st_dt + "_" + et_dt + ".csv")
        df[house_list[i]] = data['POWER']
    
    #df_house = pd.DataFrame({'TIME': data['TIME'], 'POWER': df['house01']})
    df_house = pd.DataFrame({'TIME': data['TIME'], 'POWER': df.iloc[:, n]})
    df_com = pd.DataFrame({'TIME': data['TIME'], 'POWER': df.mean(axis=1)})
    
    df_day_h = makedaydf(df_house, 'POWER')
    df_day_c = makedaydf(df_com, 'POWER')
    print(df_day_h.iloc[:,0].head())
    linechart(df_day_h, df_day_c, st_dt, house_list[n], [0,2000])
    


    
    