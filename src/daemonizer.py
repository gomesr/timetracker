'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A simple daemonizing utility that was put together from information 
          found here: 
          
          http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
'''

import fcntl
import os
import sys

def start(main_method, stdout, stderr, pidfile='/tmp/daemonize.pid'):
    try:
        pid = os.fork()
        if pid > 0:
            exit(0)
    except OSError:
        exit(1)
        
    os.setsid()
    os.umask(0)
    os.chdir('/')
        
    try:
        pid = os.fork()
        if pid > 0:
            exit(0)
      
        lfile = open(pidfile,'w')
        fcntl.lockf(lfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lfile.write('%s' %(os.getpid()))
        lfile.flush()
        
        out_log = open(stdout, 'a+')
        err_log = open(stderr, 'a+')

        os.dup2(out_log.fileno(), sys.stdout.fileno())
        os.dup2(err_log.fileno(), sys.stderr.fileno())
        
        main_method()
    except OSError:
        exit(1)    
    