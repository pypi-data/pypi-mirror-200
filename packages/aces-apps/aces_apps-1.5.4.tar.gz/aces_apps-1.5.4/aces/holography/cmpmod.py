"""
File cmpmod.py

Defines the class ComponentModel that reads, writes and generates model visibilities
for difmap component models.

10 March 2016
"""

__author__ = 'Emil Lenc <emil.lenc@csiro.au>'

import numpy as np
import logging as log

C = 299792458                   # Speed of light in m/s
DEG2RAD = np.pi / 180.0         # Conversion factor from degrees to radians
RAD2DEG = 180.0 / np.pi         # Conversion factor from radians to degrees
MAS2RAD = DEG2RAD / 3600000.0   # Conversion factor from milli-arcseconds to radians
RAD2MAS = 3600000.0 / DEG2RAD   # Conversion factor from radians to milli-arcseconds

# Model component types defined within difmap
M_DELT = 0                      # Delta component
M_GAUS = 1                      # Gaussian component
M_DISK = 2                      # Disk component
M_ELLI = 3                      # Elliptical component
M_RING = 4                      # Ring component
M_RECT = 5                      # Rectangular component
M_SZ   = 6                      # Sunyaev-Zel'dovich component

# Mask for variable parameters within a difmap model (used during fitting)
M_FLUX   = 1                    # Flux can be varied
M_CENT   = 2                    # Position can be varied
M_MAJOR  = 4                    # Major axis can be varied
M_RATIO  = 8                    # Ratio between major and minor axis can be varied
M_PHI    = 16                   # Rotation angle of major axis can be varied
M_SPCIND = 32                   # Spectral index can be varied

# Structure to hold model component parameters
class MComponent(object):
    def __init__(self, mtype, flux, x, y, major, ratio, phi, freq0, spcind, vpar):
        self.mtype = mtype      # Component type
        self.flux = flux        # Flux of componet
        self.x = x              # x position of component
        self.y = y              # y position of component
        self.major = major      # major axis of component
        self.ratio = ratio      # ratio of major and minor axis
        self.phi = phi          # rotation angle of major axis
        self.freq0 = freq0      # reference frequency
        self.spcind = spcind    # spectral index of component
        self.vpar = vpar        # variable parameter mask

