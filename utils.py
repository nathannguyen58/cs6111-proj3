from collections import defaultdict
from itertools import combinations

itemList = []

data = [['1', ['pen', 'ink', 'diary']], ['2', ['pen', 'ink', 'diary']], ['3', ['pen', 'diary']], ['4', ['pen', 'ink', 'soap']]]


def apiori_frequent_set_mining(data, min_sup, min_conf):
    
    c = defaultdict(int)
    l = defaultdict(int)
    large_itemset = defaultdict(int)
    k = 1
    for id, items in data:
        for item in items:
            c[item] += 1
            if (item not in itemList):
                itemList.append(item)

    sorted(itemList)
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
    
    return large_itemset

def apriori_association_rule(large_itemset, min_conf):
    for li in large_itemset:
        if len(li) > 1:
            lhs_combinations = [frozenset(i) for i in combinations(li, len(li) - 1)]
            for lhs in lhs_combinations:
                rhs = li - lhs
                confidence = large_itemset[li]/large_itemset[lhs] * 100
                if confidence >= min_conf * 100:
                    print(str(lhs) + " => " + str(rhs) + " [Conf: " + str(confidence) + "% Supp: " + str(large_itemset[li]) + "%]")


                

itemset = apiori_frequent_set_mining(data, 0.7, 0.8)
apriori_association_rule(itemset, 0.8)

        
            
        





    
    