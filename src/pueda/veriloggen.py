#!/usr/bin/env python3


""" PuEDA: veriloggen functions
A collection of Python tools for micro-Electronics Design Automation. """

import veriloggen as vg
from pueda.common import get_source_files_alldir

def sim(top='', src_dirs = [], inc_dirs = []):
    """ simulation """
    allfiles=get_source_files_alldir(src_dirs+inc_dirs)
    modules = vg.from_verilog.read_verilog_module(*allfiles,include=inc_dirs)
    pass

if __name__ == '__main__':
    sim()
