#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 18:56:37 2017

@author: wierie
"""

import random
import math
import time

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 18
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# < We focussed on some basic algorithms in the first half to get a lower level understanding.
# It might be better to continue to explore some prebuilt AI libraries to explore AI concepts more 
# efficiently and get a better understanding of the higher level concepts.(i'm not saying it is.its just an idea) >
# 
#####################################################
#####################################################



# Outputs a random integer, according to a multinomial
# distribution specified by probs.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0

class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior = [0.5, 0.5]
        self.transition = [[0.999, 0.001], [0.01, 0.99]]
        self.emission = [{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                         {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}]

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Computes the (natural) log probability of sequence given a sequence of states.
    def logprob(self, sequence, states):
        ###########################################
        # Start your code
        global max_prob_all
                
        
        return max_prob_all
        # End your code
        ###########################################

    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    max_prob_all = 0    
    def viterbi(self, sequence):
        ###########################################
        # Start your code   
        # **P-value in my comments refers to Probability value instead of p value in a statistical sense.
        global max_prob_all
        
        sequence = list(sequence)
        states = ('A/T','C/G')  #A/T rich or C/G rich  --> 0 and 1
        
#        start_p = {'A/T': 0.5, 'C/G': 0.5}    #priors        
        fprior = {states[0] : self.prior[0], states[1]: self.prior[1]} 
                   
        #transition values
        ftrans = {
                   states[0] : {states[0]: self.transition[0][0], states[1]: self.transition[0][1]},
                   states[1] : {states[0]: self.transition[1][0], states[1]: self.transition[1][1]}, 
                   }
         
        femis = {
                states[0] : self.emission[0], #A/T : emission values
                states[1] : self.emission[1]  #C/G : emission values
                }  
                         
        Viterbilist = [{}] # list that will record the P-value and the previous state. 
        
        
        for state in states: # set the starting point using the priors and get the first probaility pair of A/T and C/G
            
            firstset = math.log(fprior[state]) + math.log(femis[state][sequence[0]])#convert to log values
                                    
            Viterbilist[0][state] = {
                        "P": firstset, # prior values of the state times the emssion values of the state of the first sequence.
                        "PrevState": None #Previous state is None because it is the starting point.
                        }      
              
        for seq in range(1, len(sequence)): # start at sequence 1 (0 was starting point)    
          
            Viterbilist.append({}) # append empty dictionary to make ready for next pair of values
            for state in states:       
                # the previous Probability value times the transition value for each state and get the maximum probability                       
                trans_probmax = max( Viterbilist[seq - 1][eachstate]["P"] + math.log(ftrans[eachstate][state]) for eachstate in states)                                   
                                                           
                #revisit both states to assign the max P-value to the next node. take max P-value 
                #times the emission value of the state for the current sequence.
                #relative to the next node the current node should point to the previous state 
                #this will be needed for traceback later.
                for state_back in states:
                    if Viterbilist[seq - 1][state_back]["P"] + math.log(ftrans[state_back][state]) == trans_probmax:
                        Viterbilist[seq][state] = {"P": trans_probmax + math.log(femis[state][sequence[seq]]), 
                                                   "PrevState": state_back}                
                        break #end once the state is found for which the maximum P-value was found.  


        backtrackcollector = [] # make a new array to record the states this is for recording the backtrack. 
          
        # this part is for finding which one of the last states has the highes probability max_prob_all
        # it is the first element that goes in the backtrack list
        
        # with this line of code we now know what the highest values is
        highestvalue = max( Viterbilist[-1][eachstate]["P"] for eachstate in states)
        
        #this part is to determine for which of the state this highest value belongs to
        higheststate =""
        for state in states:
            if Viterbilist[-1][state]["P"] == highestvalue:
                higheststate = state # we know for which the highest value belongs to so record which state that is
                
        
        
        backtrackcollector.append(higheststate) # append highest state to the backtracking array. this is the starting point of the backtracking     
        
        progress = 0 # used to track the progress. total length is 5.2 million and this will increment to that.

        prev = higheststate   # set previous node to the highest(last node) so that traceback can start here
                
        for backtrackpos in range(1, len(Viterbilist)): # total length minus the last and first one(-2), keep decrementing by 1             
#            starttime = time.clock()
            backtrackcollector.append(Viterbilist[len(Viterbilist) - backtrackpos][prev]["PrevState"]) # insert at the beginning of the list
            prev = Viterbilist[len(Viterbilist) - backtrackpos][prev]["PrevState"] # choose the next pari of values of the Viterbilist 
#            endtime = time.clock() 
            progress += 1
            print("progress", progress)
#            print(endtime - starttime)
#            which we populated before. we are indexing from the end towards the beginning. 
        
        #this is a global variable to be used in the logprob function it contains the maximum probability found
        max_prob_all = max(value["P"] for value in Viterbilist[-1].values())
                
        viterbystring = "" 
        
        #reading the backtracking list from back to front to reverse the order and convert the 
        #labels for the states to "0"'s and "1"'s . "A/T" = 0 and "C/G" = 1
        for state in range(len(backtrackcollector)-1,-1,-1): 
            if backtrackcollector[state] == "A/T":
                viterbystring += "0"
            else:
                viterbystring += "1"

        return viterbystring
        # End your code
        ###########################################

def read_sequence(filename):
    with open(filename, "r") as f:
        return f.read().strip()

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, logprob, states):
    with open(filename, "w") as f:
        f.write(str(logprob))
        f.write("\n")
        for state in range(2):
            f.write(str(states.count(str(state))))
            f.write("\n")
        f.write("".join(map(str, states)))
        f.write("\n")

hmm = HMM()

#sequence = read_sequence("small.txt")
#viterbi = hmm.viterbi(sequence)
#logprob = hmm.logprob(sequence, viterbi)
#write_output("my_small_output.txt", logprob, viterbi)

starttime = time.clock()
sequence = read_sequence("ecoli.txt")
viterbi = hmm.viterbi(sequence)
logprob = hmm.logprob(sequence, viterbi)
write_output("ecoli_output.txt", logprob, viterbi)
endtime = time.clock()
print("running time", endtime - starttime)

