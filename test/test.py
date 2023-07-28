#!/usr/bin/env python3

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '../src') )

import unittest

class TestStringMethods(unittest.TestCase):

    def test_edalize_icarus_hello(self):
        from pueda.edalize import icarus        
        icarus(simname='hello', top='hello_tb', src_dirs = ['./hello'])

    def test_edalize_icarus_counter(self):
       from pueda.edalize import icarus
       icarus(simname='counter', top='counter_tb', src_dirs = ['./counter/rtl','./counter/tb'], iverilog_options=['-g2005-sv'])
       # self.assertEqual('foo'.upper(), 'FOO')

    def test_pyverilator_counter(self):
        from pueda.pyverilator import pyverilator_wrapper
        pv = pyverilator_wrapper(fname='./counter/rtl/counter.v', src_dirs=['./counter/rtl'], command_args = [], dump_en = True, dump_level=1)

        for _ in range(16):
            pv.sim.clock.tick()
            print('count = %d' % pv.sim.io.count)
        assert pv.sim.io.count == 0
        pv.view_waves(mode='vcdterm', block_en=False)

    def test_verilator_counter(self):
        from test_verilator_counter import test_verilator_counter
        test_verilator_counter()

    def test_yosys_counter(self):
        from pueda.yosys import yosys
        yosys(top='counter', src_dirs = ['./counter/rtl'], synth_en=True)

if __name__ == '__main__':
    unittest.main()