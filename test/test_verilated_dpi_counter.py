#!/usr/bin/env python3

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '../src') )

def test_verilated_dpi_counter():
    from pueda.edalize import verilator
    verilator(
        simname='counter', top='counter',                        
        src_dir = ['./counter/rtl','./counter/verilator'], 
        inc_dir = [],
        dump_en = False, sim_en=False)

if __name__ == '__main__':
    test_verilated_dpi_counter()            