'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: The window manager factory used to load the appropriate windowmanager
          or raise an exception to let the end user know that there current
          environment is not supported.
'''

import freedesktopwm

def load_windowmanager():
    
    if ( freedesktopwm.is_supported() ):
        return freedesktopwm
    else:
        raise 
        