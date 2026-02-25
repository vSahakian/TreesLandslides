#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 10:12:59 2025

@author: vjs
"""
import numpy as np
import obspy as obs
import datetime as dt
import pandas as pd



# %%
### Paths
mseed_dir = '/Users/vjs/research/treeslandslides/data/mseed/'
quarrydata_raw_path = '/Users/vjs/research/treeslandslides/data/quarryblasts/blastdata_raw.csv'
quarrydata_path = '/Users/vjs/research/treeslandslides/data/quarryblasts/blastdata.csv'


## Local to UTC difference in hours
local2utc_DST_dt = 7  # daylight savings
local2utc_ST_dt = 8  # normal savings

## daylight savings time date in 2024 during array installation - 2025 was during it
DST_date = dt.datetime(2024,11,3)


# %%

## Read in quarry blast data
blastdf_raw = pd.read_csv(quarrydata_raw_path)

## Convert local to a datetime objec,t then to UTC, save to new file
blastdf_raw['LocalDateTime'] = blastdf_raw['LocalDateTime'].str.replace('Z', '', regex=False)
blastdf_raw['LocalDateTime'] = pd.to_datetime(blastdf_raw['LocalDateTime'])

## Convert to UTC Datetme, save in column - start of with DST time:
## copy:
blastdf = blastdf_raw.copy()

## Convert each row if it is before or after daylight savings day this year
for index,row in blastdf_raw.iterrows():
    if (row['LocalDateTime'] > DST_date) & (row['LocalDateTime'].year ==2024):
        print('out of DST')
        print(row)
        blastdf.at[index,'UTCDateTime'] = blastdf_raw.loc[index]['LocalDateTime'] + pd.Timedelta(hours=local2utc_ST_dt)
    else:
        blastdf.at[index,'UTCDateTime'] = blastdf_raw.loc[index]['LocalDateTime'] + pd.Timedelta(hours=local2utc_DST_dt)
        
## Save new df:
blastdf.to_csv(quarrydata_path,index=False)