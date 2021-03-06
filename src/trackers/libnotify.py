'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A Tracker plugin for the timetracker tool that is used mainly for 
          testing since it just popups the notification with the currently 
          executing activity.

          The icon file is a royalty free icon from http://icons.mysitemyway.com 
          which  is supplied with the same royalty free license found on their 
          website.
'''

import process
import tracker
import os

libnotify_cmd = "/usr/bin/notify-send"

libnotify_defaults = [ "-i",
                       "%s/timetracker.png" % os.getcwd(),
                       "-u",
                       "normal"]
    
class LibNotifyTracker(tracker.Tracker):
    
    name = None
   
    def __init__(self):
        if ( not(os.path.exists(libnotify_cmd)) ):
            raise Exception("Couldn't find application [%s]" % libnotify_cmd) 
    
    def start(self, name, category, description, tags = []):
        notify("TimeTracker", "Starting activity [%s]" % name)
        self.name = name
    
    def stop(self):
        notify("TimeTracker","Stopping activity")
        self.name = None
        
    def destroy(self):
        self.name = None
        
    def get_current_activity(self):
        return self.name

def notify(title, message):
    cmd = [ libnotify_cmd ]
    
    for x in libnotify_defaults :
        cmd.append(x)
    
    cmd.append(title)
    cmd.append(message)
    
    process.execute(cmd)
