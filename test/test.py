#!/usr/bin/env python3

import unittest

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '../src') )

from pueda.edalize import icarus
from pueda.pyverilator import pyverilator_wrapper
from test_verilator_counter import test_verilator_counter
from pueda.yosys import yosys
class TestStringMethods(unittest.TestCase):
    """ Unit test class """

    def test_edalize_icarus_hello(self):
        """ test edalize icarus hello """
        icarus(simname='hello', top='hello_tb', src_dirs = ['./hello'], dump_en=False)

    def test_edalize_icarus_counter(self):
        """ test edalize icarus hello """
        icarus(simname='counter', top='counter_tb',
            src_dirs = ['./counter/rtl','./counter/tb'],
            iverilog_options=['-g2005-sv'],
            dump_en=False)
        # self.assertEqual('foo'.upper(), 'FOO')

    def test_pyverilator_counter(self):
        """ test pyverilator counter """
        pv = pyverilator_wrapper(fname='./counter/rtl/counter.v',
                                 src_dirs=['./counter/rtl'],
                                 command_args = [],
                                 dump_en = True, dump_level=1)

        for _ in range(16):
            pv.sim.clock.tick()
            print('count = %d' % pv.sim.io.count)
        assert pv.sim.io.count == 0
        pv.view_waves(mode='vcdterm', block_en=False)

    def test_verilator_counter(self):
        """ test verilator counter """
        test_verilator_counter()

    def test_yosys_counter(self):
        """ test yosys counter """
        yosys(top='counter', src_dirs = ['./counter/rtl'], synth_en=True)

if __name__ == '__main__':
    unittest.main()
