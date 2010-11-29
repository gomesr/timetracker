#!/usr/bin/python3
'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A tracking tool to help the already existing hamster-applet for gnome
          to detect what the user is currently doing on his/her desktop. This is
          done by using some preset rules to identify the name of the activity 
          as well as some tags associated with that activity. With this 
          information this tool then instructs the hamster-applet using the 
          hamster-cli to start/stop activites.
'''
import configparser 
import time
import os.path
import signal
import getopt

from os import fork, chdir, setsid, umask
from sys import exit

# adding the trackers folder to the imports path ;)
import sys
sys.path.append('trackers')
sys.path.append('windowmanagers')

# globals
global config
global activities_dict
global tags_dict
global activity_tracker

# global active window title function
global get_active_window_title

def check_activity():
    title = get_active_window_title() 
    
    if ( title != None ):
        words = title.lower().split(' ') 
        activity = None
        for word in words:
            for key in activities_dict.keys():
                if ( key.lower() in word ):
                    activity = activities_dict[key]
                    break
        
        tags = []        
        for word in words:
            for key in tags_dict.keys():
                if ( key.lower() in word ):
                    aux_tags = tags_dict[key]
                    for t in aux_tags.split(','):
                        tags.append(t)
    
        if ( activity != None ):
            aux = activity_tracker.get_current_activity()
            already_done = False
            
            if ( aux != None): 
                if ( activity in aux ):
                    print("tracked [%s,%s,{%s}]" % (activity,title,','.join(tags)))
                    already_done = True
                else:
                    print("stopping current")
                    activity_tracker.stop()
        
            if ( not(already_done) ): 
                print("starting [%s,%s,{%s}]" % (activity,title,','.join(tags)))
                activity_tracker.start(activity, "", title, tags)
        else:
            print("unknown activity [%s]" % title)
    
def get_config():
    """
    Get the currently loaded configuration file from the main timetracker 
    application. Any values set on this config will be saved once you call the
    save_config file.
    """
    return config

def save_config():
    """
    This function is used to save the application configuration whenever you 
    make any changes to the current configuration that you can obtain using the
    get_config function.
    """
    home = os.getenv("HOME")
    configfile = home + "/.timetracker.conf"
    config.write(open(configfile,"w"))

def usage():
    print("timetracker")
   
def main_loop():
    while ( True ):
        check_activity()
        time.sleep(60) 
        
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hds",
                                   ["help", "daemon", "shutdown"])
    except getopt.GetoptError as err:
        print(str(err)) 
        usage()
        sys.exit(2)
        
    daemonize = False
    shutdown = False
    
    for o, a in opts:
        if o == "-d":
            daemonize = True
        elif o == "-s":
            shutdown = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
            
    home = os.getenv("HOME")
    configfile = home + "/.timetracker.conf"
   
    config = configparser.RawConfigParser()
    if ( os.path.exists(configfile) ):
        config.read(configfile)
        titems = config.items('tags')
        tags_dict = dict([x for x in titems])
        
        aitems = config.items('activities')
        activities_dict = dict([x for x in aitems])
    else:
        print("no rules loaded...")

    # load tracker
    if ( config.has_option("main", "tracker") ):
        tracker_id = config.get("main", "tracker")
    else:
        tracker_id = "hamster:HamsterTracker"
        
    [module,cl] = tracker_id.split(':')
    # a little magical dynamic loading of modules
    exec("from %s import %s as Tracker" % (module,cl))
    exec("activity_tracker = Tracker()")
    print("using %s tracker" % module)
    
    # load window manager
    if ( config.has_option("main", "windowmanager") ):
        wm = config.get("main", "windowmanager")
    else:
        wm = "gnomewm"
        
    # a little magical dynamic loading of modules
    exec("from %s import get_active_window_title" % wm)
    
    out = config.get("main", "out.log")
    err = config.get("main", "err.log")
    
    if ( config.has_option("main", "daemon.pid") ):
        pid = int(config.get("main", "daemon.pid"))
    else:
        pid = None
    
    if ( shutdown and pid != None ):
        try:
            os.kill(pid, signal.SIGKILL)
            print("killed daemon at pid %d" % pid)
        except:
            print("unable to kill proces %d" % pid)
            
        config.remove_option("main", "daemon.pid")
        save_config()
        exit()
        
    if ( pid != None ):
        try:
            os.kill(pid, 0)
            print("already running, use -s option to shutdown previous instance")
            exit(-1)
        except OSError:
            print("stale daemon pid entry in config")
            config.remove_option("main", "daemon.pid")
            save_config()
    
    if ( daemonize ):
        try:
            pid = fork()
            if pid > 0:
                exit(0)
        except OSError as e:
            exit(1)
        
        chdir("/")
        setsid()
        umask(0)
        
        try:
            pid = fork()
            if pid > 0:
                print("daemon pid %d" % pid)
                config.set("main", "daemon.pid", pid);
                save_config()
                exit(0)
            out_log = open(out, 'a+')
            err_log = open(err, 'a+')
            os.dup2(out_log.fileno(), sys.stdout.fileno())
            os.dup2(err_log.fileno(), sys.stderr.fileno())
        except OSError as e:
            exit(1)
            
    main_loop()
        