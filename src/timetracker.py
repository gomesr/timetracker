#!/usr/bin/env python
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
import configuration

# globals
global activities_dict
global activities_dict_keys
global tags_dict
global tags_dict_keys

global tracker_sleep
global activity_tracker

# global active window title function
global windowmanager 
global laststatus

laststatus = { 'activity': '', 'title': '', 'tags': []} 

def on_shutdown():
    windowmanager.stop()
    activity_tracker.destroy()

def window_changed(title):
    global activities_dict
    global activities_dict_keys
    global tags_dict
    global tags_dict_keys
    global laststatus
    global activity_tracker

    title = title.replace("#","")
    aux = activity_tracker.get_current_activity()
    print("current %s" % aux)
    if ( aux != None and aux.find('#ttstop') != -1 ):
        print("timetracker can not touch [%s]" % aux)
        return
        
    if ( title != None ):
        tags = []        
      
        activity = None
        title = title.lower()
        
        # once the first activity is found that is the one that represents
        # this task
        for key in activities_dict_keys:
            if ( key in title ):
                activity = activities_dict[key]
                break
          
        # there is no restrictions in the number of tags you can add to 
        # any ActivityLogTracker 
        for key in tags_dict_keys:
            if ( key in title ):
                aux_tags = tags_dict[key]
                for t in aux_tags.split(','):
                    tags.append(t)
                    
        tags = set(tags)
        
        if ( activity != None ):
            already_done = False
    
            if ( aux != None ):
                if ( title == laststatus['title'] ):
                    print("tracked [%s,%s,{%s}]" % (activity,title,','.join(tags)))
                    already_done = True
                else:
                    print("stopping [%s,%s,{%s}]" % 
                                    (laststatus['activity'],
                                     laststatus['title'],
                                     ','.join(laststatus['tags'])))
                    activity_tracker.stop()
                    
            if ( not(already_done) ): 
                print("starting [%s,%s,{%s}]" % (activity,title,','.join(tags)))
                activity_tracker.start(activity, "", title, tags)
                laststatus = { "activity": activity,
                               "title" : title,
                               "tags": tags }
        else:
            print("unknown activity [%s]" % title)

def reorder(keys,dictionary):
    for key in keys:
        index = key.find('.')
        if ( index != -1 ):
            nkey = key[0:index]
            index = int(key[index+1])
            dictionary[nkey] = dictionary[key]
            del dictionary[key]
            keys.remove(key)
            keys.insert(index,nkey)
            
    return keys
                
def load_defaults(config):  
    global activities_dict
    global activities_dict_keys
    global tags_dict
    global tags_dict_keys
    
    titems = config.items('tags')
    tags_dict = dict([(str.lower(x),y) for (x,y) in titems])
    tags_dict_keys = tags_dict.keys()
    tags_dict_keys = reorder(tags_dict_keys, tags_dict)
    
    aitems = config.items('activities')
    activities_dict = dict([(str.lower(x),y) for (x,y) in aitems])
    activities_dict_keys = activities_dict.keys()
    activities_dict_keys = reorder(activities_dict_keys, activities_dict)
    
def usage():
    print("")
    print("timertracker [-d] [-s] [-h] [-c] [-l configfile]")
    print("    -d - daemonize the timetracker utility")
    print("    -s - shutdown a previously daemonized execution")
    print("    -c - copy config template to ~/.timetracker.conf")
    print("    -l - load this configfile instead")
    print("    -h - this menu")
 
def main_loop():
    global windowmanager 
    global activity_tracker
    
    # load tracker
    if ( config.has_option("main", "tracker") ):
        tracker_id = config.get("main", "tracker")
    else:
        tracker_id = "hammy:HamsterTracker"
   
    [module,cl] = tracker_id.split(':')
   
    # a little magical dynamic loading of modules
    exec("from trackers.%s import %s as Tracker" % (module,cl))
    activity_tracker = Tracker()
    print("loaded %s tracker" % module)

    windowmanager = wmfactory.load_windowmanager()
    windowmanager.start(window_changed)

    atexit.register(on_shutdown)
    
    try:
        while ( True ):
            time.sleep(1)
            isactive = windowmanager.is_desktop_active()
            current = activity_tracker.get_current_activity()
            
            if ( not(isactive) and current != "away" ):
                activity_tracker.stop()
                activity_tracker.start("away",
                                       "",
                                       "off to reality",
                                       ["ttaway","away"])
            
            if ( isactive and current.find("#ttaway") != -1 ):
                '''
                return to the previous task but make sure to wipe out the last 
                status so that the tool cn continue to track correctly
                '''
                title = laststatus['title']
                laststatus['title'] = None 
                window_changed(title)
                
    except: 
        on_shutdown()
        
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hdcls",
                                   ["help",
                                    "daemon",
                                    "create-config",
                                    "load=",
                                    "shutdown"])
    except getopt.GetoptError as err:
        print(str(err)) 
        usage()
        sys.exit(2)
        
    daemonize = False
    shutdown = False
    createconfig = False
    loadconfig = None
    
    for o, a in opts:
        if o == "-d":
            daemonize = True
        elif o == "-c":
            createconfig = True
        elif o in ( "-l","--load" ):
            loadconfig = a
        elif o == "-s":
            shutdown = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "option not handled"
            
    home = os.getenv("HOME")
    configfile = home + "/.timetracker.conf"
    
    if ( createconfig ):
        print("Copied default configuration file into place.")
        shutil.copy("%s/timetracker.conf.template" % sys.path[0], configfile)
        sys.exit(0)
    
    if ( loadconfig != None ):
        print("loading %s configuration file" % loadconfig)
        configfile = loadconfig
   
    if ( os.path.exists(configfile) ):
        configuration.load_config(configfile)
        config = configuration.get_config()
        load_defaults(config)
    else:
        print("create a new timetracker config file with the -c option")
        exit(2)
    
    if ( config.has_option("main", "update.interval") ):
        tracker_sleep = int(config.get("main", "update.interval"))
    else:
        tracker_sleep = 30 # default 30s
    
    out = config.get("main", "out.log")
    err = config.get("main", "err.log")
    pidfile = "/tmp/timetracker.pid"
    
    if ( os.path.exists(out) ):
        if ( not(os.access(out, os.W_OK)) ):
            raise EnvironmentError("Unable to write to [%s]" % out)

    if ( os.path.exists(err) ):
        if ( not(os.access(err, os.W_OK)) ):
            raise EnvironmentError("Unable to write to [%s]" % err)

    if ( os.path.exists(pidfile) ):
        if ( not(os.access(pidfile, os.W_OK)) ):
            raise EnvironmentError("Unable to write to [%s]" % pidfile)
    
        if ( not(os.access(pidfile, os.R_OK)) ):
            raise EnvironmentError("Unable to read from [%s]" % pidfile)
    
    if ( os.path.exists(pidfile) ):  
        pid = int(open(pidfile, 'r').readlines()[0]) 
    else:
        pid = None
    
    if ( shutdown ):
        if ( pid != None ):
            os.kill(pid, signal.SIGKILL)
            print("killed daemon at pid %d" % pid)
            os.remove(pidfile)
            exit()
        else:
            print("no tracker currently running.")
            exit(-1)
        
    if ( pid != None ):
        try:
            os.kill(pid, 0)
            print("already running, use -s option to shutdown previous instance")
            exit(-1)
        except OSError:
            print("stale daemon pid entry in config")
            os.remove(pidfile)

    if ( daemonize ):
        daemonizer.start(main_loop, out, err, pidfile)
    else:
        main_loop()
        
