#!/usr/bin/env python
import sys
from obspy.core import read, UTCDateTime
from matplotlib.pyplot import (figure,axes,plot,xlabel,ylabel,title,subplot,legend,savefig,xlim)
import numpy as np
debug = True
# If you want DIS, VEL, or ACC
groundunits = 'VEL'
#Prefilter corners 
fl1 = 1
fl2 = 1
fl3 = 5
fl4 = 5
#Start time
t1 = UTCDateTime('2011-03-11T05:46:00.000')+ 700
#End time
t2 = t1 + 800

#Get command line arguments
if len(sys.argv) != 2:
	print 'Purpose: Deconvolve mseed file'
	print 'Usage: mseed'
	sys.exit(0)

#Read in miniseed
try:
	if debug:
		print 'Seed file: ' + sys.argv[1]
	st = read(sys.argv[1],starttime=t1,endtime=t2)
except:
	print 'Can not read mseed file'
	sys.exit(0)


for tr in st:
#Make a copy of the trace
	trdec = tr.copy()
	trdec.detrend()
#Find the response file name
	respname = 'RESP.' + trdec.stats.network + '.' + trdec.stats.station + \
		'.' + trdec.stats.location + '.' + trdec.stats.channel
	if debug:
		print 'Resp name: ' + respname	
#Make an obspy handle to deal with the response
	resphand = {'filename': respname,'date': t1,'units': groundunits}
#Remove the response using a prefilter
	trdec.simulate(paz_remove = None, prefilt=(fl1,fl2,fl3,fl4), seedresp=resphand,taper='True')
#Throw in a post bandpass filter
	trdec.filter("bandpass",freqmin = fl1,freqmax=fl3,corners = 4)
#Remove any hanging on trends
	trdec.detrend()
#Plot the results and save them
	t = np.arange(0, trdec.stats.npts / trdec.stats.sampling_rate, trdec.stats.delta)
	synplot = figure(1)
	subplot(211)
	p1=plot(t,trdec.data*1000, 'k')
#Remember to change this if you change the units
	ylabel(groundunits + ' (mm/s)')
	title(trdec.stats.station + ' ' + trdec.stats.location + ' ' + trdec.stats.channel + ': ' + str(t1))
	xlim(min(t),max(t))
	subplot(212)
	p1=plot(t,tr.data/1000, 'k')
	xlim(min(t),max(t))
	xlabel('Time (s)')
	title(trdec.stats.channel + ': ' + str(t1))
	ylabel('kCounts')
	savefig(trdec.stats.network + trdec.stats.station + trdec.stats.location + \
		trdec.stats.channel + 'decon.jpg',format = 'jpeg',dpi=200)



