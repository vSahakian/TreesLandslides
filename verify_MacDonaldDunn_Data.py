#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 12:26:26 2025

@author: vjs
"""
import obspy
from obspy.io.segy.core import _read_segy
#import segpy.reader
import numpy as np
from obspy import Stream, Trace, UTCDateTime


## Directory with data:
data_dir = '/Users/vjs/research/treeslandslides/data/Jan22_SEGD_Corrected_Stations'






def read_segd(file_path,endianness='>'):
    try:
        # Try reading the SEG-D file using SEG-Y reader (may work for some cases)
        stream = _read_segy(file_path, endian=endianness, headonly=False)
        print(stream)
        
        # Iterate through traces and print some metadata
        for trace in stream.traces:
            print(f"Trace {trace.stats.trace_number}: {trace.stats}")

        return stream
    except Exception as e:
        print(f"Error reading SEG-D file: {e}")
        return None

# Example usage
segdpath = data_dir+'/453005483.0001.2024.10.29.22.48.00.000.E.segd'
endianflag = '<' # big endian
stream = read_segd(segdpath,endianness=endianflag)

if stream:
    print("Successfully read the SEG-D file.")
else:
    print("Failed to read the SEG-D file.")
    
