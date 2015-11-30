##########################
#  channon@hawk.iit.edu  #
##########################

from verifier import *



'''
say("hello, timed automata starting")

states = []
read_states(sys.argv[1])
cur_state = sys.argv[2]
final_state= sys.argv[5]
logFile=sys.argv[6]

time.sleep(0.5)
clock_time=time.time()
s_id = find_state(cur_state)
states[s_id].setup()
'''

while True:
    ins = listen()
    say("new input provided: %s" % ins)
    line= ins.split()
    s_id= find_state(cur_state)
    try:
        a = line[0]
        method_to_call = getattr(defs, a)
        method_to_call(line, states, s_id)
    except AttributeError:
        print('not found in custom trying local functions')
        try:
            a = line[0]
            eval(a+'(line)')
        except NameError:
            print('exception caught, looking in guards')
            s_id = find_state(cur_state)
            if line[1] == 'int':
                states[s_id].guards[line[0]] = int(line[2])
            if line[1] == 'float':
                states[s_id].guards[line[0]] = float(line[2])
            if line[1] == 'str':
                states[s_id].guards[line[0]] = str(line[2])
    print_states('a')
    #check if we can transition
    transition_state()
    check_final('a')
                                                                                                                                        
