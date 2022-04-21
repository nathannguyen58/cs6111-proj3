import sys
import utils
def main():
    args = sys.argv[1:]
    dataset = args[0]
    min_sup = float(args[1])
    min_conf = float(args[2])

    data = utils.process_data(dataset)
    itemset =  utils.apiori_frequent_set_mining(data, min_sup)
    utils.apriori_association_rule(itemset, min_conf)



if __name__ == "__main__":
    main()