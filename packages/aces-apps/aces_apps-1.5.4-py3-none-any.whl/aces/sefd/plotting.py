"""Tooling to support the plotting of SEFD figures
"""
import logging
from typing import Any

import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from aces import obsplan

logger = logging.getLogger(__name__)

def fitfunc2(p, x):
    return p[0] * np.exp(-((x - p[1]) / p[2]) ** 2)


def linfunc(p, x):
    return p[0] + p[1] * x


def fit_gauss(x: np.ndarray, y: np.ndarray, p0: list[float], fkey: str='gau') -> tuple[tuple[float,...], float, float, float]:
    """Given the bin centers and counts for data that has been binned, an 
    attempt to fit a gaussian to said binned data will be performed.

    Args:
        x (np.ndarray): The bin centers of the binned data
        y (np.ndarray): The bin counts per bins of the binned data
        p0 (list[float]): Initial guess parameters of the desired model to fit
        fkey (str, optional): Model to fit to the data. Defaults to 'gau'.

    Raises:
        ValueError: Raised when an unkown key / fit function is suppliede

    Returns:
        tuple[tuple[float,...], float, float, float]: Contains the best fit parameters, the x and y of the model evaluated with best fit parameters, and the reduced chi2
    """
    
    fit_funcs = dict(
        lin=linfunc,
        gau=fitfunc2
    )
    if fkey not in fit_funcs.keys():
        raise ValueError(f"Unkown fitting moe {fkey=}, acceptable modes are {fit_funcs.keys()}")
    
    func = fit_funcs[fkey]
    err_func = lambda p, x, y: func(p, x) - y 
    
    xx = np.array(x)
    yy = np.array(y)
    
    (p1, *_) = scipy.optimize.leastsq(err_func, p0, args=(xx, yy))
    
    xf = np.linspace(min(xx), max(xx), 100)
    yf = func(p1, xf)
    
    res = np.sum(
        err_func(p1, xx, yy) ** 2
    ) / (len(xx) - len(p1))
    
    return p1, xf, yf, res

def find_mode(data: np.ma.MaskedArray, parameters: dict[Any, Any]) -> float:
    """
    Estimates and returns the mode of those input data that lie within the limits set by the parameters.
    The mode is determined by fitting a guassian function to the peak of the histogram of the logarithms of
    the values.

    :param data: np.array of real values
    :param parameters: dictionary giving the data value bounds
    :return:
    """
    lower = parameters['lower']
    upper = parameters['upper']
    
    if data.max() < lower:
        return lower
    
    if data.min() > upper:
        return upper
    
    cdata = data.compressed()
    
    if len(cdata) == 0:
        return -1.0
    
    hist_range = (np.log(lower), np.log(upper))
    histdata = np.histogram(np.log(cdata), bins=100, range=hist_range)

    hy = np.array(histdata[0])
    hx = np.array(histdata[1])

    hxc = (hx[:-1] + hx[1:]) / 2
    imode = int(np.argmax(hy))
    
    fit_wid = 5
    i1 = max(0, imode - fit_wid)
    i2 = imode + fit_wid
    
    p0 = [hy.max(), hxc[imode], 0.3]

    rfit = fit_gauss(hxc[i1:i2], hy[i1:i2], p0)

    return np.exp(rfit[0][1])


def make_sefd_cmap(ssl: float, ssu: float) -> tuple[mpl.colors.LinearSegmentedColormap, mpl.colors.Normalize]:
    """Construct a colour map that is appropriate (targeted) for SEFD plotting

    Args:
        ssl (float): Lower limit of the SEFD values to plot (Tsys)
        ssu (float): Upper limit of the SEFD values to plot (Tsys)

    Returns:
        tuple[mpl.colors.LinearSegmentedColormap, mpl.colors.Normalize]: The colours and normalise matplotlib instances to use
    """
    # This colour map puts a break 2/3 of the way up from the "hot" scale to blue.
    r0 = 0.0416
    br = 0.98
    b1 = br * 0.365079
    b2 = br * 0.746032
    b3 = br * 1.01
    revtup1 = ((0.0, r0, r0), (b1, 1.0, 1.0), (br, 1.0, 1.0), (b3, 0.8, 0.8), (1.0, 0.8, 0.8))
    revtup2 = ((0.0, 0.0, 0.0), (b1, 0.0, 0.0), (b2, 0.9, 0.9), (br, 0.9, 0.9), (b3, 0.8, 0.8), (1.0, 0.8, 0.8))
    revtup3 = ((0.0, 0.0, 0.0), (b2, 0.0, 0.0), (br, 0.9, 0.9), (b3, 1.0, 1.0), (1.0, 1.0, 1.0))

    cdict = {'red': revtup1, 'green': revtup2, 'blue': revtup3}
    cmap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, N=256)

    norm = mpl.colors.Normalize(vmin=ssl, vmax=ssu)
    return cmap, norm


