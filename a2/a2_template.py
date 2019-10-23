import random
import time
import copy
import numpy as np

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 20
#####################################################
#####################################################
answer = {}
#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)

# I found the bayesian networks interesting. 
# The value of this course will improve greatly if we explore AI frameworks
# and libraries. This way the understanding of the python language will not be 
# a limitation and we can focus more on the concepts of AI instead of the implementation


#####################################################
#####################################################


# A clause consists of a set of symbols, each of which is negated
# or not. A clause where
# clause.symbols = {"a": 1, "b": -1, "c": 1}
# corresponds to the statement: a OR (NOT b) OR c .
class Clause:
    def __init__(self):
        pass

    def from_str(self, s):
        s = s.split()
        self.symbols = {}
        for token in s:
            if token[0] == "-":
                sign = -1
                symbol = token[1:]
            else:
                sign = 1
                symbol = token
            self.symbols[symbol] = sign

    def __str__(self):
        tokens = []
        for symbol,sign in self.symbols.items():
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            tokens.append(token)
        return " ".join(tokens)

# A SAT instance consists of a set of CNF clauses. All clauses
# must be satisfied in order for the SAT instance to be satisfied.
class SatInstance:
    def __init__(self):
        pass

    def from_str(self, s):
        self.symbols = set()
        self.clauses = []
        for line in s.splitlines():
            clause = Clause()
            clause.from_str(line)
            self.clauses.append(clause)
            for symbol in clause.symbols:
                self.symbols.add(symbol)
        self.symbols = sorted(self.symbols)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s

    # Takes as input an assignment to symbols and returns True or
    # False depending on whether the instance is satisfied.
    # Input:
    # - assignment: Dictionary of the format {symbol: sign}, where sign
    #       is either 1 or -1.
    # Output: True or False
    def is_satisfied(self, assignment):
        ###########################################
        # Start your code
        
        results = []
        for clause in self.clauses:            
            for key in  clause.symbols.keys():
                if key in assignment:
                    if clause.symbols[key] == assignment[key]: # if both values match                       
                        results.append([True]) # means this key was previously recorded
                        break    # that also means that it was true so break and continue checking next one
            if any(results): # here i get rid of all clauses that are true(search space reduction)
                self.clauses.remove(clause)       
# if the numer of clauses equals the numbers of symbols in our *assignment
# that means that all of them are true. so the conjunction of this is true
# *only symbols that were true before are recorded in our assignment
        if len(results) == len(self.clauses): 
            return True              
        return False

# The condition to be NOT satisfied is that at least one of the clauses
# is false. the list of results contains symbols per clause. if all symbols 
#are false then that clause is false
# of false symbols should be equal to the number of clauses        

    def is_notsatisfied(self, assignment):
        for clause in self.clauses:
            results = [] 
            for key in clause.symbols.keys():
                if key in assignment:
                    if clause.symbols[key] !=  assignment[key]:
                        results.append(False) # this clause is false
            if len(results) == len(clause.symbols) and all(val == False for val in results):
                return True            
        return False 
        # End your code
        ###########################################

# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: SAT instance
# Output: Dictionary of the format {symbol: sign}, where sign
#         is either 1 or -1.
def solve_dpll(instance):
    ###########################################
    # Start your code
    
    assignment = {}

    def FPS(symbols, clauses, assignment):               
        for symbol in symbols:        
            if not(symbol in assignment.keys()):                            
                findings = []
                for clause in clauses:
                    if (symbol in clause.symbols):
                        findings.append(clause.symbols[symbol])    
                if(len(findings) != 0):
                    if(findings.count(findings[0]) == len(findings)):
#                        print("FPS found for", symbol)
                        P = symbol
                        value = findings[0]
                        return P, value                      
        return None, None    
    
    def FUC(clauses, assignment):        
        P = None
        value = None        
        for clause in clauses:
            if len(clause.symbols) == 1:                
                keys = clause.symbols.keys()
                for key in keys:
                    P = key
                    value = clause.symbols[key]
                    return P, value        
#        print('FUC found P {} value {}'.format(P, value))                
        return P, value  
       
   
    def FIRST(symbols):  # choose first symbol     
        P = symbols[0]
        return P
   
    def REST(symbols):   #Choose all the other values after the first one.      
        return symbols[1:]
    
    def additem(answerdict, item, value):  # used to add The proposition to the assignment dictionary
        copyass = copy.deepcopy(answerdict)         
        copyass.update({item : value})        
        return copyass   
    
    
    def DPLL(clauses, symbols, assignment):            
        global answer
        if instance.is_satisfied(assignment):            
            print(assignment) 
            answer = assignment
            return True  
        elif instance.is_notsatisfied(assignment):   # returns confirmation if evaluates to falsse.
            return False                  
            
#        results = [] 
#        for clause in clauses:
#            for key in clause.symbols.keys():
#                if key in assignment:
#                    if clause.symbols[key] ==  assignment[key]:
#                        results.append(True)
#                        break
#            if any(results):
#                clauses.remove(clause)                        

        fpsP1, fpsval = FPS(symbols, clauses, assignment) #find pure symbol
        
        if(fpsP1 != None): # if pure function is found remove the value from symbols and add the symbols to our assignment
                
            if fpsP1 in symbols: 
                symbols.remove(fpsP1)  
                assignment.update({fpsP1 : fpsval})
                return DPLL(clauses, symbols, assignment)
              
        fucP2, fucval = FUC(clauses, assignment) # find unit clause
       
        if(fucP2 != None):  # if unit clause if found add that symbol to our assignment dictionary and set the value
            if fucP2 in symbols: 
                symbols.remove(fucP2) # remove the symbol from the list of all symbols to avoid having to search through it again
                assignment.update({fucP2 : fucval})
                return DPLL(clauses, symbols, assignment)
          
        if len(symbols) != 0: # to avoid slicing the list if there are no symbols in the list
            P3 = FIRST(symbols) #  head of the list
            rest = REST(symbols) #tail of the list       

                      
        return DPLL(clauses, rest, additem(assignment, P3, 1)) or DPLL(clauses, rest, additem(assignment, P3, -1))
            
    starttime = time.clock()  
    DPLL(instance.clauses, instance.symbols, assignment)
    endtime = time.clock()   
    print("instance time",(endtime - starttime))
            
    return answer
    # End your code
    ###########################################

with open("small_instances.txt", "r") as input_file:
    instance_strs = input_file.read()

instance_strs = instance_strs.split("\n\n")

with open("small_assignments_inferred.txt", "w") as output_file:
    starttime = time.clock()  
    for instance_str in instance_strs:
        if instance_str.strip() == "":
            continue
        instance = SatInstance()
        instance.from_str(instance_str)
        assignment = solve_dpll(instance)
        
        for symbol_index, (symbol,sign) in enumerate(assignment.items()):
            if symbol_index != 0:
                output_file.write(" ")
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            output_file.write(token)
        output_file.write("\n")
    endtime = time.clock()   
    print("total time",(endtime - starttime))















