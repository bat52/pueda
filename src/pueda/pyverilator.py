#!/usr/bin/env python3

import os
import shutil
import pyverilator

class pyverilator_wrapper(object):
    sim = None

    def __init__(self, fname='', src_dirs=[], command_args = [], dump_en = False):

        # rename to .v, if .sv
        if not os.path.isfile(fname):
            print('File %s does not exist!' % fname)
            assert(False)

        base,ext = os.path.splitext(fname)
        # print(ext)

        if ext == '.sv':
            print('renaming input file to .v')
            ofname = base + '.v'
            shutil.copyfile(fname, ofname)
        else:
            ofname = fname

        print(ofname)
        self.sim = pyverilator.PyVerilator.build(ofname, 
                                                 verilog_path=src_dirs, 
                                                 args=command_args) # args not available on pypi version of pyverilator
                                                                    # https://github.com/bat52/pyverilator
        if dump_en:
            self.view_waves()

    def view_waves(self):
        # start gtkwave to view the waveforms as they are made
        self.sim.start_gtkwave()

        # add all the io and internal signals to gtkwave
        self.sim.send_to_gtkwave(self.sim.io)
        self.sim.send_to_gtkwave(self.sim.internals)

