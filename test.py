import FPGrowth as fp
import numpy
import pandas as pd
#filename=open('C:\DATA_Mining\上机实验数据文件.txt')
simpDat = fp.loadSimpDat()
#print(simpDat)

initSet = fp.createInitSet(simpDat)
#print(initSet)
orig = len(initSet)
#print(orig)

myFPTree, myHeaderTab = fp.createTree(initSet, 0.15, orig)

"""
print(myHeaderTab)
myFPTree.disp()

local = {}
for item in myHeaderTab:
    local[item] =  myHeaderTab[item][0]
listItem1 = []
listItem1 = [v[0] for v in sorted(local.items(), key=lambda p:p[1])]
print(listItem1)
list = ['I5','I4','I3','I1']
for i in list:
    condPats = fp.findPrefixPath(i,myHeaderTab[i][1])
    print(condPats)
#print(fp.findPrefixPath('x', myHeaderTab['x'][1]))
#print(fp.findPrefixPath('z', myHeaderTab['z'][1]))
"""

freqItems = []
fp.mineTree(myFPTree, myHeaderTab, 0.15, set([]), freqItems, orig)
freqItemsList = sorted(freqItems, key=lambda i: len(i))
#print(len(freqItemsList))
size = 0
for i in freqItemsList:
    if len(i) != size:
        size = len(i)
        print('='*30,size,'-items freqSet','='*30)
    print(i)