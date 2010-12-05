'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: 
          
'''
from threading import Thread

class WindowManager(Thread):
    
    def start(self, callback):
        raise NotImplemented("implement this function")
    
    def stop(self): 
        raise NotImplemented("implement this function")
    
    def is_desktop_active():
        raise NotImplemented("implement this function")
    
    def is_supported():
        raise NotImplemented("implement this function")
    
    is_desktop_active = staticmethod(is_desktop_active)
    is_supported = staticmethod(is_supported)
    

        
        

        
    