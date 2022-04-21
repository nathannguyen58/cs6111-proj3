from collections import defaultdict
from itertools import combinations
import pandas as pd
import os
itemList = []

#data = [['1', ['pen', 'ink', 'diary']], ['2', ['pen', 'ink', 'diary']], ['3', ['pen', 'diary']], ['4', ['pen', 'ink', 'soap']]]

def process_data():
    df = pd.read_csv("NYPD_Hate_Crimes.csv")
    processed_data = []
    for index, row in df.iterrows():
        processed_data.append([str(row["Full Complaint ID"]), [str(row["Complaint Year Number"]), str(row["County"]), 
                        str(row["Offense Description"]), str(row["Bias Motive Description"])]])

    return processed_data


def apiori_frequent_set_mining(data, min_sup, min_conf):
    
    c = defaultdict(int)
    l = defaultdict(int)
    large_itemset = defaultdict(int)
    frequent_itemset_list = []
    k = 1
    for id, items in data:
        for item in items:
            c[item] += 1
            if (item not in itemList):
                itemList.append(item)

    itemList.sort()
    min_sup = (min_sup * len(data))

    for item, count in c.items():
        if count >= min_sup:
            l[frozenset([item])] = count
            large_itemset[frozenset([item])] = count/len(data) * 100

    while l and k <= len(itemList):        #while l is not empty and our item set size hasn't reached the length of the original item set
        k += 1
        prev_sets = list(l.keys())
        new_c = set()
        c = defaultdict(int)
        ##join step

        for i in range(0, len(prev_sets)):   #iterate through all the itemsets in k - 1
            for j in range(i+1, len(prev_sets)): #same thing
                u = prev_sets[i].union(prev_sets[j])
                if (len(u) == k):            #add to new candidate itemset if length = k
                    new_c.add(u)
        
        # prune step
        for itemSet in new_c:
            subsets = list(combinations(list(itemSet), k-1))
            prunned = False
            for subset in subsets:
                if subset and frozenset(subset) not in l:
                    prunned = True
                    break
            if not prunned:
                c[frozenset(itemSet)] = 0

        
        # get frequency of each new set in c in data 
        for itemSet in c:
            for id, items in data:
                if(itemSet.issubset(items)):
                    c[itemSet] += 1
        
        # get the new l
        for item, count in c.items():
            if count >= min_sup:
                l[item] = count
                large_itemset[item] = count/len(data) * 100

    #print out the frequent itemset
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    for item, support in large_itemset.items():
        #print("Item:" + str(list(item)) + "\n")
        #print("Support:" + str(support) + "\n")
        frequent_itemset_list.append([item, support])
    frequent_itemset_list.sort(key= lambda x: x[1], reverse=True)
    # for item, support in frequent_itemset_list:
    #     print("Item:" + str(list(item)) + "\n")
    #     print("Support:" + str(support) + "\n")
    # support_content = ""
    for item, support in frequent_itemset_list:
        with open("output.txt", "a") as f:
            f.write(str(list(item)) + ", " + str(support)+ "%\n")
        f.close()
    # print(support_content)
    return large_itemset

def apriori_association_rule(large_itemset, min_conf):
    high_confidence_rules = []
    for li in large_itemset:
        if len(li) > 1:
            lhs_combinations = [frozenset(i) for i in combinations(li, len(li) - 1)]
            for lhs in lhs_combinations:
                rhs = li - lhs
                confidence = large_itemset[li]/large_itemset[lhs] * 100
                if confidence >= min_conf * 100:
                        # (str(lhs) + " => " + str(rhs) + " [Conf: " + str(confidence) + "% Supp: " + str(large_itemset[li]) + "%]")
                    high_confidence_rules.append([lhs, rhs, confidence, large_itemset[li]])
    high_confidence_rules.sort(key= lambda x: x[2], reverse= True)
    for lhs, rhs, confidence, support in high_confidence_rules:
        with open("output.txt", "a") as f:
            f.write(str(list(lhs)) + " => " + str(list(rhs)) + " [Conf: " + str(confidence) + "% Supp: " + str(support) + "%]\n")
        f.close()
    # print(confidence_content)

data = process_data()
#print(data)
itemset = apiori_frequent_set_mining(data, 0.09, 0.4)
#print(itemset)
apriori_association_rule(itemset, 0.4)

        
            
        





    
    