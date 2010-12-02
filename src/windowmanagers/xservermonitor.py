import subprocess
from threading import Thread
from xwindowmonitor import XWindowMonitor

XPROP = [ "/usr/bin/xprop", "-root", "-spy"]
ACTIVE_WINDOW = "_NET_ACTIVE_WINDOW(WINDOW): window id # "

class XServerMonitor(Thread):

    def __init__(self,callback):
        Thread.__init__(self)
        self.callback = callback
        self.current = None
        self.done = False
    
    def cancel(self):
        self.done = True
        
    def run(self):
        process = subprocess.Popen(XPROP,stdout = subprocess.PIPE)
        stdout = process.stdout
        
        windowmonitor = None
        line = str(stdout.readline(),'utf8');
        while ( line != None and not(self.done) ):
            if ( line.find(ACTIVE_WINDOW) != -1 ):
                id = line.replace(ACTIVE_WINDOW,"")
                id = id.replace("\n","")
                
                if ( id != self.current ):
                    if ( windowmonitor != None ):
                        windowmonitor.cancel()
                   
                    windowmonitor = XWindowMonitor(id, self.callback)
                    windowmonitor.start() 
                    
                    self.current = id
                
            line = str(stdout.readline(),'utf8')
        
        if ( windowmonitor != None ):
            windowmonitor.cancel()
            
        process.terminate()
