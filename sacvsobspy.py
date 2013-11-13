#!/usr/bin/env python
import subprocess, os, time
from obspy.core import read
from matplotlib.pyplot import (figure,axes,plot,xlabel,ylabel,title,subplot,legend,savefig,xlim)
import numpy as np


debug = True
f1=str(10)
f2=str(20)
groundunits = 'ACC'

sacfile = '20130916103655/DEC04.HHZ.GS.01'
sacpz= 'dec05_HH_paz_sac'
#Open up sac and deconvolve
p = subprocess.Popen(['sac'], stdout = subprocess.PIPE, \
	stdin = subprocess.PIPE, stderr = subprocess.STDOUT)
p.stdin.write('r ' + sacfile + '\n')
p.stdin.write('rmean \n')
p.stdin.write('trans from polezero s ./' + sacpz + ' to none freqlimits ' + f1 + \
' ' + f1 + ' ' + f2 + ' ' + f2 + ' \n')
p.stdin.write('w tempsacfile \n')
p.stdin.write('quit \n')
p.communicate()
#Read in one example and treat it as a trace
st = read(sacfile)
tr = st[0]
time.sleep(5)
#Read in our deconvolved SAC trace
st2 = read('tempsacfile')
trsac = st2[0]
os.system('rm tempsacfile')

#Check the response file that was made up
respname = 'RESP.' + tr.stats.network + '.' + tr.stats.station + \
	'..' + tr.stats.channel

resphand = {'filename': respname,'date': tr.stats.starttime,'units': groundunits}

#Lets detrend and remove the response using evalresp
tr.detrend()
trdecresp = tr.copy()
trdecresp.simulate(paz_remove = None, prefilt=(int(f1),int(f1),int(f2),int(f2)),seedresp=resphand, taper=True)
#Convert to the same units of mm/s^2
resi = trdecresp.data*1000 - trsac.data/(10**6)
t = np.arange(0, trdecresp.stats.npts / trdecresp.stats.sampling_rate, trdecresp.stats.delta)
synplot = figure(1)
p1=plot(t,trdecresp.data*1000, 'k',label='EvalRESP')
p2 = plot(t,trsac.data/(10**6),'b:',label='SAC')
p3 = plot(t,resi,'r',label='Resi')
legend(prop={'size':6})
#Remember to change this if you change the units
ylabel(groundunits + ' (mm/s^2)')
title(trdecresp.stats.station + ' ' + trdecresp.stats.location + ' ' + trdecresp.stats.channel + ': ' + str(tr.stats.starttime))
xlim(min(t),max(t))
xlabel('Time (s)')
savefig(trdecresp.stats.network + trdecresp.stats.station + trdecresp.stats.location + \
	trdecresp.stats.channel + 'SACCOMP.jpg',format = 'jpeg',dpi=200)
