import subprocess
import re

def execute(cmd, match_line = None):
    """
    Execute the specified cmd array and if the match_line is set to something
    other than None then it will be used as a regular expression to match 
    the first line in the is a good match and will be returned. In the case that
    you don't specify a match_line then all of the output will be returned.
    """
    p = subprocess.Popen(cmd,
                         stdin=None,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE) 
    stdout,stderr = p.communicate()
   
    # not very pretty but for now this will work 
    stdout = stdout.split('\n')
    stderr = stderr.split('\n')
       
    if p.wait() != 0:
        if ( stderr != None ): 
            for line in stderr:
                print(line)
                
        print("failed to execute %s, exited with %d" % (cmd, p.wait()))
        raise
    else:
        if ( match_line is None ):
            # return all lines
            return '\n'.join(stdout)
        else:
            for line in stdout:
                if ( re.match(match_line, line) ):
                    return line
            
    return None
