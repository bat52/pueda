#!/usr/bin/env python3

""" PuEDA: verilator tests """

import sys
import os
from pyverilator.verilator_tools import verilator_verilog_tb_ok
sys.path.append( os.path.join(os.path.dirname(__file__), '../src') )
from pueda.edalize import verilator

def test_verilator_counter():
    """ Test counter with verilator """
    if verilator_verilog_tb_ok():
        print('Verilator supports verilog testbench!')
        # tested with verilator 5.021
        verilator(
            simname='counter', top='counter_tb',                  
            src_dir = ['./counter/rtl','./counter/tb'],
            inc_dir = [],
            options=['--binary'],
            dump_en = False, sim_en=True)
    else:
        print('Verilator does not support verilog testbench!')
        # tested with verilator 4.099
        verilator(
            simname='counter', top='counter',
            src_dir = ['./counter/rtl','./counter/verilator'],
            inc_dir = [],
            dump_en = False, sim_en=True)
            # options=['--cc','--no-timing'],
 
if __name__ == '__main__':
    test_verilator_counter()
