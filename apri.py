import pandas as pd
import itertools

dataSet = './adult.data'
# dataSet = './sikko.data'
df = pd.read_csv(dataSet, header=None)

itemApperanceMap = {}
itemFreq = {}
supportedItemFreq = {}


def self_join_items(depth):
    uniqueElements = []

    for key in itemApperanceMap.keys():
        uniqueElements.append(key)

    return itertools.combinations(uniqueElements, depth + 1)


def printFrozenSet(fs):
    retval = ''
    for i in fs:
        retval = retval + i + ' '

    return retval


def printTable(hashTable, count):
    for key in hashTable.keys():
        if (len(key) == count) and type(key) == frozenset:
            print(printFrozenSet(key), ' ', hashTable[key])


def calculate_set_freq(item_set):
    appearanceSets = []
    for set_item in item_set:
        appearanceSets.append(itemApperanceMap[set_item])

    intersection = appearanceSets[0]
    for i in range(1, len(appearanceSets)):
        intersection = intersection.intersection(appearanceSets[i])

    return len(intersection)


def addKeyToMaps(key, value):
    itemFreq[key] = value
    supportedItemFreq[key] = value


def remove_low_freq():
    low_freq_items = []

    for item_set in itemFreq:
        freq = itemFreq[item_set]
        if freq < minSupport:
            low_freq_items.append(item_set)

    for low_freq_item in low_freq_items:
        del supportedItemFreq[low_freq_item]


minSupport = 2
colCount = df.shape[1]

for index, row in df.iterrows():
    for i in range(colCount):
        val = row[i]
        if not pd.isna(df.iloc[index, i]):
            if val not in itemApperanceMap:
                appearanceSet = set()
                itemApperanceMap[val] = appearanceSet

            itemApperanceMap[val].add(index)

            if val in itemFreq:
                newVal = itemFreq[val] + 1
                addKeyToMaps(val, newVal)
            else:
                addKeyToMaps(val, 1)

remove_low_freq()
items = []
for item in itemFreq:
    items.append(item)

for i in range(len(items) - 1):
    for j in range(i + 1, len(items)):
        itemSet = frozenset([items[i], items[j]])
        setFreq = calculate_set_freq(itemSet)
        addKeyToMaps(itemSet, setFreq)

remove_low_freq()

printTable(supportedItemFreq, 2)

selfJoinTableResult = []
selfJoinTable = self_join_items(2)

for awd in selfJoinTable:
    selfJoinTableResult.append(awd)

for asd in selfJoinTableResult:
    joined_sample = set()
    for t in asd:
        joined_sample.add(t)
    print(asd, ' ', calculate_set_freq(frozenset(joined_sample)))


