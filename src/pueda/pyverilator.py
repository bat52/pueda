#!/usr/bin/env python3

import os
import shutil
import pyverilator
from pueda.vcd import vcd_view

class pyverilator_wrapper(object):
    ''' generate a dut wrapper with pyverilator '''
    sim = None
    dump_filename = ''

    def __init__(self, fname='', src_dirs=[], command_args = [],
                 dump_en = False, dump_fst = False, dump_filename = 'dump', dump_level=0):
        ''' initialize pyverilator wrapper '''

        # rename to .v, if .sv
        if not os.path.isfile(fname):
            assert False, f'File {fname} does not exist!'

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
                                                 args=command_args,
                                                 dump_fst=dump_fst,
                                                 dump_level=dump_level)
        if dump_en:
            if dump_fst:
                dump_ext = '.fst'
            else:
                dump_ext = '.vcd'
            self.dump_filename = dump_filename + dump_ext
            # start gtkwave to view the waveforms as they are made
            self.sim.start_vcd_trace(self.dump_filename)
            # self.view_waves()

    def view_waves(self,savefname='',options='', postcmd='', block_en = True, mode='gtkwave'):
        ''' view vcd waves with gtkwave '''

        # if False:
        #    # start gtkwave to view the waveforms as they are made
        #    self.sim.start_gtkwave()
        #
        #    # add all the io and internal signals to gtkwave
        #    # self.sim.send_to_gtkwave(self.sim.io)
        #    # self.sim.send_to_gtkwave(self.sim.internals)
        # else:
        vcd_view(self.dump_filename,
                    savefname=savefname,
                    options=options,
                    postcmd=postcmd,
                    block_en=block_en,
                    mode=mode)
