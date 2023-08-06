# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:25:27 2021

@author: Chris Downs
"""

import boto3
from io import StringIO
from multiprocessing.pool import ThreadPool
import os
import pandas as pd
import requests
import s3fs

from ccrenew import all_df_keys


s3_config = boto3.client('s3')
bucket = 'perfdatadev.ccrenew.com'
bucket_prefix_satellite = "5min_archive/Solcats/"
bucket_prefix_measured = "5min_archive/PF/"

df_keys = all_df_keys

# https://preview-docs.solcast.com.au/


def make_satellite_key(CCR_ID, date):
    return bucket_prefix_satellite + CCR_ID + "/" + "sat_weather_" + date.strftime('%Y-%m-%d') + ".csv"

def make_measured_key(CCR_ID, date):
    return bucket_prefix_measured + CCR_ID + "/" + "main_" + date.strftime('%Y-%m-%d') + ".csv"

def retrieve_df(key):
    fs = s3fs.S3FileSystem(anon=False)
    path = "s3://{b}/{k}".format(b=bucket, k=key)
    try:
        with fs.open(path, 'rb') as f:
            df = pd.read_csv(f, index_col = 0, parse_dates = True)
            df = df.loc[~df.index.duplicated(), :]
    except FileNotFoundError:
        df = pd.DataFrame()
    return df

def bucket_push(df, s3_key):
    fileobj = StringIO()
    df.to_csv(fileobj)
    fileobj.seek(0)
    s3_config.upload_fileobj(fileobj, bucket, s3_key)

def get_cat_files(site):
    s3=boto3.resource('s3')
    mybucket=s3.Bucket(bucket) # type: ignore
    files = []
    for cat_file in mybucket.objects.filter(Delimiter='/', Prefix=(bucket_prefix_satellite +'{}/'.format(site))):
        files.append((cat_file.key))

    return files

def get_solcats(site): #yes solCATS. because typos that last forever are funny
    
    PRIMARY_KEY = os.environ['SOLCAST_PRIMARY_KEY']
    API_URL = "https://api.solcast.com.au/"
    
    hours=168
    if site == 'NC-000166':
        lat=df_keys.GPS_Lat.loc[df_keys.CCR_ID==site][0]
        lon=df_keys.GPS_Long.loc[df_keys.CCR_ID==site][0]
        tz='US/'+str(df_keys.Timezone.loc[df_keys.CCR_ID==site][0])
    else:
        lat=df_keys.GPS_Lat.loc[df_keys.CCR_ID==site].item()
        lon=df_keys.GPS_Long.loc[df_keys.CCR_ID==site].item()
        tz='US/'+str(df_keys.Timezone.loc[df_keys.CCR_ID==site].item())

    key_url="&api_key={}".format(PRIMARY_KEY)
    lat_url='&latitude={}'.format(lat)
    long_url='&longitude={}'.format(lon)
    hour_url='&hours={}'.format(hours)
    format_url='&format=json'
    period_url='&period=PT5M'
    params_url='&output_parameters=air_temp,clearsky_dhi,clearsky_dni,clearsky_ghi,cloud_opacity,dhi,dni,ghi,precipitable_water,precipitation_rate,snow_water,wind_speed_10m'
    
    url=API_URL+"data/live/radiation_and_weather?"+key_url+lat_url+long_url+hour_url+format_url+period_url+params_url   #new URL
    response=requests.get(url)
    if response.status_code==200:
        df_cats=pd.DataFrame(response.json()['estimated_actuals'])
    
        #fix the timestamp and make it localized to the site. i.e we want the ghi here to line up exactly with the ghi from PF or AE
        df_cats['time']=df_cats.period_end #period end is solcast's column for the timestamp. I believe it is hour end UTC
        df_cats['time']=pd.to_datetime(df_cats['time'])
        df_cats.set_index(df_cats['time'])
        df_cats.index.name=None
        df_cats=df_cats.sort_index() #actually order the dataframe because the original df is all out of order
        df_cats=df_cats.tz_localize('Etc/GMT').tz_convert(tz).tz_localize(None)#uses gmt+1 to switch from hour end to start
    
        return response.status_code,df_cats
    else:
        return response.status_code,None
        