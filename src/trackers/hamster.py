'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A tracking tool to help the already existing hamster-applet for gnome
          to detect what the user is currently doing on his/her desktop. This is
          done by using some preset rules to identify the name of the activity 
          as well as some tags associated with that activity. With this 
          information this tool then instructs the hamster-applet using the 
          hamster-cli to start/stop activities.
'''
import process
import tracker
import os

hamster_cmd = "/usr/bin/hamster-cli"
    
class HamsterTracker(tracker.Tracker):
    
    def __init__(self):
        if ( not(os.path.exists(hamster_cmd)) ):
            raise Exception("Couldn't find application [%s]" % hamster_cmd) 
    
    def start(self, name, category, description, tags = []):
        activity = to_activity_string(name, category, description, tags)
        cmd = [ hamster_cmd, "start", activity ] 
        id = process.execute(cmd)
    
    def stop(self):
        cmd = [ hamster_cmd, "stop" ]
        id = process.execute(cmd)
        
    def get_current_activity(self):
        cmd = [ hamster_cmd, "list" ]
        data = process.execute(cmd).split("\n")
       
        if ( len(data) > 2 ): 
            n = len(data)-1
            if ( data[n] ):
                return data[n].split("| ")[1]

        return None

def to_activity_string(activity,category,description,tags):
    """
    Formats the activity details into a string that is the accepted syntaxe for 
    the hamster cli utility. Currently that format looks like so:
    
    activity@category, description #tag1..#tagn
    
    """
    string = []
    
    if ( category == None ):
        category = " "
    
    if ( description == None ):
        description = " "
        
    string.append(activity)
    string.append("@%s" % category)
    string.append(",%s" % description)
      
    for tag in tags:
        string.append(" #%s" % tag)
            
    return ''.join(string) 