#!/usr/bin/env python3

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '../src') )

from myhdl import *
from pueda.myhdl import myhdl_cosim_wrapper, clk_driver

@block
def tb(cosim):

    ports = cosim.dut_ports()
    dut_i = cosim.dut_instance(ports=ports)
    reset = ResetSignal(val=False,active=False,isasync=True)

    clk_driver_i = clk_driver(ports['clk'])
    clk = ports['clk']
    # reset = ports['reset']

    @always_seq(clk.posedge,reset=reset)
    def test_down_count():
        # or idx in range(15,0,-1):
        # print('INDEX: %d, COUNT %d' % (idx,ports['count']))
        # print('COUNT %d' % ports['count'])
        print('something')
        pass    

    return instances()

def myhdl_main():
    topfile = './counter/rtl/counter.v'
    cosim   = myhdl_cosim_wrapper(  topfile=topfile, topmodule='counter', 
                                    src_dirs=['./counter/rtl'], inc_dirs=[],
                                    simname='counter', dump_en=True)
        
    tb_i = tb(cosim)

    cosim.sim_cfg(tb_i)
    cosim.sim_run(16)
    # cosim.sim_view()

    pass

if __name__ == '__main__':
    myhdl_main()
