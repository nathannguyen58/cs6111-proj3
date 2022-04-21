from collections import defaultdict
from itertools import combinations
import pandas as pd
import os

#method used to clean data and extract necessary columns
def process_data(dataset):
    df = pd.read_csv(dataset)   #read in csv
    processed_data = []
    for index, row in df.iterrows():    #extract all the data with the specified rows
        processed_data.append([str(row["Full Complaint ID"]), [str(row["Complaint Year Number"]), str(row["County"]), 
                        str(row["Offense Description"]), str(row["Bias Motive Description"])]])

    return processed_data   #return processed data


#find the large itemsets using the apriori algorithm
def apiori_frequent_set_mining(data, min_sup):   
    itemList = []
    c = defaultdict(int)   #true candidate item set
    l = defaultdict(int)   #will act as the previous large itemset
    large_itemset = defaultdict(int)
    frequent_itemset_list = []  #used for printing
    k = 1
    for id, items in data:    #retrieve all of the distinct items of the inputted data set and the number of times that they appear
        for item in items:
            c[item] += 1
            if (item not in itemList):
                itemList.append(item)

    itemList.sort()
    min_sup = (min_sup * len(data))   #make the minimum support a value of the number of rows within the actual data set

    for item, count in c.items():     #iterate through each distinct item
        if count >= min_sup:          #if the number of occurences is above the minimum number necessary to exceed the min support threshold, add to dictionary l
            l[frozenset([item])] = count
            large_itemset[frozenset([item])] = count/len(data) * 100   #store the item and its support % in large_itemset dictionary

    while l and k <= len(itemList):        #while l is not empty and our item set size hasn't reached the length of the original item set
        k += 1
        prev_sets = list(l.keys())   #itemsets of the previous iteration
        new_c = set()         #candidate itemset before pruning
        c = defaultdict(int)  #true candidate item set
        ##join step

        for i in range(0, len(prev_sets)):   #iterate through all the itemsets in k - 1
            for j in range(i+1, len(prev_sets)): #iterate through all the itemsets excluding those that have already been seen
                u = prev_sets[i].union(prev_sets[j])
                if (len(u) == k):            #add to new candidate itemset if length = k
                    new_c.add(u)
        
        # prune step
        for itemSet in new_c:  #for each item set in our new candidate item set
            subsets = list(combinations(list(itemSet), k-1))
            prunned = False
            for subset in subsets:   #for each subset of the current item set
                if subset and frozenset(subset) not in l:   #if the subset is not empty and the subset is not in the previous iteration of the large itemset, do not add to the true candidate item set
                    prunned = True
                    break
            if not prunned:
                c[frozenset(itemSet)] = 0

        
        # get frequency of each new set in c in data 
        for itemSet in c:
            for id, items in data:
                if(itemSet.issubset(items)):
                    c[itemSet] += 1
        
        # get the new iteration of the large itemset
        for item, count in c.items():
            if count >= min_sup:   #if the count of the current itemset exceeds the minimum support threshold, add it to the new iteration of the large itemset
                l[item] = count
                large_itemset[item] = count/len(data) * 100

    #print out the frequent itemset
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    for item, support in large_itemset.items():
        frequent_itemset_list.append([item, support])
    frequent_itemset_list.sort(key= lambda x: x[1], reverse=True)
    for item, support in frequent_itemset_list:
        with open("output.txt", "a") as f:
            f.write(str(list(item)) + ", " + str(support)+ "%\n")
        f.close()
    return large_itemset

#extract association rules with confidence greater than or equal to min confidence threshold
def apriori_association_rule(large_itemset, min_conf):
    high_confidence_rules = []  #list of all high confidence rules
    for li in large_itemset:    #iterate through each itemset in the large itemset
        if len(li) > 1:
            lhs_combinations = [frozenset(i) for i in combinations(li, len(li) - 1)]  #get the subsets that are of length 1 less than the length of the current itemset, will use as the left hand side of association rules
            for lhs in lhs_combinations:    #iterate through each left handside of association rules
                rhs = li - lhs              #right handside consists of a single item that is not included in the left handside
                confidence = large_itemset[li]/large_itemset[lhs] * 100   #calculation of confidence
                if confidence >= min_conf * 100:                    #if confidence of association rule exceeds that minimum confidence
                    high_confidence_rules.append([lhs, rhs, confidence, large_itemset[li]])
    high_confidence_rules.sort(key= lambda x: x[2], reverse= True)
    for lhs, rhs, confidence, support in high_confidence_rules:
        with open("output.txt", "a") as f:
            f.write(str(list(lhs)) + " => " + str(list(rhs)) + " [Conf: " + str(confidence) + "% Supp: " + str(support) + "%]\n")
        f.close()

        
            
        





    
    