#!/usr/bin/python3

import os
import shutil

# load vcd_view for backwards compatibility
from pueda.vcd import vcd_view

def list2str(l,sep=' '):
    return sep.join(str(s) for s in l)

def get_source_files_alldir(dirlist,fmts=['.v','.sv','.vh'], excludes = []) -> list:
    files = []
    # create files list
    for d in dirlist:
        files = files + get_source_files(d,fmts=fmts, excludes=excludes)

    return files

def get_source_files(directory,fmts=['.v','.sv','.vh'], excludes = []) -> list:
    # print(directory)

    if os.path.isdir(directory):
        flist = os.listdir(directory)

        foutlist = []
        for f in flist:
            # print(f)
            fbase,fext = os.path.splitext(f)
            fullfile = os.path.abspath(os.path.join(directory,f))
            if os.path.isfile(fullfile) and (fext in fmts) and not(f in excludes) :
                # print('file %s' % f)
                foutlist.append(fullfile)
            elif os.path.isdir(fullfile):
                # recursively browse dir
                # print('recursion %s' % f)
                ldir = os.path.join(directory,f)
                # print(ldir)
                llist = get_source_files( ldir ,fmts=fmts )
                foutlist = foutlist + llist
            pass
    else: # if os.path.isdir(directory):
        print('%s : WARNING!!! directory "%s" does not exist!' % (__name__, directory) )
        foutlist = []

    # print(foutlist)

    return foutlist

def get_inc_list(inclist,work_root='',prefix='-I') -> list:

    outlist = []
    for ipath in inclist:
        if len(work_root)>0:
            inc = prefix + os.path.relpath(ipath,work_root)
        else:
            inc = prefix + os.path.abspath(ipath)
        outlist.append(inc)

    return outlist
    pass

def get_remote_files(url,flist=[],dstdir='./work_get'):
    import wget

    if not(os.path.isdir(dstdir)):
        os.makedirs(dstdir)

    if len(flist)>0:
        for f in flist:
            src = os.path.join(url   ,f)
            dst = os.path.join(dstdir,f)
            # print(src)
            # print(dst)
            if not(os.path.isfile(dst)):
                wget.download( src , dst )
    else:
        # single file
        wget.download( url , dstdir )
        fext = os.path.splitext(url)[1]
        if fext == '.zip':
            os.system('cd %s && dtrx -f `ls *.zip && cd ..`' % dstdir)

def get_work_path(tool=''):
    return os.path.join(os.getcwd() , 'work_' + tool)    

def work_exists(tool=''):
    return os.path.isdir(get_work_path(tool))

def get_clean_work(tool='',makedir=False,rm_en=True):
    work_root = get_work_path(tool) 

    if work_exists(tool) and rm_en:
        # delete work directory
        shutil.rmtree(work_root,ignore_errors=True)
    
    if makedir:
        os.makedirs(work_root)
        
    return work_root

def write_file_lines(fname, lines=[], mode='w', print_en=False):
    
    f = open(fname, mode)
    for l in lines: 
        # print(l)
        f.write(l + '\n')
    f.close()

    # print file
    if print_en:
        os.system('cat %s' % fname)