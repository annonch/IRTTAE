#!/usr/bin/python
##########################
#  channon@hawk.iit.edu  #
##########################

'''
Siri-Like Real-Time Verification Engine for Timed Automata

'''
import threading # for timer module
import sys       # argv access
import time      # timed part of timed/ automata
import pyttsx    # voice speaks to us
import os        # for exiting

defs = __import__(sys.argv[3])
# use python verifier.py state.config init_state

class State:
    'This is the object for states'
    stateCount = 0
    # 0 indexed
    def __init__(self,n,g,trans,times):
        self.ID = State.stateCount
        State.stateCount +=1
        # make ID
        self.name = n
        guar = g.split(',')
        self.guards = dict()
        
        for i in guar:
            j= i.split(':')
            if j[1] == 'int':
                self.guards[j[0]] = int(j[2])
            elif j[1] == 'float':
                self.guards[j[0]] = float(j[2])
            else:
                self.guards[j[0]] = str(j[2])

        t = trans.split(',')
        self.transition_variable = t[0]
        self.transition_var_default = self.guards.get(self.transition_variable)
        self.transition_A = t[1]
        self.transition_B = t[2]

        tim = times.split(',')
        self.reset = int(tim[0])
        self.time_max = int(tim[1])

    def display(self):
        global engine
        print("ID: %s, Name: %s, Variables: %s, Transition Guard: %s, Max Time: %s, Clock Reset: %s "
              % (self.ID,self.name, self.guards,self.transition_variable,self.time_max, self.reset   ) )
        #engine.say("ID: %s, Name: %s, Variables: %s, Transition Guard: %s, Max Time: %s, Clock Reset: %s "
        #      % (self.ID,self.name, self.guards,self.transition_variable,self.time_max, self.reset   ) )

    def str_display(self):
        return("ID: %s, Name: %s, Variables: %s, Transition Guard: %s, Max Time: %s, Clock Reset: %s "
              % (self.ID,self.name, self.guards,self.transition_variable,self.time_max, self.reset   ) )
        
    def transition(self):
        global cur_state,states

        if self.guards.get(self.transition_variable) == self.transition_var_default:
            return 0 #cant transition, variable in default state
        if self.guards.get(self.transition_variable) < self.transition_var_default:
            cur_state = self.transition_A
            return -1 #change state to trans -1
        if self.guards.get(self.transition_variable) > self.transition_var_default:
            cur_state = self.transition_B
            return 1  # change state to trans 1

    def setup(self):
        global clock_time , cur_state
        if self.reset:
            reset_clock()

        if self.time_max:
            now = time.time()
            time_elps = now-clock_time
            time_rem = self.time_max - time_elps
            print('now: %s, elps: %s, rem: %s'
                  % (now,time_elps,time_rem))
            do_every(time_rem/2,    warn ,   cur_state,   2)
            do_every(time_rem - 5 , alert,   cur_state,   2)
            do_every(time_rem,      error_a, cur_state,   2)
        
def do_every(interval, worker_func, cur_state,iterations = 0):
    if iterations !=1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func, cur_state, 0 if iterations == 0 else iterations-1]
        ).start();
    if iterations != 2:
        worker_func(cur_state); 
                     
def warn(s):
    global cur_state, states
    if s != cur_state:
        return 0
    s_id = find_state(cur_state)
    say('Warning, the time is getting close to transition out of state: %s'
          % ( states[s_id].name  ) )
    print('Warning, the time is getting close to transition out of state: %s'
          % ( states[s_id].name  ) )
    
def alert(s):
    global cur_state
    if s != cur_state:
        return 0
    global states
    s_id = find_state(cur_state)
    say('Alert the time limit for: %s, will expire in 5 seconds'
          % (states[s_id].name ) )
    print('Alert the time limit for: %s, will expire in 5 seconds'
          % (states[s_id].name ) )
   
def error_a(s):
    global cur_state
    if s != cur_state:
        return 0
    global states,  clock_time
    s_id = find_state(cur_state)
    say('ERROR time violation at time: %s, state: %s'
          % ( str(int(time.time()-clock_time)) , states[s_id].name ) )
   
    print('ERROR time violation at time %s, state: %s'
          % ( str(int(time.time()-clock_time)) , states[s_id].name ) )
    
def read_states(state_conf):
    ''' read states config file from argv[1] '''
    global states 
    with open(state_conf,'r') as ins:
        for line in ins:
            if line[0] != '#':
                l = line.split()
                '''
                name = l[0]
                guards = l[1]
                trans = l[2]
                times = l[3]
                '''
                states.append(State(l[0],l[1],l[2],l[3]))

def reset_clock():
    ''' clock reset functionality of timed automata '''
    global clock_time
    clock_time = time.time()

def listen():
    #do listen
    if sys.argv[4] == 't':
        return raw_input('enter a command\n')
    elif sys.argv[4] == 'v':
        #get voice command
        print('enter a command')
        return 'gurg'
        
def transition_state():
    global engine
    ''' changes our current state to one of the transition if possible
        if not then we just maintain our current state             '''
    global states, cur_state
    s_id = find_state(cur_state)
    res = states[s_id].transition()
    s_id = find_state(cur_state)
    if res == -1:
        print('transitioning state to %s' %  states[s_id].name)
        say('transitioning state to: %s' %  states[s_id].name)
        states[s_id].setup()
    if res == 1:
        print('transitioning state to %s' %  states[s_id].name)
        say('transitioning state to: %s' %  states[s_id].name)
        states[s_id].setup()

def print_states(s):
    global states, cur_state, engine
    print(' ')
    for state in states:
        state.display()
    print('Current State is %s:' % cur_state)
    say('Current State is: %s' % cur_state)
    
def get_time(s):
    global clock_time, engine
    print('time elapsed: %s' % str(int(time.time()-clock_time)))
    say('time elapsed: %s' % str(int(time.time()-clock_time)))
                                      
def find_state(name):
    global states
    for i in states:
        if i.name == name:
            return i.ID

def exit(s):
    print('Cleaning up. \n Exiting....')
    os._exit(-1)
    sys.exit('Cleaning up. \n Exiting....')
   
def check_final(s):
    global final_state, cur_state, states
    if final_state == cur_state:
        say('Automata finished, %s, state reached' % final_state)
        print_states(s)
        say('should we save our current state variables to log?')
        ins = raw_input("save current state log? (y/N)")

        if ins == 'y':
            #log
            targ = open(logFile,'w')
            for i in states:
                targ.write(i.str_display()+'\n')
            targ.close()
            exit(s)
        else:
            exit(s)
        
def say(s):
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+50)
    voices= engine.getProperty('voices')
    #for voice in voices:
    engine.setProperty('voice', 'english-us')
    #print voice.id
    engine.say(s)
    try:
        a = engine.runAndWait() #blocks                 
    except RuntimeError:
        print('busy')
        
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

while True:
    ins = listen()
    say("new input provided: %s" % ins)
    line= ins.split()
    try:
        a = line[0]
        method_to_call = getattr(defs, a)
        method_to_call(line)
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
