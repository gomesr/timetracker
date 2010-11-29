'''
@author: Rodney Gomes <rodneygomes@gmail.com>

@summary: A simple notifier class to be implemented for all of the trackers 
          that you'd like to use while tracking activities.
'''

class Tracker(object):
    
    def start(self, name, category, description, tags = []):
        """
        The activity with the specified name has started and should be handled
        by this notifier.
        """
        raise NotImplementedError( "Need to implement" )
    
    def stop(self):
        """
        Stop any currently running notification. If none is present then just
        return.
        """
        raise NotImplementedError( "Need to implement" )
    
    def get_current_activity(self):
        """
        Return the currently running activity. If none is running or this 
        notifier doesn't have the capacity to track currently running activities
        then return None as well.
        """
        raise NotImplementedError( "Need to implement" )
