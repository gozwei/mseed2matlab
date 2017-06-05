from obspy.core import *
from obspy.geodetics import locations2degrees
from obspy.taup.taup import getTravelTimes
from optparse import OptionParser
from datetime import date, datetime, timedelta

import os
import sys
import time
import scipy.io
import numpy as np


def datetime2matlabdn(dt):
	mdn = dt + timedelta(days = 366)
	frac_seconds = (dt-datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
	frac_microseconds = dt.microsecond / (24.0 * 60.0 * 60.0 * 1000000.0)
	return mdn.toordinal() + frac_seconds + frac_microseconds


parser = OptionParser()
parser.add_option("-s", "--station", dest="station", type='string', help="Seismic station name")
parser.add_option("-S", "--station-meta", dest="station_meta", default='0,0,0', type='string', help="Seismic station location (latitude, longitude, elevation)")
parser.add_option("-t", "--start-time", dest="start_time_str", type='string', help="Trace start time (ex. '2015-02-13 18:30:00')")
parser.add_option("-d", "--duration", dest="duration", default=3600, type='int', help="Trace duration in seconds")
parser.add_option("-c", "--components", dest="components", default="ZNE", type='string', help="Trace components (ex. 'Z' or 'NE' or 'ZNE'...)")
parser.add_option("-i", "--input_file", dest="input", default="", type='string', help="Input mseed file")
parser.add_option("-f", "--filter", dest="filter", default="", type='string', help='filter type (ex. B,0.1,4 or L,0.1)')
parser.add_option("-e", "--event", dest="event", default="", type='string', help='event data: lat, lon, depth, time')
parser.add_option("-o", "--output_file", dest="output", default="output.mat", type='string', help="Location of temporary matlab data file")

(options, args) = parser.parse_args()



station = options.station
start_time_str = options.start_time_str
duration = options.duration
component = options.components
filter = options.filter
event = options.event
input = options.input

[lat, lon, ele] = options.station_meta.split(',')

start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
end_time = start_time + timedelta(seconds=int(duration))
ST = UTCDateTime(start_time_str)
ET = ST + int(duration)

S = Stream()
if input:
	if os.path.isfile(input):
			if os.stat(input).st_size > 0:
				S = S + read(input)
	S = S.select(station=station)

S._cleanup();
S.trim(ST-3600,ET+3600)


if filter:
	filter_params = filter.split(',')
	if filter_params[0] == "B":
		S.filter("bandpass", freqmin=float(filter_params[1]), freqmax=float(filter_params[2]), zerophase=True, corners=4)
	if filter_params[0] == "L":
		S.filter("lowpass", freq=float(filter_params[1]), zerophase=True, corners=4)
	if filter_params[0] == "H":
		S.filter("highpass", freq=float(filter_params[1]), zerophase=True, corners=4)


#S.filter("bandpass", freqmin=1., freqmax=4., zerophase=True)
S.trim(ST,ET)

S.merge(method=0, fill_value=-9999999999)

data = dict();
if "Z" in options.components:
	C = S.select(component="Z")
	print(C)
	Clist = []
	for a in C[0].data.tolist():
		if a > -9*10**9:
			Clist.append(float(a))
		else:
			Clist.append(float('NaN'))
	data['Z'] = Clist

if "N" in options.components:
	C = S.select(component="N")
	print(C)
	Clist = []
	for a in C[0].data.tolist():
		if a > -9*10**9:
			Clist.append(float(a))
		else:
			Clist.append(float('NaN'))
	data['N'] = Clist

if "E" in options.components:
	C = S.select(component="E")
	print(C)
	Clist = []
	for a in C[0].data.tolist():
		if a > -9*10**9:
			Clist.append(float(a))
		else:
			Clist.append(float('NaN'))
	data['E'] = Clist

R = dict()
R['time_start']=datetime2matlabdn(S[0].stats.starttime.datetime)
R['time_end']=datetime2matlabdn(S[0].stats.endtime.datetime)
R['sampling_rate'] = S[0].stats.sampling_rate;
R['station'] = S[0].stats.station;
R['latitude'] = lat
R['longitude'] = lon
R['elevation'] = ele
R['data'] = data

if event:
	event_params = event.split(',')
	distance = locations2degrees(float(event_params[0]), float(event_params[1]), lat, lon)
	tt = getTravelTimes(delta=distance, depth=float(event_params[0]))
	R['first_arrival'] = datetime2matlabdn(datetime.strptime(event_params[3], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=tt[0]['time']))
	
	
	
scipy.io.savemat(options.output, R)
print(S)
