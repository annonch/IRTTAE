##########################
#  channon@hawk.iit.edu  #
##########################


#from verifier import *

#import pywapi
import time

def test(strr,states,cur_state):
    print('testing %s ' %strr)
    print(cur_state)


def update(state,time):
    print('updating continuous variables')
    print time
    t=float(time)
    rst=''
    if state == 's3':
        glucose = get_external_reading('g')
        rst+= 'glucose:float:%s '%glucose
        
    return rst

def transition_handl():
    print('transition routine complete')

def get_external_reading(s):
    return time.time()
