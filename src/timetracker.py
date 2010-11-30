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
import getopt
import signal
import atexit
import shutil

from sys import exit

# adding the trackers folder to the imports path ;)
import sys
sys.path.append("%s/trackers" % sys.path[0])
sys.path.append("%s/windowmanagers" % sys.path[0])

import daemonizer
import windowmanagers.wmfactory as wmfactory

# globals
global config
global activities_dict
global tags_dict
global activity_tracker

# global active window title function
global windowmanager 

def on_shutdown():
    print("Shutting down...")
    activity_tracker.stop()

def check_activity():
    if ( not(windowmanager.is_desktop_active()) ):
        print("desktop inactive...")
        activity_tracker.stop()
        
        activity_tracker.start("Away","","Off to reality",[])
        return
    
    title = windowmanager.get_active_window_title() 
    
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
    print("")
    print("timertracker [-d] [-s] [-h]")
    print("    -d - daemonize the timetracker utility")
    print("    -s - shutdown a previously daemonized execution")
    print("    -c - copy config template to ~/.timetracker.conf")
    print("    -h - this menu")
   
def main_loop():
    while ( True ):
        check_activity()
        time.sleep(30) 
        
if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hdcs",
                                   ["help", "daemon", "create-config" "shutdown"])
    except getopt.GetoptError as err:
        print(str(err)) 
        usage()
        sys.exit(2)
        
    daemonize = False
    shutdown = False
    createconfig = False
    
    for o, a in opts:
        if o == "-d":
            daemonize = True
        if o == "-c":
            createconfig = True
        elif o == "-s":
            shutdown = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
            
    home = os.getenv("HOME")
    configfile = home + "/.timetracker.conf"
    
    if ( createconfig ):
        shutil.copy("%s/timetracker.conf.template" % sys.path[0], configfile)
   
    config = configparser.RawConfigParser()
    if ( os.path.exists(configfile) ):
        config.read(configfile)
        titems = config.items('tags')
        tags_dict = dict([x for x in titems])
        
        aitems = config.items('activities')
        activities_dict = dict([x for x in aitems])
    else:
        print("create a new timetracker config file with the -c option")
        exit(2)

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
    
    if ( config.has_option("main", "update.interval") ):
        tracker_sleep = config.get("main", "update.interval")
    else:
        tracker_sleep = 30 # default 30s
    
    out = config.get("main", "out.log")
    err = config.get("main", "err.log")
    
    if ( os.path.exists('/tmp/timetracker.pid') ):  
        pid = int(open('/tmp/timetracker.pid', 'r').readlines()[0]) 
    else:
        pid = None
    
    if ( shutdown and pid != None ):
        try:
            os.kill(pid, signal.SIGKILL)
            print("killed daemon at pid %d" % pid)
            os.remove('/tmp/timetracker.pid')
        except:
            print("unable to kill proces %d" % pid)
            exit()
        
    if ( pid != None ):
        try:
            os.kill(pid, 0)
            print("already running, use -s option to shutdown previous instance")
            exit(-1)
        except OSError:
            print("stale daemon pid entry in config")
            os.remove('/tmp/timetracker.pid')

    windowmanager = wmfactory.load_windowmanager()
    
    if ( daemonize ):
        daemonizer.start(main_loop, out, err, '/tmp/timetracker.pid')

    atexit.register(on_shutdown)
    main_loop()
        