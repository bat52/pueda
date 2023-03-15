#!/usr/bin/env python3

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from pueda.common import get_source_files_alldir, get_remote_files, get_work_path, work_exists, get_clean_work, list2str, get_inc_list

def vpi_make(src_dirs=['./'], inc_dirs=[], args = []):
    # print(src_dirs)
    src = get_source_files_alldir(src_dirs,fmts=['.c','.cc','.cpp'])
    inc = get_inc_list(inc_dirs)
    # print(inc)

    argstr = list2str(args)
    srcstr = list2str(src)
    incstr = list2str(inc)
    cmdstr = list2str( ['iverilog-vpi', argstr, srcstr, incstr]) # , ' > iverilog-vpi.log' ] )

    print('### Making VPI...')
    print(cmdstr)
    os.system(cmdstr)
    os.system('rm *.o')
    print('### Making VPI... Done')
    pass

class custom_vpi(object):
    work = './'

    def __init__(self,tool='custom_vpi',url='',flist=[],inc_dirs=[],args=[], custom_make_cmds=[],rm_en=True):
        #if not( self._init_work(tool=tool,rm_en=rm_en) ):
        self._init_work(tool=tool,rm_en=rm_en)
        self._get_custom_vpi(url=url,flist=flist)      

        if len(custom_make_cmds)>0:
            self.custom_make(cmds=custom_make_cmds)
        else:
            self.auto_make(inc_dirs=inc_dirs,args=args)
        #else:
        #    print('WARNING: skip compiling VPI %s, because folder already exists!!! ' % tool)

    def _init_work(self,tool='',rm_en=False):
        exist = work_exists(tool)

        if rm_en or not(exist):
            self.work = get_clean_work(tool=tool,rm_en=rm_en) # do not remove if exist
        else:
            self.work = get_work_path(tool)        
        
        return exist

    def _get_custom_vpi(self,url,flist):
        get_remote_files(url=url,flist=flist,dstdir=self.work)

    def auto_make(self,inc_dirs=[],args=[]):
        new_inc = [os.path.join(self.work,ii) for ii in inc_dirs]
        vpi_make(src_dirs=[self.work], inc_dirs=new_inc,args=args)
        os.system('mv *.vpi %s' % self.work)

    def custom_make(self,cmds=[]):
        cmdstr = ' && '.join(cmds)
        print(cmdstr)
        os.system(cmdstr)

class myhdl_vpi(custom_vpi):
    def __init__(self):
        tool='myhdl_vpi'
        url="https://raw.githubusercontent.com/myhdl/myhdl/master/cosimulation/icarus"
        flist = ['myhdl.c', 'myhdl_table.c', 'Makefile']
        custom_vpi.__init__(self,tool=tool,url=url,flist=flist) # , args=['-w'])

class fst_vpi(custom_vpi):
   
    def __init__(self):
        tool='fst_vpi'
        url="https://github.com/semify-eda/fstdumper/archive/refs/heads/main.zip"        
        self._init_work(tool=tool)
        cmds = ['cd %s' % os.path.join(self.work,'fstdumper-main'),
                'make simulation-iverilog',
                'mv *.vpi %s' % self.work ,
                'cd ..']
        custom_vpi.__init__(self,tool=tool,url=url,custom_make_cmds=cmds)

if __name__ == '__main__':
    # mv = myhdl_vpi()
    fv = fst_vpi()