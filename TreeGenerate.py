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

"""
    Generate a decision tree
    with pruning and continuous value handling.
    - Possible future work:
    - when we are selecting
    - the refering attribute
    - or the class as division result
    - for a treenode, if multi-result is available,
    - some more specific strategies to select the best one,
    - rather choosing randomly, shoule be taken.
"""

import random
from math import log

class TreeNode:
    def __init__(self):
        self.bl = "branch"
        self.kind = [] # may be multi-result
        self.attr = None
        self.attr_type = None
        self.children = {}
    def printinfo(self):
        print(self.bl)
        print(self.kind)
        print(self.attr)
        print(self.attr_type)
        print(self.children)
        print('\n')



def findmost(samples):
    "Find the class which contains largest number of samples"
    tmp_dict = {}
    for sample in samples:
        tmp_dict[sample[0]] = tmp_dict.get(sample[0], 0) + 1
    candidates = []
    for i in sorted(tmp_dict.items(), reverse=True, key=lambda x:x[1]):
        if len(candidates)==0:
            candidates.append(i[0])
            n = i[1]
        else:
            if i[1]==n:
                candidates.append(i[0])
            else:
                break
    return candidates



def Ent(samples):
    subsets = {}
    total_num = len(samples)
    ent = 0
    for sample in samples:
        subsets[sample[0]] = subsets.get(sample[0], 0) + 1
    for item in subsets.items():
        porpotion = item[1]/total_num
        ent += porpotion * log(porpotion, 2)
    return (-ent)



def Gain(samples, attr, attr_type):
    
    total_num = len(samples)
    
    if attr_type=='d':
        subsets = {}
        for sample in samples:
            subsets.setdefault(sample[attr], []).append(sample)
        tmp = 0
        for item in subsets.items():
            tmp += len(item[1])*Ent(item[1])/total_num
        gain = Ent(samples) - tmp
        return gain, subsets
            
    else:
        values = []
        finalsubsets = {}
        maxgain = 0
        for sample in samples:
            values.append(sample[attr])
        values.sort()
        divpoints = []
        for i in range(len(values)-1):
            divpoints.insert(i, (values[i]+values[i+1])/2)
        for divp in divpoints:
            subsets = {}
            for sample in samples:
                if sample[attr]<divp:
                    subsets.setdefault('<'+str(divp), []).append(sample)
                else:
                    subsets.setdefault('>='+str(divp), []).append(sample)
            tmp = 0
            for item in subsets.items():
                tmp += len(item[1])*Ent(item[1])/total_num
            gain = Ent(samples) - tmp
            if gain>maxgain:
                maxgain = gain
                finalsubsets = subsets
        return maxgain, finalsubsets



def selectAttr(samples, attributes, attr_types):
    """
        Handling discrete values normally.
        Handling continuous values by using bi-partition.
        - Possible future work:
        - Use multi-partition.
    """
    count = {}
    subsets = {}
    for attr in attributes:
        count[str(attr)], subsets[str(attr)] = Gain(samples, attr, attr_types[attr])
    candidates = []
    for i in sorted(count.items(), reverse=True, key=lambda x:x[1]):
        if len(candidates)==0:
            candidates.append(i[0])
            n = i[1]
        else:
            if i[1]==n:
                candidates.append(i[0])
            else:
                break
    selected_attr = candidates[random.randint(0, len(candidates)-1)]
    subsets_attr = subsets[selected_attr] # random feels bad, to improve
    selected_attr = int(selected_attr)
    
    return selected_attr, subsets_attr



def TreeGenerate(samples, attributes, attr_types):
    "Algorithm on Page 74"
    treenode = TreeNode()
    print(' - new node!')
    
    for sample in samples: # test if all samples' class are the same
        if sample[0] != samples[0][0]:
            break # different classes found
    else:
        treenode.bl = 'leaf' # all samples' class are the same
        treenode.kind = samples[0][0]
        return treenode
    
    if len(attributes)==0:
        treenode.bl = 'leaf'
        treenode.kind = findmost(samples)
        return treenode
    
    for attr in attributes: # test if samples can be divided
        for sample in samples:
            if sample[attr] != samples[0][attr]:
                flag = False
                break # samples can still be divided
        else:
            continue
        break
    else: #samples cannot be divided anymore
        treenode.bl = 'leaf'
        treenode.kind = findmost(samples)
        return treenode

    treenode.attr, subsets = selectAttr(samples, attributes, attr_types)
    treenode.attr_type = attr_types[treenode.attr]
    
    for value in subsets:
        if len(subsets[value])==0:
            treenode.children[value] = TreeNode()
            treenode.children[value].bl = 'leaf'
            treenode.children[value].kind = findmost(samples)
        else:
            new_attributes = attributes[:]
            if attr_types[treenode.attr]=='d':
                new_attributes.remove(treenode.attr)
            treenode.children[value] = TreeGenerate(subsets[value], new_attributes, attr_types)

    return treenode
