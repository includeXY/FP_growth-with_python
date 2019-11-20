import pandas as pd
"""
FP树的类定义
"""
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode=None):   #treeNode类的构造函数，self 代表的是类的实例，代表当前对象的地址
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):                                    #treeNode类的方法
        self.count += numOccur

    def disp(self, ind = 2):
        print(' '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+2)

"""
FP树构建函数
"""

def createTree(dataSet, minsup,OrigDataSetSize):
    """
    参数：
        dataSet：事务集，是字典类型
        minsup：最小支持度阈值,小数形式
        OrigDataSetSize:初始事务集中的事务数量
    返回：
        retTree:FP树
        headerTable:头指针列表
    """
    headerTable = {}                                     #使用字典作为头指针表
    for trans in dataSet:
        for item in trans[0]:
            headerTable[item] = headerTable.get(item,0) + trans[1]
            #headerTable.get(item,0)返回指定键item的值，若item的值不在字典中，则返回默认值0
    for k in list(headerTable.keys()):                    # headerTable.keys()以列表形式返回字典的所有键
        sup = headerTable[k]/OrigDataSetSize            # 一项的支持度
        if sup < minsup:
            del(headerTable[k])                      # 若该项的支持度小于最小的支持度阈值，则删除该项
    freqItemSet = set(headerTable.keys())            # set()函数，返回一个非重复的无序的集合，该集合是频繁1项集
    if len(freqItemSet) == 0:
        return None,None                             # 如果频繁1项集为空，则退出
    for k in headerTable:
        headerTable[k] = [headerTable[k],None]       # 头指针表是一个字典，键是项，关键字是支持度计数和指向FP树中该项的指针的二元组
    retTree = treeNode('Null Set',1,None)            #创建FP树的根节点
    for tranSet, count in dataSet:           #dataSet.items()以列表形式返回可遍历的（键，值）元组
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]   # 筛选出每个事务中的频繁项，并保存在localD字典中作为键，同时以其在headerTable中的值作为值
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p:p[1],reverse=True)]
            #对localD进行降序排序，key=lambda p:p[1]表示以字典的值作为排序依据，v[0]表示以字典的键作为orderedItems的元素
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree, headerTable

def updateTree(items, inTree, headerTable, count):
    """
    :param items:单个事务中，单项满足支持度阈值的集合
    :param inTree: FP树的根结点
    :param headerTable: 头指针列表
    :param count: 事务集字典中的对应键的值
    :return: None
    """
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)       #如果该事务集已经在FP树中了，则更新其支持度计数即可
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree)  #如果该项不在FP树中，则创建一个结点作为孩子结点加进树中
        if headerTable[items[0]][1] == None:                         #如果头指针表中该项的指针为空，则改为指向该项
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])  #否则将该节点添加到原链表中
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)  #如果items元素不止一个，则对剩下的元素递归调用updateTree

def updateHeader(nodeToTest, targetNode):
    """
    :param nodeToTest: 头指针列表中待测结点的指针
    :param targetNode: 待测结点
    :return: None
    """
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink       #遍历头指针列表中该项的链表
    nodeToTest.nodeLink = targetNode           #将待测结点加进链表中

def loadSimpDat():
        filename = open('D:\study\Data Mining\上机实验数据文件.txt')
        items_txt = pd.read_csv( filename, header=None)
        data = items_txt.values.tolist()  # 将pd.read_csv读入的文本数据转换为数组，数组的每个元素都是一个字符串
        L = len(data)  # 求数组的条目数
        data_set = []
        for i in range(0, L):
            t = data[i][0].split()  # 将字符串按空格差分，默认删除空格
            data_set.append(t)
        return data_set


"""
def loadSimpDat():
    dataSet = [['I1','I2','I5'],
               ['I2','I4'],
               ['I2','I3'],
               ['I1','I2','I4'],
               ['I1','I3'],
               ['I2','I3'],
               ['I1','I3'],
               ['I1','I2','I3','I5'],
               ['I1','I2','I3']]
    return dataSet
"""

def createInitSet(dataSet):
    """
    将列表类型的dataSet转换成字典类型
    :param dataSet: 列表类型的事务集
    :return: 字典类型的事务集
    """
    retDict = []
    for trans in dataSet:
        tem = []
        tem.append(trans)
        tem.append(1)
        temp = tuple(tem)
        retDict.append(temp)
    return retDict

def accendTree(leafNode, prefixPath):
    """
    由leafNode开始迭代上溯整棵树,知道遇到根结点为止
    :param leafNode: 迭代上溯的起点
    :param prefixPath: 迭代上溯得到的路径
    :return: None
    """
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        accendTree(leafNode.parent,prefixPath)

def findPrefixPath(basePat, treeNode):
    """
    根据fp树，查找元素项basePat的条件模式基
    :param basePat: 元素项
    :param treeNode:头指针列表中该元素项所在栏指向的fp结点
    :return: 元素项basePat的条件模基为键的字典
    """
    condPats = []                #初始化空字典保存条件模式基
    while treeNode != None:
        prefixPath = []          #初始化空列表保存上溯的lujing
        accendTree(treeNode,prefixPath)
        tem = []
        if len(prefixPath) > 1:
            tem.append(prefixPath[1:])
            tem.append(treeNode.count)   #以treeNode的前缀路径作为键保存在condPats中
            temp = tuple(tem)
            condPats.append(temp)
        treeNode = treeNode.nodeLink                               #上溯链表中的下一个结点，抽取条件模式基
    return condPats

def mineTree(inTree, headerTable, minsup, preFix, freqItemList, OrigDataSetSize):
    """
    递归查找频繁项集
    :param inTree:
    :param headerTable:
    :param minsup:
    :param prefix:
    :param freqItemList:
    :return:
    """
    local = {}
    for item in headerTable:
        local[item] = headerTable[item][0]
    bigL = [v[0] for v in sorted(local.items(), key=lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minsup, OrigDataSetSize)
        if myHead != None:
            mineTree(myCondTree, myHead, minsup, newFreqSet, freqItemList, OrigDataSetSize)