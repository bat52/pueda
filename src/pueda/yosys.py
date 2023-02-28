
#!/usr/bin/python3

import os
from pueda.common import get_source_files_alldir, get_inc_list, get_clean_work, write_file_lines

def yosys(top='', src_dirs = [], inc_dirs = [], exclude_files = [], synth_en=True) -> None:

    tool = 'yosys'
    work_root = get_clean_work(tool,True)

    # create yosys script
    lines  = get_inc_list(inc_dirs,prefix='read -incdir ')
    lines += ['read_verilog ' + s for s in get_source_files_alldir(src_dirs,fmts=['.v'], excludes=exclude_files)]

    lines.append('hierarchy -top %s' % top)
    fullfile = '%s_full.v' % os.path.join(work_root,top)
    lines.append('write_verilog %s' % fullfile)

    if synth_en:
        if True:
            lines += ['synth']
            lines += ['abc -g cmos2','stat']
        else:
            lines += ['synth_ice40']
        synthfile = '%s_synth.v' % os.path.join(work_root,top)
        lines.append('write_verilog %s' % synthfile)
        # lines += ['show -prefix ./ecdsa256 -format svg -viewer ']
        # lines += ['stat -tech xilinx']
    else:
        synthfile = ''

    # print output
    ysoutfile = os.path.join(work_root,'%s.ys' % top)
    write_file_lines(ysoutfile,lines,print_en=True)    

    # yosys command
    cmdstr = 'yosys -s %s > %s/yosys.log' % (ysoutfile,work_root)
    print(cmdstr)
    os.system(cmdstr)

    return {'single':fullfile,'synth':synthfile,'work':work_root}