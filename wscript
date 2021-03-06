#!/usr/bin/env python

APPNAME = 'timetracker'
VERSION = '0.1'

top = '.' 
out = 'build' 

def configure(ctx):
    print('* configuring the project in ' + ctx.path.abspath())

    ctx.check_tool('python')
    ctx.check_python_version((2,4,2))
    
    ctx.define('PYEXECDIR', ctx.env["PYTHONDIR"]) 
   
    ctx.check_python_module('ConfigParser')
    ctx.check_python_module('hamster')
        
    try:
        ctx.find_program('xprop', var='XPROP', mandatory=True)
    except ctx.errors.ConfigurationError:
        ctx.to_log("Unable to find xprop executable")
    
    try:
        ctx.find_program('qdbus', var='QDBUS', mandatory=True)
    except ctx.errors.ConfigurationError:
        ctx.to_log("Unable to find qdbus executable")
        
    pass

def build(ctx):
    print('* building the project in ' + ctx.path.abspath())
    
    sdir = ctx.path.find_dir('src')
    find = sdir.ant_glob
    
    ctx.install_files('${PYTHONDIR}/timetracker', find('*.py'))
    ctx.install_files('${PYTHONDIR}/timetracker', find('timetracker.py'),chmod=0755)
    ctx.install_files('${PYTHONDIR}/timetracker', find('*.template'))
    ctx.install_files('${PYTHONDIR}/timetracker/trackers',
                      find('trackers/*.py'))
    ctx.install_files('${PYTHONDIR}/timetracker/windowmanagers',
                      find('windowmanagers/*.py'))

    pydir = ctx.env["PYTHONDIR"] 
    ctx.symlink_as('${BINDIR}/timetracker',
                   "%s/timetracker/timetracker.py" % pydir)
    
def dist(ctx):
    ctx.algo      = 'tar.gz' 
    ctx.excl      = ' **/.waf-1* **/*~ **/*.pyc **/*.swp **/.lock-w*' 
    ctx.files     = ctx.path.ant_glob('src/**')

def test(ctx): 
    '''
    A test runner that will load all of the python modules that end with the 
    keyword test from the src/tests directory and run them through the pyunit 
    framework.
    '''
    import os
    import unittest
    import sys
    sys.path.append("src")
    sys.path.append("tests")
    files = os.listdir("tests") 
  
    suite = None 
    for file in files:
        if ( str(file).endswith("test.py") ):
            module = str(file).replace(".py", "")
            exec("import %s" % module)
            suite = unittest.TestLoader().loadTestsFromName(module)
            unittest.TextTestRunner(verbosity=2).run(suite)
