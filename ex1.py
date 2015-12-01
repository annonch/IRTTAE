##########################
#  channon@hawk.iit.edu  #
##########################


#from verifier import *


def test(strr,states,cur_state):
    print('testing %s ' %strr)
    print(cur_state)


def update(state,time):
    print('updating continuous variables')
    print time
    t=float(time)
    rst=''
    if state == 'a':
        beta = t * 2
        rst+= 'beta:float:%s '%beta
        if beta > 50:
            rst += 'charlie:int:1 '
    if state == 'b':
        delta = time.time()
        rst+= 'delta:int:%s '% int(time.time())
    #if state == 'c':
        # 

    return rst
