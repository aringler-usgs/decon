#!/usr/bin/env python
from obspy.core import read 
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt
import scipy.optimize.minpack as solv
import matplotlib.mlab as mlab
import math
import numpy as np
from numpy import *
import matplotlib.mlab
from obspy.signal import psd
from obspy.signal.invsim import evalresp 
from obspy.signal.invsim import pazToFreqResp

st = read("DEC01.CNZ.GS.01.mseed")
tr1=st[0]
st = read('DEC01.DP1.GS.02.mseed')
tr2 = st[0]


lnfft=1024
nol=256


#Read the resp
resp1,fg=evalresp(0.002,lnfft,"RESP.GS.DEC01..CNZ", tr1.stats.starttime, station="DEC01", channel="CNZ", network="GS", units='ACC', freq=True, debug=False)
resp1=np.absolute(resp1[1:]*np.conjugate(resp1[1:]))
fg=fg[1:]
resp2=evalresp(0.002,lnfft,"RESP.GS.DEC01..DP1", tr2.stats.starttime, station="DEC01", channel="DP1", network="GS", units='ACC', freq=False, debug=False)
resp2=np.absolute(resp2[1:]*np.conjugate(resp2[1:]))



#Estimate The Spectra
(pspec1, fre1) = matplotlib.mlab.psd(tr1.data, NFFT=lnfft, Fs=500, noverlap=nol)
fre1=fre1[1:]
pspec1=pspec1[1:]/resp1
(pspec2, fre2) = matplotlib.mlab.psd(tr2.data, NFFT=lnfft, Fs=500, noverlap=nol)
fre2=fre2[1:]
pspec2=pspec2[1:]/resp2


p1=plt.semilogx(fre1, 10*np.log10(pspec1), 'k')
p2=plt.semilogx(fre1, 10*np.log10(pspec2), 'r')
plt.title('Spectra: ')
plt.ylabel('PSD')
plt.xlabel('Frequency (Hz)')
plt.xlim(1,250)
plt.title('Spectra DEC01 GS')
plt.legend((p1[0],p2[0]),('CNZ','DP1'))
plt.savefig('Spectra.pdf', orientation='landscape')
plt.show()



