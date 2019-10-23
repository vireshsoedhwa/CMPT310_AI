import random
import math

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 0
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
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
#        sequencefromgen = self.generate_sequence(states)
        
        return 100
        # End your code
        ###########################################

    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        ###########################################
        # Start your code   
        
        # **P-value in the notes refers to Probability value instead of p value in a statistical sense.
        
        sequence = list(sequence)
        states = ('A/T','C/G')  #A/T rich or C/G rich  --> 0 and 1
        
#        start_p = {'A/T': 0.5, 'C/G': 0.5}    #priors        
        fprior = {states[0] : self.prior[0], states[1]: self.prior[1]} 
                   
        ftrans = {
                   states[0] : {states[0]: self.transition[0][0], states[1]: self.transition[0][1]},
                   states[1] : {states[0]: self.transition[1][0], states[1]: self.transition[1][1]}, 
                   }
         
        femis = {
                states[0] : self.emission[0], #A/T : emission values
                states[1] : self.emission[1]  #C/G : emission values
                }  
                         
        Viterbilist = [{}]
      
        for state in states: # set the starting point using the priors and get the first probaility pair of A/T and C/G
            Viterbilist[0][state] = {
                        "P": fprior[state] * femis[state][sequence[0]], # prior values of the state times the emssion values of the state of the first sequence.
                        "PrevState": None #Previous state is None because it is the starting point.
                        }      
                   
        for seq in range(1, len(sequence)): # start at sequence 1 (0 was starting point)    
            Viterbilist.append({}) # append empty dictionary to make ready for next pair of values
            for state in states:       
                # the previous Probability value times the transition value for each state and get the maximum probability                       
                trans_probmax = max(Viterbilist[seq-1][eachstate]["P"] * ftrans[eachstate][state] for eachstate in states)                                   
                
                #revisit both states to assign the max P-value to the next node. take max P-value 
                #times the emission value of the state for the current sequence.
                #relative to the next node the current node should point to the previous state 
                #this will be needed for traceback later.
                for state_back in states:
                    if Viterbilist[seq-1][state_back]["P"] * ftrans[state_back][state] == trans_probmax:
                        Viterbilist[seq][state] = {"P": trans_probmax * femis[state][sequence[seq]], 
                                                   "PrevState": state_back}
                        break #end once the state is found for which the maximum P-value was found.  
        
        #check which state has the highest ending probability; record state and the Probability
        
        highestvalue = 0   # to keep track of highest P-Value
        higheststate = ""  # the state of that value
        for state, data in Viterbilist[-1].items(): # index -1 is last sequence        
            if data["P"] > highestvalue:                
                highestvalue = data["P"] # record P-Value if it is larger than previous
                higheststate = state  # record the state with highest P-Value. this is the last value
                #and the starting point for our traceback
                    
        viterbycollector = [] # make a new array to record the states as we are doing the backtrack. 
        prev = higheststate   # set previous node to the highest(last node) so that traceback can start here
        for t in range(len(Viterbilist) - 2, -1, -1): # total length minus the last and first one(-2), keep decrementing by 1 
            viterbycollector.insert(0, Viterbilist[t + 1][prev]["PrevState"]) # insert at the beginning of the list
            prev = Viterbilist[t + 1][prev]["PrevState"] # choose the next pari of values of the Viterbilist 
            #which we populated before. we are indexing from the end towards the beginning. 

        
#        viterbycollector = []
#        # The highest probabilitstatey
#        max_prob_all = max(value["P"] for value in Vitlist[-1].values())
#        prev = None
#        # Get most probable state and its backtrack    
#        for state, data in Vitlist[-1].items():
#            if data["P"] == max_prob_all:
#                viterbycollector.append(state)
#                prev = state
#                break
#        # Follow the backtrack till the first observation
#
#        for t in range(len(Vitlist) - 2, -1, -1):
#            viterbycollector.insert(0, Vitlist[t + 1][prev]["P_prev"])
#            prev = Vitlist[t + 1][prev]["P_prev"]
#        
#        print(viterbycollector)
#        print(math.log(max_prob_all))
#        
#        
        viterbystring = ""                
        for state in viterbycollector:
            if state == "A/T":
                viterbystring += "0"
            else:
                viterbystring += "1"
                
#        print(viterbystring)
#        return viterbystring
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

sequence = read_sequence("small.txt")
viterbi = hmm.viterbi(sequence)
#logprob = hmm.logprob(sequence, viterbi)
#
#write_output("my_small_output.txt", logprob, viterbi)


#sequence = read_sequence("ecoli.txt")
#viterbi = hmm.viterbi(sequence)
#logprob = hmm.logprob(sequence, viterbi)
#write_output("ecoli_output.txt", logprob, viterbi)



