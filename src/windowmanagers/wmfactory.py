'''

'''

import freedesktopwm

def load_windowmanager():
    
    if ( freedesktopwm.is_supported() ):
        return freedesktopwm
    else:
        raise 
        