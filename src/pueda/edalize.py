#!/usr/bin/env python3

import os
import multiprocessing
import pkg_resources

# from edalize import *
from edalize.edatool import get_edatool # required by edalize 0.5.0

import pueda
from pueda.common import get_source_files_alldir, get_inc_list, get_clean_work
from pueda.icarus import myhdl_vpi, fst_vpi
from pueda.vcd    import vcd_view
from pyverilator.verilator_tools import verilator_verilog_tb_ok

def get_dump_dirs():
    r_data_path = '../../../../data/'
    # assert pkg_resources.resource_isdir(pueda.__name__,r_data_path), 'ERROR: directory {r_data_path} does not exist!'
    data_path = pkg_resources.resource_filename(pueda.__name__,r_data_path)

    if pkg_resources.resource_isdir(pueda.__name__,r_data_path):
        # pueda installed, look in shared data folder    
        inc_dirs = [ os.path.join(data_path, 'icarus/inc') ]
        src_dirs = [ os.path.join(data_path, 'icarus/src') ]
    else:
        # pueda not installed, assume running from local git copy
        inc_dirs = [ os.path.join(os.path.dirname(__file__), '../../data/icarus/inc') ]
        src_dirs = [ os.path.join(os.path.dirname(__file__), '../../data/icarus/src') ]

    return inc_dirs, src_dirs

def eda_get_files(dirlist,work_root,fmts=['.v','.sv','.vh'],print_en=False) -> list:
    fnames = get_source_files_alldir(dirlist,fmts=fmts)
    # print(fnames)
    
    # build list of dict as needed by edalize
    files = []
    for fname in fnames:

        if print_en:
            print(fname)

        fext = os.path.splitext(fname)[1]

        # source files
        if fext in ['.v']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'verilogSource'}
        elif fext in ['.vh']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'verilogSource',
            'is_include_file' : True
            }
        elif fext in ['.sv']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'systemVerilogSource'}
        elif fext in ['.svh']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'systemVerilogSource',
            'is_include_file' : True
            }
        elif fext in ['.c','.cpp']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'cSource'}
        elif fext in ['.h']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'cSource',
            'is_include_file' : True
            }
        elif fext in ['.vpi']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'verilogSource'}
        else:
            print(f'unknown file extension for file {fname} !!!')
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'unknown'}
       
        files.append(f)

    return files

def icarus(simname='', top='', src_dirs = [], inc_dirs = [],
            dump_en = True, dump_fst_vpi = True, run_en = True, myhdl_en = False,
            iverilog_options = [],
            plot_mode = 'vcdterm', plot_block_en = False, gtkw='') -> None:
    """ Icarus verilog helper function """

    # tool
    tool = 'icarus'
    work_root = get_clean_work(tool,True)

    # always include dump files, in case want to use them,
    # even if dump is disabled
    inc_dump, src_dump = get_dump_dirs()
    inc_dirs += inc_dump
    src_dirs += src_dump
    
    if dump_en:
        iverilog_options += [
            '-DDUMP_EN', 
            '-DDUMP_LEVEL=0', 
            f'-DDUMP_MODULE={top}'
            ]
        if dump_fst_vpi:
            iverilog_options += ['-DDUMP_FST_VPI']

    if myhdl_en:
        mvpi = myhdl_vpi()
        src_dirs += [mvpi.work]
    else:
        mvpi = None

    # this is only for fstdumper-vpi, but fst saving 
    # is enabled by default when using icarus with edalize
    if dump_en and dump_fst_vpi:
        fvpi = fst_vpi()
        vvp_options = ['-mfstdumper.so', f'-M{fvpi.work}']
    else:
        vvp_options = []

    # get design files
    files = eda_get_files(src_dirs, work_root, fmts=['.v','.vpi'])

    # get include directories
    options = iverilog_options + get_inc_list(inc_dirs,work_root)
    tool_options = {
        tool :
            {
            'iverilog_options'  : options,
            'vvp_options'       : vvp_options 
        }
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : top,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)
    
    backend.configure()
    backend.build()

    if run_en:
        backend.run()
        if dump_en:
            if dump_fst_vpi:
                dump_file = 'dump.fst'
            else:
                dump_file = 'dump.vcd'

            vcd_view(os.path.join(work_root, dump_file),
                    savefname=gtkw,
                     mode=plot_mode, block_en=plot_block_en)

    return {'backend'   : backend,
            'work_root' : work_root, 
            'mvpi'      : mvpi
            }

def verilator(simname='', top='', src_dir=[], inc_dir = [],
              options = [],
              dump_en = True, dump_fst = False, gtkw = '', sim_en = True,
              plot_mode = 'vcdterm', plot_block_en = False) -> None:
    # tool
    tool = 'verilator'
    work_root = get_clean_work(tool)

    verilator_options = options
    verilator_options += [f'--top-module {top}' ]
    # verilator_options += ['-j %d' % multiprocessing.cpu_count() ] # does not work with version 4.028

    if verilator_verilog_tb_ok():
        inc_dump, src_dump = get_dump_dirs()
        inc_dir += inc_dump
        src_dir += src_dump

    if dump_en:
        verilator_options += ['--trace']
           
        if dump_fst:
            verilator_options += ['--trace-fst', '-CFLAGS -DDUMP_FST']

    # get design files
    files = eda_get_files(src_dir, work_root, fmts=['.v','.vh','.cpp','.c'])

    # get include directories
    options = verilator_options + get_inc_list(inc_dir,work_root)
    tool_options = {
        tool :
            {
            'verilator_options'  : options,
        }
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : top,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()

    if sim_en:
        backend.run()

        if dump_en:
            if dump_fst:
                dump_file = 'dump.fst'
            else:
                dump_file = 'dump.vcd'

            vcd_view( fname=os.path.join(work_root, dump_file),
                     savefname=gtkw,
                     options='-o', mode=plot_mode, block_en=plot_block_en)

def trellis(simname='',top='',src_dir=[], inc_dir=[]) -> None:

    # tool
    tool = 'trellis'
    work_root = get_clean_work(tool)
    
    # get design files
    files = eda_get_files(src_dir, work_root, fmts=['.v'])

    # get include directories
    files += eda_get_files(inc_dir, work_root, fmts=['.vh'])

    # get include directories
    options = get_inc_list(inc_dir,prefix='read -incdir ')

    tool_options = {
        tool :
            {
            'trellis_options'  : {'yosys_synth_options' : options},
        }
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : top,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()

def yosys_edalize(simname='',top='',src_dir=[], inc_dir=[], arch='ice40') -> None:

    # tool
    tool = 'yosys'
    work_root = get_clean_work(tool)
    
    # get design files
    files = eda_get_files(src_dir, work_root, fmts=['.v'])

    # get include directories
    files += eda_get_files(inc_dir, work_root, fmts=['.vh'])
    
    tool_options = {
        tool :
            {
            # 'yosys_synth_options'  : options,
            'arch': arch,
        },
    
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : top,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()
