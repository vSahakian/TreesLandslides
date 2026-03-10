#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:38:26 2026

@author: vjs
"""
import numpy as np
import obspy as obs
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime as dt
import matplotlib.dates as mdates
from obspy import read_inventory
from glob import glob

# %%
### Paths
mseed_dir = '/Users/vjs/research/treeslandslides/data/mseed_2024_8M/'


## Response file XML input:
respXML_path = '/Users/vjs/research/treeslandslides/data/response_files/xml/8M_resp.xml'

## Output response file resp format:
response_dir = '/Users/vjs/research/treeslandslides/data/response_files/resp/8M/'

# Prefilter:
prefilt_list=(0.001, 0.005, 0.95*250, 250) ## very low taper, 0.001 - 0.005 Hz; upper taper is 95% of fN to fN


# %%
# Create subdirectories for this blast inside the fig_dirs
mseed_corrected_path = os.path.join(mseed_dir, 'corrected')
os.makedirs(mseed_corrected_path, exist_ok=True)

# %% Make a glob of the files to correct:
mseedraw_glob = glob(os.path.join(mseed_dir, 'raw') + '/*.mseed')

# %%
## For each file in the directory, import, remove the response

## Load the resp file:)
inv = read_inventory(respXML_path)

for i_mseed in mseedraw_glob:
    ## Get the basename:
    i_basename = os.path.basename(i_mseed)
    print(f'Correcting for {i_basename}')
    
    ## Get output file:
    i_correctedpath = os.path.join(mseed_dir, 'corrected',i_basename)
    
    ## Read in and correct:
    i_st = obs.read(i_mseed)
    i_st.remove_response(inventory=inv, output="VEL", pre_filt=prefilt_list)
    
    ## Write out:
    print(f'writing to {i_correctedpath}')
    i_st.write(i_correctedpath)

# # %%
# st = obs.read('/Users/vjs/research/treeslandslides/data/mseed_2024/raw/8M_101_s2024-11-19T00_00_00_e2024-11-19T23_59_59.mseed')
# st.plot()

# # Load your inventory (StationXML or Dataless)
# inv = read_inventory(respXML_path)

# st.remove_response(inventory=inv, output="VEL", water_level=60, pre_filt=(0.001, 0.005, 45, 50))
# st.plot()
    
