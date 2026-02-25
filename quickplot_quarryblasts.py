#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 10:12:59 2025

@author: vjs
"""
import numpy as np
import obspy as obs
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime as dt
import matplotlib.dates as mdates


# %%
### Paths
mseed_dir = '/Users/vjs/research/treeslandslides/data/mseed/'
quarrydata_path = '/Users/vjs/research/treeslandslides/data/quarryblasts/blastdata.csv'

fig_dir = '/Users/vjs/research/treeslandslides/plots/blasts2024/'


# ## Time before blast to plot in minutes
preblast_dt = 1

# ## Time after blast in minutes
postblast_dt = 5

## Array info:
network = '8M'
station_nums = np.r_[np.arange(101,111),np.arange(201,216)]
# station_nums = np.array([100,101])

array_start = dt.datetime(2024,10,29)
array_end = dt.datetime(2024,11,25)



# %%

## Read in quarry blast data
blastdf_all = pd.read_csv(quarrydata_path)

## Convert utc date time column to dt object:
blastdf_all['UTCDateTime'] = pd.to_datetime(blastdf_all['UTCDateTime'])

# subset it to keep only the ones inside the array dates:
blastdf = blastdf_all.copy()
blastdf = blastdf_all.loc[(blastdf.UTCDateTime >= array_start) & (blastdf.UTCDateTime <= array_end)]



## Loop through blasts:
for blast_ind,blast_row in blastdf.iterrows():
    ## Get blast UTC Time
    blast_time = blast_row['UTCDateTime']
    print(f"Processing blast at {blast_time}")
    
    ## Get start and end time for plot based on blast time:
    plot_start = blast_time - pd.Timedelta(minutes=preblast_dt)
    plot_end = blast_time + pd.Timedelta(minutes=postblast_dt)
    
    # Create subdirectories for this blast inside the fig_dirs
    blast_label = f"blast{blast_ind+1:02d}"
    blast_dir_png = os.path.join(fig_dir, 'png', blast_label)
    blast_dir_pdf = os.path.join(fig_dir, 'pdf', blast_label)
    os.makedirs(blast_dir_png, exist_ok=True)
    os.makedirs(blast_dir_pdf, exist_ok=True)
        
    ## Loop through stations to plot it:
    for i_station in station_nums:
        ## Make stream object:                    
        st = obs.Stream()

        # Dates needed: day of start and possibly day after
        dates_needed = [plot_start.date()]
        ## If the plot start and end are not on the same day, append a date needed
        if plot_start.date() != plot_end.date():
            dates_needed.append(plot_end.date())
        
        ## for the days needed for the plot, set file path and open/append to st
        for date in dates_needed:
            i_fstart = f"{date}T00_00_00"
            i_fend = f"{date}T23_59_59"
            base_filename = f"{network}_{i_station}_s{i_fstart}_e{i_fend}.mseed"
            file_path = os.path.join(mseed_dir, base_filename)
        
            ## If the file path exists, open up and append to stream:
            if os.path.exists(file_path):
                try:
                    st += obs.read(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
            ## Otherwise, print an error
            else:
                print(f"Missing file: {file_path}")
        
        ## If there's nothing in the stream there's no data, print and continue
        if len(st) == 0:
            print(f"No data for station {i_station} around {blast_time}")
            continue
        
        ## Merge the streams and trim to the plotting window
        # Merge and trim to plotting window
        st.merge(method=1, fill_value='interpolate')
        st.trim(starttime=obs.UTCDateTime(plot_start), endtime=obs.UTCDateTime(plot_end))
        
        ## If there's nothing in here, continue and print error
        if len(st) == 0:
            print(f"No usable data after trimming for station {i_station}")
            continue
        
        ## Grab the trace to plot
        tr = st[0]
        times = tr.times("matplotlib")
        
        i_fig, i_ax = plt.subplots(figsize=(10, 2))
        
        ## Plot data
        i_ax.plot_date(times, tr.data, 'k-', linewidth=0.8, markersize=0)
        
        ## Plot blast time
        i_ax.axvline(obs.UTCDateTime(blast_time).matplotlib_date, color='r', linestyle='--', label='Blast Time')
        
        ## x axis format
        ## Set x axis major ticks
        i_ax.xaxis.set_major_locator(mdates.SecondLocator(bysecond=range(0,60,15)))
        i_ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ## minor ticks every 1 second
        # i_ax.xaxis.set_minor_locator(mdates.SeceondLocator(interval=1))
        
        ## Labels
        i_ax.set_title(f"Station {i_station} | {blast_time}")
        i_ax.set_xlabel("Time (UTC)")
        i_ax.set_ylabel("Amplitude")
        i_ax.legend()

        i_fig.autofmt_xdate()

        # Output filenames
        i_fname = f"{blast_label}_station{i_station}_{blast_time.strftime('%Y%m%dT%H%M%S')}"
        i_fig.savefig(os.path.join(blast_dir_png, i_fname + ".png"), dpi=200, bbox_inches='tight')
        i_fig.savefig(os.path.join(blast_dir_pdf, i_fname + ".pdf"), dpi=300, bbox_inches='tight')
        plt.close(i_fig)
        
        
        
        
        
