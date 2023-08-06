#!/usr/bin/env python3
""" Utility for generating names for holography and ASKAP primary beam files """

import glob


def make_file_name(obj, kind):
    """Returns a file name according to metadata and the label provided in kind
    :param obj: MapSet object holding holography beam data
    :param kind: str
    """
    parts = ['akpb']
    pol = set(obj.metadata["polarizations"].astype(str))
    if pol == {"I", "Q", "U", "V"}:
        parts.append('iquv')
    elif pol == {"XX", "XY", "YX", "YY"}:
        parts.append('xxyy')
    elif len(pol) == 1:
        parts.append(list(pol)[0].lower())
    else:
        parts.append('????')
    parts.append(obj.metadata['fp_name'])
    p_arcmin = int(obj.metadata['fp_pitch'] * 60 + 0.5)
    parts.append("{:02d}".format(p_arcmin))
    frqs = obj.frequencies
    frq_centre = int((frqs[0] + frqs[-1])/2.0 + 0.5)
    parts.append("{:d}MHz".format(frq_centre))
    sb = obj.metadata['holographySBID']
    parts.append("SB{:d}".format(sb))
    if len(kind) > 0:
        parts.append(kind)
    fix_parts = []
    for p in parts:
        if type(p) is bytes:
            p = p.decode()
        fix_parts.append(p)
    return '.'.join(fix_parts)


def make_file_name_template(pol='????', fp_name='*', fp_pitch=0, frq_centre=0, sbid=-1, kind='.*'):
    """Returns a file name according to arguments and the label provided in kind. Parameters not
    provided result in wild-card sections in the file name
    :param pol: str Polarization desriptor 'xxyy' or 'iquv'
    :param fp_name: str Footprint name
    :param fp_pitch: int beam pitch in arcminutes
    :param frq_centre: int Centre frequency in integer MHz.
    :param sbid: int Scheduling block ident.
    :param kind: str
    """
    parts = ['akpb', pol, fp_name]
    if fp_pitch == 0:
        parts.append('??')
    else:
        parts.append("{:02d}".format(fp_pitch))
    if frq_centre == 0:
        parts.append('*MHz')
    else:
        parts.append("{:d}MHz".format(frq_centre))
    if sbid == -1:
        parts.append('SB*')
    else:
        parts.append("SB{:d}".format(sbid))
    if len(kind) > 0:
        parts.append(kind)
    return '.'.join(parts)


def find_holo_file(holo_dir, pol='????', fp_name='*', fp_pitch=0, frq_centre=0, sbid=-1, kind='*'):
    """Returns a file name according to arguments and the label provided in kind. Parameters not
    provided result in wild-card sections in the file name, and the disk is searched for a matching file.
    :param holo_dir: str Name of directory holding files
    :param pol: str Polarization desriptor 'xxyy' or 'iquv'
    :param fp_name: str Footprint name
    :param fp_pitch: int beam pitch in arcminutes
    :param frq_centre: int Centre frequency in integer MHz.
    :param sbid: int Scheduling block ident.
    :param kind: str
    """
    templ = holo_dir + '/' + make_file_name_template(pol=pol, fp_name=fp_name, fp_pitch=fp_pitch,
                                                     frq_centre=frq_centre, sbid=sbid, kind=kind)
    names = glob.glob(templ)
    if len(names) == 1:
        return names[0]
    else:
        raise FileNotFoundError("No file {} found".format(templ))
