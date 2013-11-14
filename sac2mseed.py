#!/usr/bin/env python
from obspy.core import read, Stream, UTCDateTime
import sys

#Get command line arguments
if len(sys.argv) != 2:
	print 'Purpose: Convert Sac to mseed'
	print 'Usage: sacfile'
	sys.exit(0)


try:
	datain = read(sys.argv[1])

except:
	print "Trouble reading mseed data"
	sys.exit(0)


datain[0].write(sys.argv[1] + '.mseed', format = "MSEED", encoding = 4, reclen = 512)
