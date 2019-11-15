import time
from FPtree import FPtree
from printTree import printFPtree
from FPtreeMining import firstScan, deleteNsort, FP_growth

fileName = 'data/small.csv'
# fileName = 'data/flare.data1.csv'
# fileName = 'data/flare.data2.csv'
# fileName = 'data/agaricus-lepiota.csv'

# minimum support
min_sup = 2

# read data: list of lists
# default params: delimiter=','
file = open(fileName, 'r', encoding='UTF-8')
data = file.read().split('\n')
for i in range(len(data)):
    data[i] = data[i].split(',')

# step 1: scan the freq of all items -> dict
timer0 = time.time()
L1 = firstScan(data, min_sup)
timer1 = time.time()

# dict -> list of tuples
L1Tuple = sorted(L1.items(), key=lambda x: x[1], reverse=True)
timer2 = time.time()
print('L1:')
print(L1Tuple)

# delete the items according to min_sup
reData = deleteNsort(data, L1)
timer3 = time.time()

# build the initial FP tree
root = FPtree()
for transaction in reData:
    subTree = root
    for item in transaction:
        subTree = subTree.buildTree(item)
timer4 = time.time()
print("\nFP tree:")
printFPtree(root)

#┌────────────────┐#
#│ Mining FP Tree │#
#└────────────────┘#
FP_growth(L1Tuple, root, [], min_sup)
timer5 = time.time()

# time used
print('\nfirst scan:', timer1-timer0)
print('second scan:', timer3-timer2)
print('build the initial FP tree:', timer4-timer3)
print('FP mining:', timer5-timer4)