#!/usr/bin/env python
from obspy.core import read
from matplotlib.pyplot import (figure,axes,plot,xlabel,ylabel,title,subplot,legend,savefig,xlim)
import numpy as np
import sys

sacfile = '20130916103655/DEC04.HHZ.GS.01'
groundunits = 'VEL'

#Read in one example and treat it as a trace
st = read(sacfile)
tr = st[0]

#Check the response file that was made up
respname = 'RESP.' + tr.stats.network + '.' + tr.stats.station + \
	'..' + tr.stats.channel

resphand = {'filename': respname,'date': tr.stats.starttime,'units': groundunits}

#Lets detrend and remove the response using evalresp
tr.detrend()
trdecresp = tr.copy()
trdecresp.simulate(paz_remove = None, seedresp=resphand, taper=True)


#Lets use Joerns response.  Notice I removed the extra 0.  This is likely a SAC default
#Normally SAC likes to deconvolve to displacement
dec_hh_paz = {'poles':[
     (-3.6910e-2 + 3.7120e-2j),
     (-3.6910e-2 + -3.7120e-2j),
     (-3.7120e2 + 0.0j),
     (-3.7390e2 +  4.7550e2j),
     (-3.7390e2 + -4.7550e2j),
     (-5.8840e2 +  1.5080e3j),
     (-5.8840e2 + -1.5080e3j)],
    'zeros':[
      ( 0.0 + 0.0j),
      ( 0.0 +  0.0j),
      (-4.341e2 + 0.0j) ],
    'gain':   8.1984e11, # A0-normalization from IRIS DMC
    'sensitivity': 4.712805339e8}# Overall sensitivity
trdecpaz = tr.copy()
trdecpaz.simulate(paz_remove = dec_hh_paz, taper = True)



#Lets do a back of the envelope comparison with no response and just the sensitivity
#In the mid-band of the instrument (20 Hz to 120 seconds period) this should roughly be the same
trremsen = tr.copy()
#Going from counts to vols
trremsen.data = trremsen.data/(629129.0)
#Going from volts to m/s
trremsen.data = trremsen.data/(749.1)




t = np.arange(0, trdecresp.stats.npts / trdecresp.stats.sampling_rate, trdecresp.stats.delta)
synplot = figure(1)
subplot(211)
p1=plot(t,trdecresp.data*1000, 'k',label='EvalRESP')
p2 = plot(t,trdecpaz.data*1000,'b:',label='Joerns RESP')
p3 = plot(t,trremsen.data*1000,'r',label='Mid-band')
legend(prop={'size':6})
#Remember to change this if you change the units
ylabel(groundunits + ' (mm/s)')
title(trdecresp.stats.station + ' ' + trdecresp.stats.location + ' ' + trdecresp.stats.channel + ': ' + str(tr.stats.starttime))
xlim(min(t),max(t))
subplot(212)
p1=plot(t,tr.data/1000, 'k')
xlim(min(t),max(t))
xlabel('Time (s)')
title(trdecresp.stats.channel + ': ' + str(tr.stats.starttime))
ylabel('kCounts')
savefig(trdecresp.stats.network + trdecresp.stats.station + trdecresp.stats.location + \
	trdecresp.stats.channel + 'decon.jpg',format = 'jpeg',dpi=200)



