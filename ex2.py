##########################
#  channon@hawk.iit.edu  #
##########################


#from verifier import *

import pywapi

def test(strr,states,cur_state):
    print('testing %s ' %strr)
    print(cur_state)


def update(state,time):
    print('updating continuous variables')
    print time
    t=float(time)
    rst=''
    if state == 'a':
        beta = t * 2.2
        rst+= 'beta:float:%s '%beta
        if beta > 50:
            rst += 'charlie:int:1 '
        elif pywapi.get_weather_from_noaa('KORD')['temp_c'] < 5:
            rst += 'charlie:int:-1 '
        
    if state == 'b':
        delta = pywapi.get_weather_from_noaa('KORD')['wind_mph']
        rst+= 'delta:float:%s '% delta
    return rst

def transition_handl():
    print('transition routine complete')
