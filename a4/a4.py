#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 01:43:20 2017

@author: wierie
"""

import random
import math
import time
import copy

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 80
#####################################################
#####################################################


def logistic(x):
    return 1.0 / (1.0 + math.exp(-x))

def logistic_derivative(x):
    return logistic(x) * (1-logistic(x))

class Neuron:
    def __init__(self, attribute_weights, neuron_weights, bias_weight):
        # neuron.attribute_weights[i] = Weight of input attribute i as input to this neuron
        self.attribute_weights = attribute_weights
        # neuron.neuron_weights[i] = Weight of neuron j as input to this neuron
        self.neuron_weights = neuron_weights
        self.bias_weight = bias_weight

class ANN:
    def __init__(self, num_attributes, neurons):
        # Number of input attributes.
        self.num_attributes = num_attributes
        # Number of neurons. neurons[-1] is the output neuron.
        self.neurons = neurons
        for neuron_index, neuron in enumerate(self.neurons):
            for input_neuron, input_weight in neuron.neuron_weights.items():
                assert(input_neuron < neuron_index)

    # Calculates the output of the output neuron for given input attributes.
    def calculate(self, attributes):
        ###########################################
        # Start your code
                
#        calculate() applies the neural network to a given 
#        input and returns the output of the network (i.e. the output of the last neuron).

        #neurons 0 and 1 are hidden layer neurons. 
        #neurons 2 is output neuron. 
        
        # put all the neuron weights in variables for more clarity.
        i1 = attributes[0]
        i2 = attributes[1]
        
        w13 = self.neurons[0].attribute_weights.get(0)
        w23 = self.neurons[0].attribute_weights.get(1)
        w14 = self.neurons[1].attribute_weights.get(0)
        w24 = self.neurons[1].attribute_weights.get(1)

        w35 = self.neurons[2].neuron_weights.get(0)
        w45 = self.neurons[2].neuron_weights.get(1)

        b03 = self.neurons[0].bias_weight
        b04 = self.neurons[1].bias_weight
        b05 = self.neurons[2].bias_weight
        
        #weigthed sums of all the inputs to the specific neuron.         
        a3in = i1 * w13 + i2 * w23 - b03
        a4in = i1 * w14 + i2 * w24 - b04        
        # apply the logictic function on the weighted sum inputs to get the output
        a3o = logistic(a3in)
        a4o = logistic(a4in)    
        # for output neuron 5(the last neuron) take the outputs of the hidden layer a3 and a4 to get to weighted input sums of a5
        a5in = w35 * a3o + w45 * a4o - b05        
        #same as for the hidden layer apply the logistic function again for final output. 
        a5o = logistic(a5in)                   
        #pass all variables as python tuples. I chose this method because its easier to debug and see what goes where. less confusion        
        return a3o, a4o, a5o, a3in, a4in, a5in
    
        # End your code
        ###########################################

    # Returns the squared error of a collection of examples:
    # Error = 0.5 * sum_i ( example_labels[i] - ann.calculate(example_attributes) )**2
    def squared_error(self, example_attributes, example_labels):
        ###########################################
        # Start your code       
#        squared_error() calculates the error of the network on a set of examples        
        error = 0        
        for example in range(0, len(example_attributes)):                         
            a3o, a4o, a5o, a3in, a4in, a5in  = self.calculate(example_attributes[example])        
            error += 0.5 * ((example_labels[example] - a5o)**2)        
                        
        return error
        # End your code
        ###########################################

    # Runs backpropagation on a single example in order to
    # update the network weights appropriately.
    def backpropagate_example(self, attributes, label, learning_rate=10.0):
        ###########################################
        # Start your code
        
#        backpropagate_example() applies the backpropagation algorithm to learn the weights for a given example.        
        i1 = attributes[0]
        i2 = attributes[1]                
        w13 = self.neurons[0].attribute_weights.get(0)
        w23 = self.neurons[0].attribute_weights.get(1)
        w14 = self.neurons[1].attribute_weights.get(0)
        w24 = self.neurons[1].attribute_weights.get(1)
        
        w35 = self.neurons[2].neuron_weights.get(0)
        w45 = self.neurons[2].neuron_weights.get(1)

        b03 = self.neurons[0].bias_weight
        b04 = self.neurons[1].bias_weight
        b05 = self.neurons[2].bias_weight
               
        # before we can backwards propagate we need to forward propagate to get all inputs and outputs of each neuron
        a3o, a4o, a5o, a3in, a4in, a5in  = self.calculate(attributes)
        
#        dEtotal/dW5 = dEtotal/dOut * dOut/dNet * dNet/dW5
#        the derivative product looks like this. this is basically the deltas for each neuron. 
        
# use the input and output that was returned from the forward propagation. Apply logistic derivative on the input(weigthed sums) 
# and multiply with the real output minus the observed output.         
        delta_5 = logistic_derivative(a5in) * (label - a5o)   
# for the hidden layers we dont know the real outputs. for this we multiply with the weigth times the delta of the output.
        delta_3 = logistic_derivative(a3in) * (w35 * delta_5)
        delta_4 = logistic_derivative(a4in) * (w45 * delta_5)
        
# To actually update the weigths. we multiply a fixed learning rate value times the delta value times the output values. 
# We have to look at relative to the current weight what was the input and what is the delta of the end point. for the neuron 
        # weights the outputs of the hidden layers can be used. 
        # for the attribute weigths the outputs of the input layer can be used. 
        # add the result to the previous weigths. 
        self.neurons[2].neuron_weights[0] += learning_rate * delta_5 * a3o
        self.neurons[2].neuron_weights[1] += learning_rate * delta_5 * a4o
        
        self.neurons[0].attribute_weights[0] += learning_rate * delta_3 * i1
        self.neurons[0].attribute_weights[1] += learning_rate * delta_3 * i2
        self.neurons[1].attribute_weights[0] += learning_rate * delta_4 * i1
        self.neurons[1].attribute_weights[1] += learning_rate * delta_4 * i2
        
        # updating biases is simpler. just multiple the learning rate with the deltas and substract from the previous biases. 
        self.neurons[0].bias_weight -= learning_rate * delta_3
        self.neurons[1].bias_weight -= learning_rate * delta_4
        self.neurons[2].bias_weight -= learning_rate * delta_5
                             
        return
     
        # End your code
        ###########################################

    # Runs backpropagation on each example, repeating this process
    # num_epochs times.
    def learn(self, example_attributes, example_labels, learning_rate=10.0, num_epochs=10000):
        ###########################################
        # Start your code
        
#       learn() repeatedly applies the backpropagation algorithm to each of 
#       the input examples, repeating num_epochs times (that is, for 4 examples and 100 epochs, 
#       learn() will call backpropagate_example() 400 times.)
        
        # for each epoch call backpropagate for each example(set of training data).                    
        for epoch in range(0,num_epochs):
            for example in range(0,len(example_attributes)):
                self.backpropagate_example(example_attributes[example],example_labels[example],learning_rate)              
        
        # End your code
        ###########################################

example_attributes = [ [0,0], [0,1], [1,0], [1,1] ]
example_labels = [0,1,1,0]

def random_ann(num_attributes=2, num_hidden=2):
    neurons = []
    # hidden neurons
    for i in range(num_hidden):
        attribute_weights = {attribute_index: random.uniform(-1.0,1.0) for attribute_index in range(num_attributes)}
        bias_weight = random.uniform(-1.0,1.0)
        neurons.append(Neuron(attribute_weights,{},bias_weight))
    # output neuron
    neuron_weights = {input_neuron: random.uniform(-1.0,1.0) for input_neuron in range(num_attributes)}
    bias_weight = random.uniform(-1.0,1.0)
    neurons.append(Neuron({},neuron_weights,bias_weight))
    ann = ANN(num_attributes, neurons)
    return ann

best_ann = None
best_error = float("inf")

for instance_index in range(10):
    ann = random_ann()
    ann.learn(example_attributes, example_labels, learning_rate=10.0, num_epochs=10000)
    error = ann.squared_error(example_attributes, example_labels)
    if error < best_error:
        best_error = error
        best_ann = ann    
#    print("instance_index", instance_index)

print("best_error", best_error)
print("result", best_ann)
print("neuron 0 attributes", best_ann.neurons[0].attribute_weights)
print("neuron 0 bias", best_ann.neurons[0].bias_weight)
print("neuron 1 attributes", best_ann.neurons[1].attribute_weights)
print("neuron 1 bias", best_ann.neurons[1].bias_weight)
print("neuron 2 neuron weight", best_ann.neurons[2].neuron_weights)
print("neuron 2 bias", best_ann.neurons[2].bias_weight)

#####################################################
#####################################################
# Please hard-code your learned ANN here:
learned_ann = random_ann()
learned_ann.neurons[0].attribute_weights[0] = -7.4431816681486715
learned_ann.neurons[0].attribute_weights[1] = -7.598748525780117
learned_ann.neurons[0].bias_weight = -3.232622301036815
learned_ann.neurons[1].attribute_weights[0] = -6.089845109060663
learned_ann.neurons[1].attribute_weights[1] = -6.118814430635697
learned_ann.neurons[1].bias_weight = -9.118149177554171
learned_ann.neurons[2].neuron_weights[0] = -12.652079717234438
learned_ann.neurons[2].neuron_weights[1] = 12.488584861240517
learned_ann.neurons[2].bias_weight = 6.036267315027895
# Enter the squared error of this network here:
final_squared_error = 2.4943843832028376e-05
#####################################################
#####################################################


