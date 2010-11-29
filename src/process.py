import subprocess
import re

def execute(cmd, match_line = None):
    """
    Execute the specified cmd array and if the match_line is set to something
    other than None then it will be used as a regular expression to match 
    the first line in the is a good match and will be returned. In the case that
    you don't specify a match_line then all of the output will be returned.
    """
    p = subprocess.Popen(cmd, stdin=None, stdout=subprocess.PIPE) 
       
    if p.wait() != 0:
        _,stderr = p.communicate()
       
        if ( stderr != None ): 
            for line in stderr.readlines():
                print(line)
                
        print("failed to execute %s, exited with %d" % (cmd, p.wait()))
        raise
    else:
        if ( match_line == None ):
            # return all lines
            data = []
            for line in p.stdout.readlines():
                data.append(str(line, 'utf8'))
                
            return '\n'.join(data)
        else:
            for line in p.stdout.readlines():
                line = str(line, 'utf8')
                if ( re.match(match_line, line) ):
                    return line
            
    return None
