#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 16:29:24 2025

@author: vjs
"""
## Write batch script to download ph5 data, by station

import datetime as dt
import numpy as np

# %%    Parameters and Stuff

##### EDIT THESE PARAMETERS FOR YOUR OWN MACHINE/ACCOUNT CREDENTIALS #######
## Batch download script path:
# batch_script_path = '/Users/vjs/research/treeslandslides/scripts/2_batch_ph5.sh' 
batch_script_path = '/Users/vjs/research/treeslandslides/scripts/2_batch_ph5_2025.sh' 
# batch_script_path = '/Users/vjs/research/treeslandslides/scripts/2_batch_ph5_4Will.sh' 

## Output file directory:
# output_mseed_dir = '/Users/vjs/research/treeslandslides/data/mseed'  ## Change this to the directory you want the miniseed files to save to
output_mseed_dir = '/Users/vjs/research/treeslandslides/data/mseed_2025'  ## Change this to the directory you want the miniseed files to save to
 
## access token:
# accesstoken = 'bvbc0gOlZHWjykZc'  ## Change this to be the Access token from your earthscope account
# user_name = 'vjs@uoregon.edu'     ## Change this to be the user name from your earthscope account
accesstoken = 'Oi7wsSBf5Koeu5Wj'  ## As of Feb 24 2026 (expires in 180 days)
user_name = 'vjs@uoregon.edu'     ## Change this to be the user name from your earthscope account


# accesstoken = 'EVtu5RjHIdG5D0cO'  ## Change this to be the Access token from your earthscope account
# user_name = 'wstruble@uh.edu'     ## Change this to be the user name from your earthscope account


################################# END EDIT ##################################

# ############
# ## Data download parameters - 2024 experiment, batch_ph5.sh
# network = '8M'  ## Earthscope network code
# station_list = np.append(np.arange(101,111,1),np.arange(201,216,1)).astype('str') ## stations are 101-110, 201-215

# array_start = '2024-10-29T00:00:00' ## start of experiment
# array_end = '2024-11-25T23:59:59' ## end of experiment

## Data download parameters - 2025 experiment, batch_ph5_2025.sh
network = '8M'  ## Earthscope network code
station_list = np.append(np.arange(101,111,1),np.arange(201,216,1)).astype('str') ## stations are 101-110, 201-215

array_start = '2024-10-29T00:00:00' ## start of experiment
array_end = '2024-11-25T23:59:59' ## end of experiment

# %% Make needed arrays

## Make download start time array:
array_start_datetime = dt.datetime.fromisoformat(array_start)
array_end_datetime = dt.datetime.fromisoformat(array_end)
    
## Number of days to download:
num_days = array_end_datetime - array_start_datetime

## Make download end time array:
day_start_list = []
for i_num_days in range(num_days.days + 1):
    i_day_start = array_start_datetime + dt.timedelta(i_num_days)
    day_start_list.append(i_day_start)


# %% Write to the file
with open(batch_script_path,'w') as file:
    ## Write first script line:
    file.write('#!/bin/bash \n')
        
    ## Loop over station:
    for i_station in station_list:
        ## Loop over day:
        for j_day_start in day_start_list:
            j_day_end = j_day_start + dt.timedelta(hours=23,minutes=59,seconds=59)  ## End of day for download call
            ## Make the output path, replacing : in datetime with _ to save file correctly
            ij_outputpath = '%s/%s_%s_s%s_e%s.mseed' % (output_mseed_dir,network,i_station,j_day_start.isoformat().replace(":","_"),j_day_end.isoformat().replace(":","_"))
            print(ij_outputpath)
            
            ## Get start/end times in string format for command:
            ij_starttime = j_day_start.isoformat()
            ij_endtime = j_day_end.isoformat()
    
            ## Define the call text. Adds a 10 second sleep after each one to not overload/get booted off Earthcope's servers
            call_text = "curl -L --digest --user %s:%s -o %s 'https://service.iris.edu/ph5ws/dataselect/1/queryauth?reqtype=fdsn&format=mseed&network=%s&channel=DP*&starttime=%s&endtime=%s&station=%s&nodata=404' \nsleep 10 \n" % (user_name,accesstoken,ij_outputpath,network,ij_starttime,ij_endtime,i_station)

            ## Write the call text to the file:
            file.write(call_text)