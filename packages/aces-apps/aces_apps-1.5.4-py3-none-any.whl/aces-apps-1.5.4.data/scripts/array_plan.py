from __future__ import print_function
import numpy as np
import matplotlib.pyplot as pl

# Load Eastings and Northings
config = range(1,37)

positions = []

f = open("antenna-positions.txt")
for line in f:
    positions.append([float(line.split()[0]),float(line.split()[1])])

relx = [0.0]
rely = [0.0]
for ant in config[1:]:
    relx.append(positions[ant-1][0] - positions[config[0]-1][0])
    rely.append(positions[ant-1][1] - positions[config[0]-1][1])

baselines = []

for ant1 in config:
    for ant2 in config:
        if ant1 == ant2: 
            continue
        dx = positions[ant1-1][0] - positions[ant2-1][0]
        dy = positions[ant1-1][1] - positions[ant2-1][1]
        baselines.append(np.sqrt(dx**2+dy**2))
print("Shortest Baseline = %f" % (min(baselines)))
print ("Longest Baseline = %f" % (max(baselines)))

pl.clf()
pl.xlim(min(relx)-np.fabs(min(relx)/5.0),max(relx)+np.fabs(max(relx)/5.0))
pl.ylim(min(rely)-np.fabs(min(rely)/5.0),max(rely)+np.fabs(max(rely)/5.0))
for i in range(len(relx)):
    pl.plot([0.0,relx[i]],[0.0,rely[i]],'-',color='grey',linewidth=2.0,alpha=0.5)
    pl.annotate(" ak%02d" %config[i],xy=[relx[i],rely[i]])
    if (np.sqrt(relx[i]**2+rely[i]**2)>150.0):
        pl.annotate(" %.1f m" %(np.sqrt(relx[i]**2+rely[i]**2)), xy=[relx[i]/2.0,rely[i]/2.0])
pl.plot(relx, rely, '.', markersize=12)
pl.grid(True)
pl.title("Array configuration map")
pl.xlabel("Eastern distance from ak%02d (m)" %config[0])
pl.ylabel("Northern distance from ak%02d (m)" %config[0])
pl.show()
