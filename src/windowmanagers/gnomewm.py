'''
@author: Rodney Gomes 
@contact: rodneygomes@gmail.com 

@summary: A gnome window manager that uses a few xlib command line tools to 
          figure out the title of the currently active desktop window.
'''
from process import execute

root_cmd = ["/usr/bin/xprop","-root"]
active_window_match = ".*_NET_ACTIVE_WINDOW\(WINDOW\)\: window id #.*"

window_cmd = ["xprop", "-id", ""]
window_title_match = "^WM_ICON_NAME.*"

def get_active_window_title():
    data = execute(root_cmd, active_window_match)
    window_id = data[data.find('#')+1:].strip()

    window_cmd[2] = window_id
    data = execute(window_cmd, window_title_match)
    
    if ( data == None ):
        return None
    
    title = data.split("= \"")[1][:-2]
    title = ''.join(filter(lambda x: not((x in range(128,256))), title))
                    
    return title
    
    