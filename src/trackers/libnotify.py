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
    
    def start(self, name, category, description, tags = []):
        cmd = [ libnotify_cmd ] 
        for x in libnotify_defaults :
            cmd.append(x)
        cmd.append("Activity started: %s" % name)
        cmd.append("%s" % description)
        process.execute(cmd)
    
    def stop(self):
        cmd = [ libnotify_cmd, "" ]
        for x in libnotify_defaults :
            cmd.append(x)
        cmd.append("stopping activity")
        process.execute(cmd)
        
    def get_current_activity(self):
        return None
