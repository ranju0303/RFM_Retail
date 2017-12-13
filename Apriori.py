# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:24:55 2017
@author: abhishekk
"""
my_list = ['apple', 'banana', 'grapes', 'pear']
for c, value in enumerate(my_list):
    print(c,value)
#items, rules = runApriori(inFile, minSupport, minConfidence)

from optparse import OptionParser
from collections import defaultdict
from itertools import chain, combinations

def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    #x={i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length}
    #print("inside joinset")
    #print(x)
    #return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])
    return {i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length}

def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset
    of the itemSet each of whose elements satisfies the minimum support"""
    print ("Inside returnItemsWithMinSupport")
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        print ("item",item)
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1
                        
    
#    print (freqSet)
    print("localset")
    print (localSet)

    for item, count in localSet.items():
        support = float(count)/len(transactionList)
        
        if support >= minSupport:
                _itemSet.add(item)

    return _itemSet

def getItemSetTransactionList(data_iterator):
    print ("Inside itemsettransaction")
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        #print (record)
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
#            print (item)
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, transactionList

def dataFromFile(fname):    
    """Function which reads from the file and yields a generator"""
    
    print ("Inside datafromfile")
    file_iter = open(fname, 'rU')
    for line in file_iter:
        line = line.strip().rstrip(',')                # Remove trailing comma
        record = frozenset(line.split(','))      
        yield record

if __name__ == "__main__":
    print("inside main")
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')
    
    (options, args) = optparser.parse_args()    
    inFile = dataFromFile(options.input)      
    print("before")    
    itemSet, transactionList = getItemSetTransactionList(inFile)
    #print(transactionList)
    
    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport
    minSupport  = 0.15
    minConfidence=0.6
    assocRules = dict()
    # Dictionary which stores Association Rules
    print ("ok")
    oneCSet = returnItemsWithMinSupport(itemSet,transactionList,minSupport,freqSet)
    print ("###########################################################################")
    print(" ")
    print(" ")
    print (oneCSet)  
    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        print (largeSet)
        print (k)
    #    joinSet(currentLSet, k)
    
        currentLSet = joinSet(currentLSet, k)
        print("current l set is")
        print(currentLSet)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                     transactionList,
                                                     minSupport,
                                                     freqSet)
        print("Current C set")
        print(currentCSet)
        currentLSet = currentCSet
        k = k + 1
    
    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item])/len(transactionList)
    
    print("Largeset")
    print(largeSet)
    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])
    
    print("toRetItems#########################################")
    print(toRetItems)
    print("largesetitems")
    #print (largeSet.items()[1:])
    toRetRules = []
    for key, value in largeSet.items():
        for item in value:
            print (item)
            _subsets = map(frozenset, [x for x in subsets(item)])
            x=[x for x in subsets(item)]
            print("subset",[i for i in x])
            for element in _subsets:
                remain = item.difference(element)
                print ("emain",remain)
                if len(remain) > 0:
	                confidence = getSupport(item)/getSupport(element)
	                if confidence >= minConfidence:
	                    toRetRules.append(((tuple(element), tuple(remain)),
	                                       confidence))
    print (toRetRules)








                


