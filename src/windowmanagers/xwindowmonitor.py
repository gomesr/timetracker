import subprocess
from threading import Thread

WINDOW_STATE = [ "/usr/bin/xprop", "-spy", "-id"]

class XWindowMonitor(Thread): 
    
    def __init__(self,id,callback):
        Thread.__init__ (self)
        self.id = id
        self.cmd = [x for x in WINDOW_STATE]
        self.cmd.append(id)
        self.done = False
        self.current = None
        self.callback = callback
    
    def cancel(self):
        self.done = True
    
    def run(self):
        process = subprocess.Popen(self.cmd, stdout = subprocess.PIPE)
        stdout = process.stdout
       
        line = str(stdout.readline(),'utf8');
        while ( line != None and not(self.done) ):
            title = None
            
            if ( line.find("WM_NAME(STRING) = ") != -1 ):
                title = line.replace("WM_NAME(STRING) = ","")
                title = title.replace("\n","")
            
            if ( line.find("WM_NAME(COMPOUND_TEXT) = ") != -1 ):
                title = line.replace("WM_NAME(COMPOUND_TEXT) = ","")
                title = title.replace("\n","")
               
            if ( title != None and title != self.current ): 
                self.callback(title)
                self.current = title
                
            line = str(stdout.readline(),'utf8')
            
        process.terminate()