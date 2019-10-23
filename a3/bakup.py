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
        
        obs = list(sequence)
        states = ('A/T','C/G')  #A/T rich or C/G rich
        start_p = {'A/T': 0.5, 'C/G': 0.5}    #priors
               
        trans_p = {
                   'A/T' : {'A/T': 0.999, 'C/G': 0.001},
                   'C/G' : {'A/T': 0.01, 'C/G': 0.99},
                   }

        emit_p = {
                'A/T' : {"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                'C/G' : {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}
                }        
        V = [{}]
        
        for st in states:
            V[0][st] = {
                        "prob": start_p[st] * emit_p[st][obs[0]], 
                        "prev": None
                        }                
                           
        for t in range(1, len(obs)):
            V.append({})
            for st in states:                               
                max_tr_prob = max(V[t-1][prev_st]["prob"] * trans_p[prev_st][st] for prev_st in states)                                   
                for prev_st in states:
                    if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                        max_prob = max_tr_prob * emit_p[st][obs[t]]
                        V[t][st] = {"prob": max_prob, "prev": prev_st}
                        break
                        
        opt = []
        # The highest probability
        max_prob = max(value["prob"] for value in V[-1].values())
        previous = None
        # Get most probable state and its backtrack    
        for st, data in V[-1].items():
            if data["prob"] == max_prob:
                opt.append(st)
                previous = st
                break
        # Follow the backtrack till the first observation

        for t in range(len(V) - 2, -1, -1):
            opt.insert(0, V[t + 1][previous]["prev"])
            previous = V[t + 1][previous]["prev"]
        
        print(math.log(max_prob))
        
        
        viterbystring = ""                
        for state in opt:
            if state == "A/T":
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

sequence = read_sequence("small.txt")
viterbi = hmm.viterbi(sequence)
logprob = hmm.logprob(sequence, viterbi)

write_output("my_small_output.txt", logprob, viterbi)


#sequence = read_sequence("ecoli.txt")
#viterbi = hmm.viterbi(sequence)
#logprob = hmm.logprob(sequence, viterbi)
#write_output("ecoli_output.txt", logprob, viterbi)



