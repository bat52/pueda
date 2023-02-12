#!/usr/bin/env python3

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '../src') )

def test_verilator_counter():
    from pueda.edalize import verilator
    verilator(
        simname='counter', top='counter',                        
        src_dir = ['./counter/rtl','./counter/verilator'], 
        inc_dir = [],
        dump_en = False, sim_en=True)

if __name__ == '__main__':
    test_verilator_counter()            