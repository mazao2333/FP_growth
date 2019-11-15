from FPtree import FPtree
from printTree import printFPtree
from itertools import combinations


def firstScan(unsortedList, min_sup=2):
    unsortedDict = dict()
    for ri in range(len(unsortedList)):
        for ci in range(len(unsortedList[ri])):
            if unsortedList[ri][ci] in unsortedDict.keys():
                unsortedDict[unsortedList[ri][ci]] += 1
            else:
                unsortedDict[unsortedList[ri][ci]] = 1
    filtered = dict()
    for k, v in unsortedDict.items():
        if v >= min_sup:
            filtered[k] = v
    return filtered


def deleteNsort(data, L1):
    newData = list()
    for row in data:
        newRow = dict()
        count = 1
        for element in row:
            if element in L1.keys():
                newRow[element] = L1[element]
        if len(newRow) > 0:
            sortedRow = sorted(
                newRow.items(), key=lambda x: x[1], reverse=True)
        sortedList = list()
        for sr in sortedRow:
            sortedList.append(sr[0])
        newData.append(sortedList)
    return newData


def buildTreeExternal(reData):
    root = FPtree()
    for transaction in reData:
        count = transaction[-1]
        transaction.pop()
        subTree = root
        for item in transaction:
            subTree = subTree.buildTree(item, count)
    return root


def buildIHT(L1Tuple, root):
    IHT = list()
    for l in L1Tuple:
        iht = [l[0], root.getCount(l[0]), root.getPointer(l[0])]
        IHT.append(iht)
    return IHT


def findPath(node):
    path = [tuple([node.name,node.value])]
    if len(node.children) > 0:
        path.extend(findPath(node.children[0]))
    return path

# python -m memory_profiler main.py
@profile
def FP_growth(L1Tuple, Tree, alpha, min_sup):
    if Tree.is1Path():
        pItems = findPath(Tree)
        items = list()
        for i in pItems:
            if i[0] != 'null' and i[1] >= min_sup:
                items.append(i)
        Beta = dict()
        for n in range(len(items)):
            results = combinations(items, n+1)
            for result in results:
                keys = list()
                sups = list()
                for r in result:
                    keys.append(r[0])
                    sups.append(r[1])
                keys.extend(alpha)
                sup = min(sups)
                Beta[tuple(keys)] = sup
        if Beta:
            print('\npatterns:')
            for k,v in Beta.items():
                print(k, end=':')
                print(v)
    else:
        pIHT = buildIHT(L1Tuple, Tree)
        IHT = list()
        for piht in pIHT:
            if piht[1] > min_sup and len(piht[2]) > 0:
                IHT.append(piht)
        # print('\nitem header table:')
        # for iht in IHT:
        #     print(iht)
        for iht in reversed(IHT):
            beta = [iht[0]]
            beta.extend(alpha)
            print('\npatterns:')
            print(tuple(beta), end=':')
            print(iht[1])
            CPB = Tree.getCPB(iht[0], iht[2])
            Tree_beta = buildTreeExternal(CPB)
            # printFPtree(Tree_beta)
            if len(Tree_beta.children) > 0:
                FP_growth(L1Tuple, Tree_beta, beta, min_sup)
