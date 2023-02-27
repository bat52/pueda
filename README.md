PuEDA
=====
A collection of Python tools for micro-Electronics Design Automation.

PuEDA in an acronym, but also stands for a conjugate for of the Spanish verb "poder" which means "can".
The project was born as part of a group of scripts to test the [cryptech](https://cryptech.is/) [ecdsa256](https://github.com/bat52/cryptech) IP.

# Install (from github)
    pip3 install git+https://github.com/bat52/pueda.git@master

# Example of simple simulation with Icarus Verilog
    from pueda.edalize import icarus
    icarus(simname='hello', top='hello_tb', src_dirs = ['./hello'])
   
# Example of simulation with Icarus Verilog
    from pueda.edalize import icarus
    icarus(simname='counter', top='counter_tb', src_dirs = ['./counter/rtl','./counter/tb'], iverilog_options=['-g2005-sv'])

# Example of simulation with pyverilator
    from pueda.pyverilator import pyverilator_wrapper
    pv = pyverilator_wrapper(fname='./counter/rtl/counter.v', src_dirs=['./counter/rtl'], command_args = [], dump_en = False)

    for _ in range(16):
        pv.sim.clock.tick()
        print('count = %d' % pv.sim.io.count)
    assert(pv.sim.io.count == 0)

# Example of synthesys with yosys
    from pueda.yosys import yosys
    yosys(top='counter', src_dirs = ['./counter/rtl'], synth_en=True)
    # gate count available in ./work_yosys/yosys.log

# Common functions
    from pueda.common import * 
    
    # list2str : convert a list of strings into a single string
    # get_source_files_alldir : returns a file list from a list of directories
    # get_source_files: gets all rtl source files from a directory
    # get_inc_list: returns a string appending -I to the input list of directories
    # get_remote_files: donwload files from an internet url
    # vcd_view: visualize a vcd or fst file with gtkwave
    # get_clean_work: generate a clean work direactory for a specific tool
    # write_file_lines: print a file to screen
