'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: This tracker is used for testing and basically logs each of the 
          start/stops of activites to a log file
'''
import tracker
import time

class ActivityLogTracker(tracker.Tracker):

    def __init__(self):
        self.log = open('activites.log', 'w')
        self.name = None
    
    def start(self, name, category, description, tags=[]):
        current = time.asctime()
        tagstr = ','.join(tags)
        
        self.current_activity = "%s@%s [%s] {%s}" % (name,category,description,tagstr)
        self.log.write("%s - START %s\n" % (current, self.current_activity))
        self.log.flush()
        self.name = name
        
    def stop(self):
        current = time.asctime()
        self.log.write("%s - STOP  %s\n" % (current, self.current_activity))
        self.log.flush()
        self.name = None
        
    def get_current_activity(self):
        return self.name

