# -*- coding: utf-8 -*-

import urllib.request as urllib2
import json
import matplotlib.pyplot as plt
import datetime
import time
from matplotlib.dates import HourLocator
import pandas as pd
import numpy as np
import os


def getcustomers(base_url, user, password):
    headers ={}
    headers["Authorization"] = "imSP " + (user + ":" + password)
    url = base_url + "/get_customers"
    req = urllib2.Request(url = url, headers=headers)
    res = urllib2.urlopen(req)
    cuslist = json.load(res)
    return cuslist


def getdata(base_url, user, password, customer, duration):
    headers ={}
    headers["Authorization"] = "imSP " + (user + ":" + password)
    url = base_url + "/observed_data?customer=" + customer + duration
    req = urllib2.Request(url=url, headers=headers)
    res = urllib2.urlopen(req)
    resj = json.load(res)
    return resj

    
if __name__ == '__main__':
    base_url = "https://imgate.vw.informetis.com/0.1"
    user = "0060"
    password = "x0d1hpdsXs2S48T6E6ww"
    #command = "/observed_data?customer=0060_SONYCSL001"

    ### Set start and end time
    st = "2017-05-22 00:00:00"
    #et = "2017-05-15 00:00:00"
    tunits = "20"   # 20 -> each minute
    st_dt = datetime.datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
    #et_dt = datetime.datetime.strptime(et, '%Y-%m-%d %H:%M:%S')
    et_dt = st_dt + datetime.timedelta(days=1)
    st_unix = int(time.mktime(st_dt.timetuple()))
    et_unix = int(time.mktime(et_dt.timetuple()))
    sts = str(st_unix)
    ets = str(et_unix)
    duration = "&sts=" + sts + "&ets=" + ets + "&time_units=" + tunits

    cuslist = getcustomers(base_url, user, password)
    customer = cuslist['customers'][0]['customer']
    print("get customers information")
    data = getdata(base_url, user, password, customer, duration)    # pay attention for several customers (so far only one customer)
    print("get {} data from {} to {}".format(customer, st_dt, et_dt))

    utime = data['data'][0]['timestamps']
    power = data['data'][0]['root_powers']
    
    output = pd.DataFrame({'time': utime, 'power': power})
    output['time'] = output['time'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    
    filename = customer + "_" + str(datetime.datetime.date(st_dt))
    os.chdir("data")
    output.to_csv(filename + ".csv")
    print("output data to {}.csv".format(filename))
    
    