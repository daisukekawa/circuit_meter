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

def cusdata(base_url, user, password, customer, st, et):
    st_dt = datetime.datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
    et_dt = datetime.datetime.strptime(et, '%Y-%m-%d %H:%M:%S')
    #day_len = 31
    #et_dt = st_dt + datetime.timedelta(days=day_len)
    st_unix = int(time.mktime(st_dt.timetuple()))
    et_unix = int(time.mktime(et_dt.timetuple()))
    sts = str(st_unix)
    ets = str(et_unix)
    duration = "&sts=" + sts + "&ets=" + ets + "&time_units=" + tunits

    data = getdata(base_url, user, password, customer, duration)    # pay attention for several customers (so far only one customer)
    print("get {} data from {} to {}".format(customer, st_dt, et_dt))

    utime = data['data'][0]['timestamps']
    power = data['data'][0]['root_powers']
    
    output = pd.DataFrame({'TIME': utime, 'POWER': power})
    output['TIME'] = output['TIME'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    
    filename = customer + "_" + str(datetime.datetime.date(st_dt)) + "_" + str(datetime.datetime.date(et_dt - datetime.timedelta(days=1)))
    output.to_csv(filename + ".csv")
    print("output data to {}.csv".format(filename))
    
    
if __name__ == '__main__':
    base_url = "https://imgate.vw.informetis.com/0.1"
    user = "0060"
    password = "x0d1hpdsXs2S48T6E6ww"
    #command = "/observed_data?customer=0060_SONYCSL001"

    ### Initial setting for the data ###
    st = "2017-06-25 00:00:00"  #Cus1: 2017-05-13~, Cus2/Cus3: 2017-06-24~
    et = "2017-06-26 00:00:00"
    cus_n = 0 #(0~2)

    tunits = "25"   # 20: each minute, 25: each 30 minutes


    os.chdir("data")
    ### Get customers list ###
    cuslist = getcustomers(base_url, user, password)
    cusnum = len(cuslist['customers'])
    customers = []
    for i in range(cusnum):
        customers.append(cuslist['customers'][i]['customer'])    
    print("customer list is {}, number of customers is {}".format(customers, cusnum))
                
    ### Get certain customer data ###
    #customer = cuslist['customers'][cus_n]['customer']
    #cusdata(base_url, user, password, customer, st, et)

    ### Get all customers data ###
    for i in range(cusnum): 
        cusdata(base_url, user, password, cuslist['customers'][i]['customer'], st, et)
    
    