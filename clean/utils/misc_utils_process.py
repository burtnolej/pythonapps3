from subprocess import Popen, STDOUT, PIPE
from time import sleep
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils_enum import enum
from misc_utils import Log
from os import remove, kill
import signal
import unittest

log = Log()

def process_start(cmdlineargs,stdin=True):
    ''' pass stdin=True when you want the process to wait for 
    stdin '''
    args = dict(stderr=STDOUT,stdout=PIPE)
    
    if stdin == True:
        args['stdin'] = PIPE
    
    p = Popen(cmdlineargs,**args)
    
    log.log(__name__,3,"started process","pid=",str(p.pid),"cmd="," ".join(cmdlineargs))
    return(p)

def process_stdin(process,stdinstr):
    ''' pass stdin to a process waiting for stdin '''
    return(process.communicate(input=stdinstr))

def process_kill(pid):
    ''' accepts str or int'''
    try:
        _pid = int(pid)
    except ValueError:
        raise Exception('requires an int or int as string')

    log.log(__name__,3,"killed process","pid=",str(_pid))
    return(kill(_pid,signal.SIGTERM))
    
def process_instances_get(match):

    cmd = ['ps','-ef']
    p = process_start(cmd)
    processlist = p.stdout.read()
    
    # put back into string format for grep -v an remove blank last item 
    process_str = "".join(list(processlist)[:-1]) 
    
    cmd = ['grep',match]
    pgrep1 = process_start(cmd,stdin=True)
    matches =  process_stdin(pgrep1,process_str)
    #pgrep1.communicate(input=process_str)
       
    # put back into string format for grep -v an remove blank last item 
    matches_str = "".join(list(matches)[:-1]) 
         
    cmd = ['grep','-v','defunct']
    pgrep2 = process_start(cmd,stdin=True)
    
    nondefunctmatches = process_stdin(pgrep2,matches_str)[0].split("\n")[:-1]

    pid = [(match.split(" ")[2],match.split(" ")[4]) for match in nondefunctmatches]
    
    return(pid)