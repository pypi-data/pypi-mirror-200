import numpy as np


def flux_of_1934(freq):
    """ frequency in MHz
    """
    a, b, c, d = -30.7667, 26.4908, -7.0977, 0.605334
    log_f = np.log10(freq)
    log_s = a + log_f * (b + log_f * (c + d * log_f))
    s = 10 ** log_s
    return s
