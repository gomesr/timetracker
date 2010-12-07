
import ConfigParser
import os

global config
global wm

def load_config(configfile):
    global config
    config = ConfigParser.RawConfigParser()
    print("loading configuration [%s]" % configfile)
    config.read(configfile)
  
def get_config():
    """
    Get the currently loaded configuration file from the main timetracker 
    application. Any values set on this config will be saved once you call the
    save_config file.
    """
    global config
    return config

def save_config():
    """
    This function is used to save the application configuration whenever you 
    make any changes to the current configuration that you can obtain using the
    get_config function.
    """
    global config
    home = os.getenv("HOME")
    configfile = home + "/.timetracker.conf"
    config.write(open(configfile,"w"))
