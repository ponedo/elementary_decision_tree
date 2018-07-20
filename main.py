#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################
#
#    samples:
#        [[], [], [], ...]
#
#    attributes:
#        [1, 2, 3, 4,...]
#
#    attr_types:
#        [None, 'd', 'c', ...]
#
#################################

import TreeGenerate
from test_lib import *
from copy import deepcopy

def floattrans(x):
    """
    Distinguish discrete attributes and continuous attributes
    if discrete: string retains its form
    if continuous: tranform string into float
    """
    try:
        return float(x)
    except:
        return x



def preproc(samples, attributes):
    """
        Handle continuous attributes.
        Transform corresponding string values in file into float numbers.
        Generate attribute list.
    """
    attr_types = []
    attr_types.insert(0, None)
    attrset = attributes[:]
    for attr in attributes:
        if samples[0][attr]==floattrans(samples[0][attr]):
            attrset.remove(attr) # still string, discrete attr!
            attr_types.insert(attr, 'd') # discrete
        else:
            attr_types.insert(attr, 'c') # continuous
    for sample in samples:
        for attr in attrset:
            sample[attr] = floattrans(sample[attr])
    return attr_types



if __name__ == "__main__":
    samples = []
    
    f = open("wine_data.txt")
    for sample in f:
        sample = sample.strip('\n')
        sample = sample.split(',')
        samples.append(sample)

    attributes = list(range(1, len(samples[0])))

    # test by bootstrapping
    samples_cp = deepcopy(samples) # Deepcopy to avoid bugs
    print("Bootstrapping:")
    print("Generating training set by sampling for 100 times in dataset...")
    trainset, testset = bootstrap(samples_cp, 100)
    attr_types = preproc(trainset, attributes)
    print("Generating decision tree...")
    decision_tree = TreeGenerate.TreeGenerate(trainset, attributes, attr_types)
    accuracy = test(testset, decision_tree)
    print("Accuracy: %s" % accuracy)

    print('\n')
    # test by cross validation
    samples_cp = deepcopy(samples) # Deepcopy to avoid bugs
    print("Cross validation:")
    print("Dividing dataset for 10 times for training and testing...")
    trainsets, testsets = crossvalid(samples_cp, 10)
    accuracies = []
    for trainset, testset in zip(trainsets, testsets):
        trainset_cp = deepcopy(trainset) # Deepcopy to avoid bugs
        testset_cp = deepcopy(testset) # Deepcopy to avoid bugs
        attr_types = preproc(trainset_cp, attributes)
        print("Generating decision tree...")
        decision_tree = TreeGenerate.TreeGenerate(trainset_cp, attributes, attr_types)
        accuracies.append(test(testset_cp, decision_tree))
    accuracy = sum(accuracies)/len(accuracies)
    print("Accuracy: %s" % accuracy)  
    
    f.close()
