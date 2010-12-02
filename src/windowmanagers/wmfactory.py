'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: The window manager factory used to load the appropriate windowmanager
          or raise an exception to let the end user know that there current
          environment is not supported.
'''

from freedesktopwm import FreedesktopManager 

def load_windowmanager():
    
    if ( FreedesktopManager.is_supported() ):
        return FreedesktopManager()
    else:
        raise 
        