#!/usr/bin/env python
from obspy.core import read
from matplotlib.pyplot import (figure,axes,plot,xlabel,ylabel,title,subplot,legend,savefig,xlim)
import numpy as np
import sys


fl1 = 25
fl2 = 25
fl3 = 30
fl4 = 30



sacfile1 = '20130916103655/DEC04.HHZ.GS.01'
sacfile2 = '20130916103655/DEC04.HNZ.GS.01'
groundunits = 'ACC'

#Read in one example and treat it as a trace
st1 = read(sacfile1)
st2 = read(sacfile2)
tr1 = st1[0]
tr2 = st2[0]


#Check the response file that was made up
respname1 = 'RESP.' + tr1.stats.network + '.' + tr1.stats.station + \
	'..' + tr1.stats.channel

resphand1 = {'filename': respname1,'date': tr1.stats.starttime,'units': groundunits}

respname2 = 'RESP.' + tr2.stats.network + '.' + tr2.stats.station + \
	'..' + tr2.stats.channel

resphand2 = {'filename': respname2,'date': tr2.stats.starttime,'units': groundunits}

#Lets detrend and remove the response using evalresp
tr1.detrend()
tr1 = tr1.copy()
tr1.simulate(paz_remove = None,  prefilt=(fl1,fl2,fl3,fl4), seedresp=resphand1, taper=True)
tr1.filter("bandpass",freqmin = fl1,freqmax=fl3,corners = 4)
tr2.detrend()
tr2 = tr2.copy()
tr2.simulate(paz_remove = None,  prefilt=(fl1,fl2,fl3,fl4), seedresp=resphand2, taper=True)
tr2.filter("bandpass",freqmin = fl1,freqmax=fl3,corners = 4)

resi = tr1.data*1000 - tr2.data*1000

t1 = np.arange(0, tr1.stats.npts / tr1.stats.sampling_rate, tr1.stats.delta)
t2 = np.arange(0, tr2.stats.npts / tr2.stats.sampling_rate, tr2.stats.delta)
synplot = figure(1)
p1=plot(t1,tr1.data*1000, 'k',label=tr1.stats.channel)
p2 = plot(t2,tr2.data*1000,'r:',label=tr2.stats.channel)
p3= plot(t1,resi,'b',label='Residual')
legend(prop={'size':6})
#Remember to change this if you change the units
ylabel(groundunits + ' (mm/s^2)')
title(tr1.stats.station + ' ' + tr1.stats.location + ' ' + tr1.stats.channel + ': ' + str(tr1.stats.starttime))
xlim(min(t1),max(t1))
xlabel('Time (s)')
savefig('deconBBLG.jpg',format = 'jpeg',dpi=200)



