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

import random

def classify(testsample, tree):
    "The testsample is not supposed to be preprocesed!"
    if tree.bl=='leaf':
        return tree.kind
    else:
        if tree.attr_type == 'd':
            subtree = tree.children[testsample[tree.attr]]
            return classify(testsample, subtree)
        else:
            for i in tree.children.items():
                ineq = testsample[tree.attr] + i[0]
                if eval(ineq):
                    subtree = i[1]
                    return classify(testsample, subtree)
            else:
                return Exception('Unable to classify!')    



def test(testset, tree):
    "Samples in the testset are not supposed to be preprocesed!"
    record=[]
    for sample in testset:
        judgeset = classify(sample, tree)
        for judge in judgeset:
            if judge==sample[0]:
                #print("test passed")
                record.append(True)
                break
        else:
            #print("test failed")
            record.append(False)
    accuracy = record.count(True)/len(record)        
    return accuracy
    


def crossvalid(samples, k):
    "k-fold cross validation"
    total_num = len(samples)
    trainsets = []
    testsets = []
    
    random.shuffle(samples) # This line is where randomness exerts its influence!
    classes = {}
    j=0
    for sample in samples:
        classes.setdefault(sample[0], []).append(j)
        j += 1
    # classes =
    # {
    #     class1: [sample_id, sample_id ...],
    #     class2: [sample_id, sample_id ...],
    #     class3: [sample_id, sample_id ...],
    #     ...
    # }
    for i in range(k):
        # chunk every list (every value corresponding to a key) in the dictionary "classes"
        trainset = []
        trainindex = []
        testindex = []
        testset = []
        for item in classes.items():
            step = len(item[1])//k
            try:
                testindex.extend(item[1][i*step:(i+1)*step])
            except:
                testindex.extend(item[1][i*step:])
        trainindex = set(range(total_num))-set(testindex)
        for index in testindex:
            testset.append(samples[index])
        for index in trainindex:
            trainset.append(samples[index])
        trainsets.append(trainset)
        testsets.append(testset)
    return trainsets, testsets



def bootstrap(samples, n):
    """
    Bootstrap sampling for n times
    n should be a rather large number.
    """
    trainset = []
    trainindex = []
    testindex = []
    testset = []
    total_num = len(samples)

    for i in range(n):
        index = random.randint(0, total_num-1)
        trainset.append(samples[index])
        trainindex.append(index)
    testindex = set(range(total_num))-set(trainindex)

    for i in testindex:
        testset.append(samples[i])
    
    return trainset, testset
    
