'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A windowmanager that works for the X desktops that currently working
          on freedesktop. This includes KDE and Gnome, although Gnome refuses to
          create the freedesktop dbus path of org.freedesktop.ScreenSaver and 
          there is a small tweak to handle that in this windowmanager
'''

from windowmanager import WindowManager
from xservermonitor import XServerMonitor

from process import execute

import os

class FreedesktopManager(WindowManager):
    
    def start(self, callback):
        self.monitor = XServerMonitor(callback)
        self.monitor.start()
    
    def stop(self): 
        self.monitor.cancel()

    def is_supported():
        session = os.environ['DESKTOP_SESSION']
        return (session == 'gnome' or  session == 'kde')

    def is_desktop_active():
        session = os.environ['DESKTOP_SESSION']
        
        if ( session == 'gnome' ):
            # /usr/bin/qdbus org.gnome.ScreenSaver / org.gnome.ScreenSaver.GetActive
            cmd = [ "/usr/bin/qdbus",
                    "org.gnome.ScreenSaver",
                    "/",
                    "org.gnome.ScreenSaver.GetActive" ]
        elif ( session == 'kde' ):
            cmd = [ "/usr/bin/qdbus",
                    "org.freedesktop.ScreenSaver",
                    "/ScreenSaver",
                    "org.freedesktop.ScreenSaver.GetActive" ]
        
        data = execute(cmd)
        return "false" in data

    is_desktop_active = staticmethod(is_desktop_active)
    is_supported = staticmethod(is_supported)