# Class to hold model components. Methods provide basic access functionality.
class ComponentModel:
    def __init__(self):
        self.list = []

    def add(self, component):
        # Add a component model (type MComponent) to the overall model
        self.list.append(component)

    def read(self, file):
        # Read a complete model from a difmap model file.
        # file specifies the file name for the difmap model to read.
        fin = open(file, "r")       # Open the difmap model file
        for line in fin:            # Read line by line
            data = line.split()
            if data[0] == "!":      # Skip if reading the header information
                continue
            mtype = M_DELT          # Assume a delta component unless explicitly specified
            if len(data) > 6:
                mtype = int(data[6])
            if mtype == M_DELT and len(data) < 3:
                continue
            if mtype != M_DELT and len(data) != 9:
                continue
            vpar = 0                # Reset the mask that records variable parameters
            dv = []
            for d in data:          # Make a list to record the presence (or not) of the variable flag
                dv.append(d.find('v'))
                    
            # Extract the flux
            if dv[0] != -1:
                flux = float(data[0][:dv[0]])
                vpar |= M_FLUX
            else:
                flux = float(data[0])
                
            # Extract the position
            if dv[1] != -1:
                radius = float(data[1][:dv[1]])
                vpar |= M_CENT
            else:
                radius = float(data[1])
            radius *= MAS2RAD
            
            if dv[2] != -1:
                theta = float(data[2][:dv[2]])
                vpar |= M_CENT
            else:
                theta = float(data[2])
            theta *= DEG2RAD
            # Convert from polar to cartesian coordinates
            x = radius * np.sin(theta)
            y = radius * np.cos(theta)

            major = 0.0
            ratio = 1.0
            phi = 0.0
            if mtype != M_DELT:
                # Extract the major axis
                if dv[3] != -1:
                    vpar |= M_MAJOR
                    major = float(data[3][:dv[3]])
                else:
                    major = float(data[3])
                major *= MAS2RAD

                # Extract the ratio
                if dv[4] != -1:
                    vpar |= M_RATIO
                    ratio = float(data[4][:dv[4]])
                else:
                    ratio = float(data[4])

                # Extract the ratio
                if dv[5] != -1:
                    vpar |= M_PHI
                    phi = float(data[5][:dv[5]])
                else:
                    phi = float(data[5])
                phi *= DEG2RAD

            # Extract the frequency and spectral index
            if dv[7] != -1:
                vpar |= M_SPCIND
                freq0 = float(data[7][:dv[7]])
            else:
                freq0 = float(data[7])
            if dv[8] != -1:
                vpar |= M_SPCIND
                spcind = float(data[8][:dv[8]])
            else:
                spcind = float(data[8])
            assert(mtype <= M_SZ), "Unknown component type specified: %d" %(mtype)
            self.list.append(MComponent(mtype, flux, x, y, major, ratio, phi, freq0, spcind, vpar))
        fin.close()

    def dump(self):
        # Dump the model contents to stdout
        pname = [ " ", "v" ]
        print("! Flux (Jy) Radius (mas)  Theta (deg)  Major (mas)  Axial ratio   Phi (deg) T  Freq (Hz)     SpecIndex")
        for mod in self.list:
             # Convert component X,Y position to polar representation.
            radius = 0.0
            theta = 0.0
            line = ""
            if mod.x != 0.0 or mod.y != 0.0:
                radius = RAD2MAS * np.sqrt(mod.x * mod.x + mod.y * mod.y);
                theta  = RAD2DEG * np.arctan2(mod.x, mod.y);

            if mod.vpar & M_FLUX == M_FLUX:
                line += "%#10.6gv" %(mod.flux)
            else:
                line += "%#10.6g " %(mod.flux)
            if mod.vpar & M_CENT == M_CENT:
                line += " %#11.6gv %#11.6gv" %(radius, theta)
            else:
                line += " %#11.6g  %#11.6g " %(radius, theta)
            if (mod.mtype != M_DELT) or (mod.freq0 > 0.0):
                if mod.vpar & M_MAJOR == M_MAJOR:
                    line += " %#11.6gv" %(mod.major * RAD2MAS)
                else:
                    line += " %#11.6g " %(mod.major * RAD2MAS)
                if mod.vpar & M_RATIO == M_RATIO:
                    line += " %#11.6gv" %(mod.ratio)
                else:
                    line += " %#11.6g " %(mod.ratio)
                if mod.vpar & M_PHI == M_PHI:
                    line += " %#10.6gv" %(mod.phi * RAD2DEG)
                else:
                    line += " %#10.6g " %(mod.phi * RAD2DEG)
                line +=" %d" %(mod.mtype)
                if mod.freq0 > 0.0:
                    line += " %#11.6g" %(mod.freq0)
                    if mod.vpar & M_SPCIND == M_SPCIND:
                        line += " %11.6gv" %(mod.spcind)
                    else:
                        line += " %11.6g " %(mod.spcind)

            print(line)
        return 0

    def write(self, file):
        # Write the model to a file using the difmap model format.
        pname = [ " ", "v" ]
        fout = open(file, "w")
        fout.write("! Flux (Jy) Radius (mas)  Theta (deg)  Major (mas)  Axial ratio   Phi (deg) T  Freq (Hz)     SpecIndex\n")
        for mod in self.list:
             # Convert component X,Y position to polar representation.
            radius = 0.0
            theta = 0.0
            if mod.x != 0.0 or mod.y != 0.0:
                radius = RAD2MAS * np.sqrt(mod.x * mod.x + mod.y * mod.y);
                theta  = RAD2DEG * np.arctan2(mod.x, mod.y)

            if mod.vpar & M_FLUX == M_FLUX:
                fout.write("%#10.6gv" %(mod.flux))
            else:
                fout.write("%#10.6g " %(mod.flux))
            if mod.vpar & M_CENT == M_CENT:
                fout.write(" %#11.6gv %#11.6gv" %(radius, theta))
            else:
                fout.write(" %#11.6g  %#11.6g " %(radius, theta))
            if (mod.mtype != M_DELT) or (mod.freq0 > 0.0):
                if mod.vpar & M_MAJOR == M_MAJOR:
                    fout.write(" %#11.6gv" %(mod.major * RAD2MAS))
                else:
                    fout.write(" %#11.6g " %(mod.major * RAD2MAS))
                if mod.vpar & M_RATIO == M_RATIO:
                    fout.write(" %#11.6gv" %(mod.ratio))
                else:
                    fout.write(" %#11.6g " %(mod.ratio))
                if mod.vpar & M_PHI == M_PHI:
                    fout.write(" %#10.6gv" %(mod.phi * RAD2DEG))
                else:
                    fout.write(" %#10.6g " %(mod.phi * RAD2DEG))
                fout.write(" %d" %(mod.mtype));
                if mod.freq0 > 0.0:
                    fout.write(" %#11.6g" %(mod.freq0))
                    if mod.vpar & M_SPCIND == M_SPCIND:
                        fout.write(" %11.6gv" %(mod.spcind))
                    else:
                        fout.write(" %11.6g " %(mod.spcind))
            fout.write("\n")
        fout.close()
        return 0

    def getmodvis(self, uvw, freq):
        # Generate visibilities based on the current model from the specified uvw coordinates
        # and at the specified frequency.
        # uvw is a N x 3 array with N sets of (U, V, W) coordinates
        # freq is the frequency at which to generate the visibilities (in Hz)
        
        uu = uvw[:,0] / C * freq # Visibility U in wavelengths
        vv = uvw[:,1] / C * freq # Visibility V in wavelengths
        
        # Reset the generated complex visibilities
        mod_vis = np.zeros(uu.shape, dtype=np.complex64)
        # Loop through the components of the variable model.
        for mod in self.list:
            # Since all model component types are even functions, the only
            # contribution to the model visibility phase is from the centroid
            # position of the component.
            cmpphs = 2.0 * np.pi * (uu * mod.x + vv * mod.y) # Component phase
            # Pre-compute useful constants.
            sinphi = np.sin(mod.phi)
            cosphi = np.cos(mod.phi)
            # Compute the elliptically stretched UV radius (also scaled by pi * major
            # axis for convenience).
            tmpa = (uu * cosphi - vv * sinphi) * mod.ratio
            tmpb = (uu * sinphi + vv * cosphi)
            uvrad = np.pi * mod.major * np.sqrt(tmpa * tmpa + tmpb * tmpb)
            # Get the spectral-index scale factor.
            si = 1.0
            if mod.spcind != 0.0:
                si = (freq / mod.freq0) ** mod.spcind
    
            # Get the potentially frequency dependent flux of the component.
            flux = mod.flux * si

            # Compute model-component visibility amplitude.
            if mod.mtype == M_DELT:
                cmpamp = flux;
            elif mod.mtype == M_GAUS:
                cmpamp = flux * np.exp(-0.3606737602 * uvrad * uvrad)
            elif mod.mtype == M_ELLI:
                cmpamp = 3.0 * flux * (np.sin(uvrad) - uvrad * np.cos(uvrad)) / np.power(uvrad, 3.0)
            else:
                log.error(("Unknown model component type: %d" %(mod.mtype)))
                return None, None

            # Compute the real and imaginary parts of the model-component
            # visibility and add to the overall model visibility.
            mod_vis += cmpamp * (np.cos(cmpphs) + 1.0j * np.sin(cmpphs))

        # return the cumulative complex model visibilities
        return mod_vis

    def dump_ccal(self, freq):
        srclist = []
        print("sources.names = field1")
        ra_hms = self.center.ra.hms
        dec_dms = self.center.dec.dms
        if np.sign(self.center.dec) == 1:
            sign = "+"
        else:
            sign = "-"
        ra_hms_str = f"{ra_hms.h:0.0f}h{ra_hms.m:0.0f}m{ra_hms.s:0.4f}"
        dec_dms_str = f"{sign}{dec_dms.d:0.0f}.{dec_dms.m:0.0f}.{dec_dms.s:0.3f}"
        print(f"sources.field1.direction = [{ra_hms_str}, {dec_dms_str}, J2000]")
        for i, mod in enumerate(self.list):
            sinphi = np.sin(mod.phi)
            cosphi = np.cos(mod.phi)
            # Get the spectral-index scale factor.
            si = 1.0
            if mod.spcind != 0.0:
                si = (freq / mod.freq0) ** mod.spcind

            # Get the potentially frequency dependent flux of the component.
            flux = mod.flux * si
            name = f"src{i+1}"
            srclist += [name]
            print(f"sources.{name}.flux.i = {flux}")
            print(f"sources.{name}.direction.ra = {mod.x}")
            print(f"sources.{name}.direction.dec = {mod.y}")
            print(f"sources.{name}.shape.bmaj = {mod.major}")
            print(f"sources.{name}.shape.bmin = {mod.major*mod.ratio}")
            print(f"sources.{name}.shape.bpa = {mod.phi}")
        print('sources.field1.components = [%s]' % ', '.join(map(str, srclist)))
        return 0
    
    def write_ccal(self, freq, file):
        fout = open(file, "w")
        srclist = []
        fout.write("sources.names = field1 \n")
        ra_hms = self.center.ra.hms
        dec_dms = self.center.dec.dms
        if np.sign(self.center.dec) == 1:
            sign = "+"
        else:
            sign = "-"
        ra_hms_str = f"{ra_hms.h:0.0f}h{ra_hms.m:0.0f}m{ra_hms.s:0.4f}"
        dec_dms_str = f"{sign}{dec_dms.d:0.0f}.{dec_dms.m:0.0f}.{dec_dms.s:0.3f}"
        fout.write(f"sources.field1.direction = [{ra_hms_str}, {dec_dms_str}, J2000] \n")
        for i, mod in enumerate(self.list):
            sinphi = np.sin(mod.phi)
            cosphi = np.cos(mod.phi)
            # Get the spectral-index scale factor.
            si = 1.0
            if mod.spcind != 0.0:
                si = (freq / mod.freq0) ** mod.spcind

            # Get the potentially frequency dependent flux of the component.
            flux = mod.flux * si
            name = f"src{i+1}"
            srclist += [name]
            fout.write(f"sources.{name}.flux.i = {flux*10} \n")
            fout.write(f"sources.{name}.direction.ra = {mod.x} \n")
            fout.write(f"sources.{name}.direction.dec = {mod.y} \n")
            fout.write(f"sources.{name}.shape.bmaj = {mod.major} \n")
            fout.write(f"sources.{name}.shape.bmin = {mod.major*mod.ratio} \n")
            fout.write(f"sources.{name}.shape.bpa = {mod.phi} \n")
        fout.write('sources.field1.components = [%s] \n' % ', '.join(map(str, srclist)))
        fout.close()
        return 0
