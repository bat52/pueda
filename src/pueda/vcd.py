#!/usr/bin/env python3

import os
import numpy as np
from ast import literal_eval

# https://pypi.org/project/vcdvcd/
from vcdvcd import VCDVCD

def vcd_view(fname,savefname='',options='', postcmd='', block_en = True):

    # by default look for gtkw file named as vcd
    basefname = os.path.splitext(fname)[0]
    basegtkw = basefname + '.gtkw'
        
    if os.path.isfile(basegtkw):
        savefname = basegtkw

    if os.path.isfile(savefname):
        cmdstr = 'gtkwave %s -a %s %s %s' % (options, savefname,fname,postcmd)
    else:
        cmdstr = 'gtkwave %s %s %s' % (options,fname, postcmd)

    if not(block_en):
        cmdstr += ' &'

    # print(cmdstr)
    os.system(cmdstr)
    pass

def vcd_tv2list(tv,fmt='dec'):
    time = []
    value = []
    for e in tv:

        if   fmt == 'dec':
            vstr = e[1]
        elif fmt == 'bin':
            vstr = '0b' + str.strip(e[1])
        elif fmt == 'hex':    
            vstr = '0h' + str.strip(e[1])
        else:
            print('unsupported format "%s" !!!' % fmt)
            assert(False)

        value.append(literal_eval(vstr))
        time.append(e[0])
    return {'value':value,'time':time}

def vcd_resample(s, fs=1):

    # generate time series
    tmin = min(s['time'])
    tmax = max(s['time'])
    t = np.arange(tmin,tmax,fs)
    sout = np.interp(t, s['time'], s['value'])
    # sout = f(t)

    return {'value':sout, 'time': t}    

def vcd_get_signal(vcdh,sname,fmt = 'dec', resample_en = False, fs=1e9):
    signal = vcdh[sname]
    # tv is a list of Time/Value delta pairs for this signal.
    s = vcd_tv2list(signal.tv,fmt = fmt)
    if resample_en:
        s = vcd_resample(s)
    return s 
