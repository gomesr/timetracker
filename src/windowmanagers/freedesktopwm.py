'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A windowmanager that works for the X desktops that currently working
          on freedesktop. This includes KDE and Gnome, although Gnome refuses to
          create the freedesktop dbus path of org.freedesktop.ScreenSaver and 
          there is a small tweak to handle that in this windowmanager
'''
import os
from process import execute

xprop_cmd = "/usr/bin/xprop"
qdbus_cmd = "/usr/bin/qdbus"

active_window_match = ".*_NET_ACTIVE_WINDOW\(WINDOW\)\: window id #.*"
window_title_match = "^WM_ICON_NAME.*"

def is_supported():
    if ( not(os.path.exists(xprop_cmd)) ):
        raise Exception("Couldn't find application [%s]" % xprop_cmd) 

    if ( not(os.path.exists(qdbus_cmd)) ):
        raise Exception("Couldn't find application [%s]" % qdbus_cmd) 
    
    session = os.environ['DESKTOP_SESSION']
    return (session == 'gnome' or  session == 'kde')

def get_active_window_title():
    cmd = [ xprop_cmd, "-root" ]
    data = execute(cmd, active_window_match)
    window_id = data[data.find('#')+1:].strip()

    cmd = [ xprop_cmd, "-id", window_id ]
    data = execute(cmd, window_title_match)
    
    if ( data == None ):
        return None
    
    title = data.split("= \"")[1][:-1]
    title = ''.join(filter(lambda x: not((x in range(128,256))), title))
                    
    return title

def is_desktop_active():
    session = os.environ['DESKTOP_SESSION']
    
    if ( session == 'gnome' ):
        # /usr/bin/qdbus org.gnome.ScreenSaver / org.gnome.ScreenSaver.GetActive
        cmd = [ qdbus_cmd,
                "org.gnome.ScreenSaver",
                "/",
                "org.gnome.ScreenSaver.GetActive" ]
    elif ( session == 'kde' ):
        cmd = [ qdbus_cmd,
                "org.freedesktop.ScreenSaver",
                "/ScreenSaver",
                "org.freedesktop.ScreenSaver.GetActive" ]
    
    data = execute(cmd)
    return "false" in data
