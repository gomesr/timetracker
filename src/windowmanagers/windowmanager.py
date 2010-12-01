'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A window manager that defines the desktop functions that are required
          by timetracker to track what the user is doing at any given moment.
          
          * get_active_window_title
            This function should return the complete title of the application
            that is currently active (or in other words has the users focus) on 
            the desktop. 
            
          * is_desktop_active
            Should return a boolean that states if the desktop is active, which
            means that the screen isn't locked or the lid of the laptop isn't
            closed. When this method returns false then timetracker will set
            the activity to "Away" since the user wasn't really at his desk 
            doing anything.
          
'''

def get_active_window_title():
    raise NotImplemented("Implement this function for your own window manager")

def is_desktop_active():
    raise NotImplemented("Implement this function for your own window manager")
        
    