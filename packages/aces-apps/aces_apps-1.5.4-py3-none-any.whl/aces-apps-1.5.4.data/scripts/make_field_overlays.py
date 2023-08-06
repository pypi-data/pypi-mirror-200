from __future__ import print_function
from astropy.io import ascii
import numpy as np
import sys
import string


def dec2deg(ra_hms,dec_dms):
    """
    DEC2DEG = converts hh:mm:ss.sss +/-dd:mm:ss.ssss to decimal degrees
    """
    # convertinf RA
    ra_hms = ra_hms.split(':')
    hh = abs(float(ra_hms[0]))
    mm = float(ra_hms[1])/60.
    ss = float(ra_hms[2])/3600.
    ra_deg = (hh+mm+ss)*15.
    # converting DEC
    dec_dms = dec_dms.split(':')
    hh = abs(float(dec_dms[0]))
    mm = float(dec_dms[1])/60.
    ss = float(dec_dms[2])/3600.
    dec_deg = hh + mm + ss
    if float(dec_dms[0]) < 0:
        dec_deg = -1.*dec_deg
    # returning position of RA and DEC in decimal degrees
    return [ra_deg,dec_deg]


def coord_deg(x,y):
    print(x, y)
    ra = string.split(x, ":")

    hh = abs(float(ra[0]))
    mm = float(ra[1])/60
    ss = float(ra[2])/3600

    ra_deg = (hh+mm+ss)/15.

    dec = string.split(y, ":")
    hh=abs(float(dec[0]))
    mm=float(dec[1])/60
    ss=float(dec[2])/3600
    if float(dec[0]) < 0:
        dec_deg = -hh+mm+ss
    else:
        dec_deg = hh+mm+ss
 
    return ra_deg,dec_deg


def main():
    racsfile = 'survey.csv'
    data = ascii.read(racsfile,format='csv')
    numfields = len(data['FIELD_NAME'])
    pitch = 1.05

    ii = 0
    while ii < numfields:
        annfile = data['FIELD_NAME'][ii] + '.ann'
        ds9file = data['FIELD_NAME'][ii] + '.reg'

        fout = open(annfile,'w+')
        fout.write('COORD W\n')
        fout.write('PA STANDARD\n')
        fout.write('COLOR YELLOW\n')

        fout2 = open(ds9file,'w+')

        jj = 0
        for jj in np.arange(0,36):
            ra_hms = data['RA_HMS'][ii + jj]
            dec_dms = data['DEC_DMS'][ii + jj]
            coords = dec2deg(ra_hms,dec_dms)
            # KVIS annotation file
            fout.write('CIRCLE {} {} {}\n'.format(coords[0],coords[1],pitch/2.))
            fout.write('TEXT {} {} {}\n'.format(coords[0],coords[1],jj))
            # DS9 Region fild
            fout2.write('icrs;circle({},{},{}) # color=yellow\n'.format(coords[0],coords[1],pitch/2.))
            fout2.write('icrs;text({},{}) # color=yellow text={}{}{}\n'.format(coords[0],coords[1],'{',jj,'}'))
        fout.close()
        fout2.close()
        
        ii = ii + 36
        
    
if __name__ == "__main__":
    sys.exit(main())
