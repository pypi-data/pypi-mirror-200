from __future__ import print_function
from __future__ import print_function
import sys
import numpy as np

import matplotlib.pyplot as pl

# from mpi4py import MPI


def get_beam_width_deg(freq):
    wavelength = 3E8/(freq*1E6) # Assume frequency given in MHz
    return (wavelength/12.0)*180.0/np.pi


def get_slope(sigma,x):
    slope = ((x/(sigma**2)) * np.exp((-1.0*x*x)/(2.0*sigma*sigma)))
    return slope


def get_slope_at_fwhm(fwhm):
    sigma = fwhm/2.35482
    return get_slope(sigma,fwhm/2.0)


def evalModel(coeff,points):
    data = []
    for p in points:
        total = 0.0
        for i in range(len(coeff)):
            total += coeff[i]*np.power(p,len(coeff)-i-1)
        data.append(total)
    return data


def get_maxima(coeff):
    if len(coeff) != 3:
        raise ValueError("get_maxima only works for quadratic models")
    return ((-1.0*coeff[1]) / (2.0*coeff[0]))


def find_data_on_disk(file, antInd, feed):
    amplitudes = []
    count = 0
    f = open(file, 'r')
    for line in f:
        myfields = line.split()
        if len(myfields) < 8:
            continue
        if myfields[7] != "result:":
            continue
        if int(myfields[10]) == feed:
            count += 1
            amplitudes.append(float(myfields[(13+(antInd*2))]))

    f.close()
    if count == 0:
        return RuntimeError("No valid data found.")
    else:
        return amplitudes


if len(sys.argv) <= 1:
    print("Usage: python point_opcal.py filename.opcal")
    exit()

fna = sys.argv[1]
#sna = (((fna.split('.'))[0]).split('_'))[2]

#################################################################

offsl = [[-0.75,0.0],[-0.5,0.0],[-0.25,0.0],[0.0,0.0],[0.25,0.0],[0.5,0.0],[0.75,0.0],[0.0,-0.75],[0.0,-0.5],[0.0,-0.25],[0.0,0.0],[0.0,0.25],[0.0,0.5],[0.0,0.75]]
rolll = [-120.0,0.0,120.0]

bm = 0  # beam

# This is the list of antennas defined in the MS. Don't change.
array = range(1,37)

# This is the list of antennas you are interested in.
active = [27]
#active = [1,2,3,4,5,6,8,10,11,12,13,14,15,16,17,18,19,24,25,26,27,28,30,31,32,33,34,36]
#active = [1]

plotMe = False

#################################################################

f = open("offsets.txt","w")

threshold = 10.0

for ant in active:
    print("Processing Antenna ak%02d" % (ant))
    badAntenna = False

    ElOffsets = []
    AzOffsets = []

    if plotMe:
        pl.figure(figsize=(20,20))

    powers = find_data_on_disk(fna,array.index(ant),bm)
    powers = 10.0*np.log10(powers)
    oi = 0

    for j in range(len(rolll)):
        if badAntenna:
            break
        AzP = []
        AzO = []
        ElP = []
        ElO = []

        for i in range(len(offsl)):
            if powers[oi] < -5.0:
                oi += 1
                continue
            if i < len(offsl)/2:
                AzO.append(offsl[i][0])
                AzP.append(powers[oi])
            else:
                ElO.append(offsl[i][1])
                ElP.append(powers[oi])

            oi += 1

        if len(ElP) > 3 and len(AzP) > 3:

            ElC, residuals, rank, singular_values, rcond = np.polyfit(ElO,ElP,2,full=True)
            print (residuals)
            if float(residuals[0]) > threshold:
                badAntenna = True
                break
            AzC, residuals, rank, singular_values, rcond = np.polyfit(AzO,AzP,2,full=True)
            print (residuals)
            if float(residuals[0]) > threshold:
                badAntenna = True
                break

            ModRange = np.arange(AzO[0],AzO[-1],0.01)

            ElM = evalModel(ElC,ModRange)
            AzM = evalModel(AzC,ModRange)

            if plotMe:
                pl.subplot(2,len(rolll),j+1)
                pl.xlim(-1.0,1.0)
                pl.title("Roll Angle %.1f" %rolll[j])
                pl.xlabel("Elevation Offset (deg)")
                if j == 0:
                    pl.ylabel("Power (dB)")
                pl.plot(ElO,ElP,"r+")
                pl.plot(ModRange,ElM,"r")
                pl.subplot(2,len(rolll),(len(rolll))+j+1)
                pl.xlim(-1.0,1.0)
                pl.xlabel("Azimuth Offset (deg)")
                if j == 0:
                    pl.ylabel("Power (dB)")
                pl.plot(AzO,AzP,"bx")
                pl.plot(ModRange,AzM,"b")

            ElPeak = get_maxima(ElC)
            ElOffsets.append(ElPeak)
            AzPeak = get_maxima(AzC)
            AzOffsets.append(AzPeak)

            print ("Elevation offset for roll angle %f = %9.6f" % (rolll[j], ElPeak))
            print ("Azimuth offset for roll angle %f = %9.6f" % (rolll[j], AzPeak))
        else:
            print ("Too few valid offset measurements found")
            badAntenna = True

    if not badAntenna:
        ElResult = np.mean(ElOffsets)
        AzResult = np.mean(AzOffsets)

        if plotMe:
            pl.show()

        if plotMe:
            pl.figure(figsize=(20,20))
            pl.plot(AzOffsets,ElOffsets,"o")
            pl.ylabel("Elevation Offset (deg)")
            pl.ylim(-0.7,0.7)
            pl.xlabel("Azimuth Offset (deg)")
            pl.xlim(-0.7,0.7)
            pl.plot(AzResult,ElResult,"d")
            pl.plot([-0.7,0.7],[0.0,0.0],"r--")
            pl.plot([0.0,0.0],[-0.7,0.7],"r--")
            pl.show()

        print ("Average elevation offset = %9.6f" % (ElResult))
        print ("Average azimuth offset = %9.6f" % (AzResult))

        f.write("common.antenna.ant%d.pointing_parameters = [0.0, %f, 0.0, 0.0, 0.0, %f, 0.0, 0.0, 0.0]\n"
                % (ant, AzResult, ElResult))
    else:
        print ("Rejecting antenna due to bad fit")
f.close()
