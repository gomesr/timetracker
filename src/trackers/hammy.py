'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A tracking tool to help the already existing hamster-applet for gnome
          to detect what the user is currently doing on his/her desktop. This is
          done by using some preset rules to identify the name of the activity 
          as well as some tags associated with that activity.
'''
import tracker

from hamster import client
from hamster.utils import stuff

class HamsterTracker(tracker.Tracker):
    
    def __init__(self):
        self.storage = client.Storage()
        
    def start(self, name, category, description, tags = []):
        fact = stuff.Fact(name, category, description, tags)
        return self.storage.add_fact(fact)
    
    def stop(self):
        id(None)
        
    def get_current_activity(self):
        facts = self.storage.get_todays_facts()
        
        if ( len(facts) > 1 ):
            return facts[-1].activity
        
        return None
    
    def destroy(self):
        self.storage.stop_tracking()
            