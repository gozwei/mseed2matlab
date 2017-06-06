# `mseed2matlab`
Python script for easy mseed to MATLAB conversion

## Features

`mseed2matlab` allows convering parts of miniseed files into matlab data structures. Output can be filtered. Gaps are filled with `NaN`.

## dependencies

1. obspy [https://github.com/obspy/obspy/wiki]
2. optparse
3. datetime
4. scipy
5. numpy

## Usage
```
  -h, --help            show this help message and exit
  -s STATION, --station=STATION
                        Seismic station name
  -S STATION_META, --station-meta=STATION_META
                        Seismic station location (latitude, longitude,
                        elevation)
  -t START_TIME_STR, --start-time=START_TIME_STR
                        Trace start time (ex. '2015-02-13 18:30:00')
  -d DURATION, --duration=DURATION
                        Trace duration in seconds
  -c COMPONENTS, --components=COMPONENTS
                        Trace components (ex. 'Z' or 'NE' or 'ZNE'...)
  -i INPUT, --input_file=INPUT
                        Input mseed file
  -f FILTER, --filter=FILTER
                        filter type (ex. B,0.1,4 or L,0.1)
  -e EVENT, --event=EVENT
                        event data: lat, lon, depth, time
  -o TMPFILE, --output_file=TMPFILE
```

## Example

```python3.5 mseed2matlab.py -s SUW -t '2015-04-22 13:55:00' -d 900 -c Z -i '2015112.mseed' -o SUW_bandpass.mat -f 'B,0.1,4'
python3.5 mseed2matlab.py -s SUW -t '2015-04-22 13:55:00' -d 900 -c Z -i '2015112.mseed' -o SUW_highpass.mat -f 'H,2.5'
python3.5 mseed2matlab.py -s SUW -t '2015-04-22 13:55:00' -d 900 -c Z -i '2015112.mseed' -o SUW_lowpass.mat -f 'L,0.1'
```

Reading output in MATLAB:

```
>> load('SUW_highpass.mat')
>> whos
  Name               Size            Bytes  Class     Attributes

  data               1x1             48184  struct              
  elevation          1x1                 8  double              
  first_arrival      1x1                 8  double              
  latitude           1x1                 8  double              
  longitude          1x1                 8  double              
  sampling_rate      1x1                 8  double              
  station            1x4                 8  char                
  time_end           1x1                 8  double              
  time_start         1x1                 8  double              

>> D = data.Z;
>> T = linspace(time_start, time_end, length(data.Z));
>> plot(T,D)
```
