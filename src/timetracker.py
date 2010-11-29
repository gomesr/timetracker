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

if __name__ == '__main__':
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
    
    while ( True ):
        check_activity()
        time.sleep(10)
        