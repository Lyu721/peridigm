#! /usr/bin/env python

import sys
import os
import string
from subprocess import Popen
from pylab import *

if __name__ == "__main__":

	executable = sys.argv[-1]
	base_name = string.splitfields(executable, '/')[-1]
	logfile = open(base_name + ".log", 'w')

	if not os.path.exists(executable):
		logfile.write("\nError:  " + executable + " not found!\n\n")
		sys.exit(1)

	command = []
	for i in range(len(sys.argv)-1):
		command.append(sys.argv[1+i])

	p = Popen(command, stdout=logfile, stderr=logfile)
	return_code = p.wait()
	if 0<return_code:
		logfile.write("\nExecution of unit test failed\n\n")
		sys.exit(1)
		
	# load computed and gold data
	d=loadtxt("ep.dat")
	dG=loadtxt("ep.gold.dat")
	if len(d) != len(dG):
		logfile.write("\nError: Files have different number of time steps!")
		sys.exit(1)
	
	# diff files
	logfile.write("\nDiffing Files ...")
	tMag=.02
	uMag=.005
	fMag=800
	tol=1.0e-15;
	for i in range(len(d)):
		dt=abs(d[i][0]-dG[i][0])
		du=abs(d[i][1]-dG[i][1])
		df=abs(d[i][2]-dG[i][2])
		if dt/tMag > tol or du/uMag > tol or df/fMag > tol:
			logfile.write("\nep.dat DIFFERs with ep.gold.dat\n\n")
			sys.exit(1)
			
	logfile.write("\nDiffing Files ...DONE")
	sys.exit(0)
