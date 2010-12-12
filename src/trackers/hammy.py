'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A tracking tool to help the already existing hamster-applet for gnome
          to detect what the user is currently doing on his/her desktop. This is
          done by using some preset rules to identify the name of the activity 
          as well as some tags associated with that activity.
'''
import tracker
import threading
import gobject

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

from hamster import client
from hamster.utils import stuff
from hamster import db

'''
Had to implement this because retrieve all of the facts of the day in order to 
just know what is the last task is too heavy and makes both the applet and this
application perform badly. By querying the very last row and validating it is
in course, this is a very efficient method. 

Had to be its own thread because sqlite doesn't like it when two threads attempt
to access the same sqlite connection.
'''
class DBThread(threading.Thread):
    
    def __init__(self, storage):
        threading.Thread.__init__(self)
            
        from hamster.lib import i18n
        i18n.setup_i18n()

        self.sem = threading.Semaphore(0)
        self.done = threading.Semaphore(0)
        self.activity = None
        self.running = True
        self.storage = storage
    
    def cancel(self): 
        self.running = False
        self.sem.release()
        
    def run(self):
        loop = gobject.MainLoop()
        self.storagedb = db.Storage(loop)
        while ( self.running ):
            self.sem.acquire(1)
            
            query = """
                   SELECT a.id AS id,
                          a.start_time AS start_time,
                          a.end_time AS end_time,
                          a.description as description,
                          b.name AS name, b.id as activity_id,
                          e.name as tag
                     FROM facts a
                LEFT JOIN activities b ON a.activity_id = b.id
                LEFT JOIN categories c ON b.category_id = c.id
                LEFT JOIN fact_tags d ON d.fact_id = a.id
                LEFT JOIN tags e ON e.id = d.tag_id
                ORDER BY a.id DESC
                LIMIT 1
            """
            aux = self.storagedb.fetchall(query)
            self.activity = None
            if ( aux != None and len(aux) > 0 ):
                fact = aux[0]
                if ( fact['end_time'] == None ):
                    ''' end_time == None then the task is still running '''
                    name = fact['name']
                   
                    description = fact['description'] 
                    if ( description == None ):
                        description = ""
                        
                    tag = fact['tag']
                    tags = ""
                    
                    if ( tag != None ):
                        tags = tag.split(' ')
                        tags = ''.join(["#%s" % tag for tag in tags])
                        
                    self.activity = "%s, %s %s" % (name,description,tags)
                
            self.done.release()
        
    def get_current_activity(self):
        self.sem.release()
        self.done.acquire(1)
        return self.activity

class HamsterTracker(tracker.Tracker):
    
    def __init__(self):
        global onchange 
        self.storage = client.Storage()
        self.dbthread = DBThread(self.storage) 
        self.dbthread.start()
        
    def start(self, name, category, description, tags = []):
        fact = stuff.Fact(name, category, description, tags)
        return self.storage.add_fact(fact)
    
    def stop(self):
        id(None)
        
    def get_current_activity(self):
        return self.dbthread.get_current_activity()
    
    def destroy(self):
        self.storage.stop_tracking()
        self.dbthread.cancel()
            