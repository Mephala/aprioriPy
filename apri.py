import pandas as pd
import itertools

# dataSet = './adult.data'
# dataSet = './sikko.data'
# dataSet = './adult-min.data'
dataSet = './adul5.data'
df = pd.read_csv(dataSet, header=None)

itemApperanceMap = {}
itemFreq = {}
supportedItemFreq = {}
minSupport = 3


def check_depth_support(check_depth):
    if check_depth == 0:
        for itemSet in supportedItemFreq:
            if type(itemSet) == str:
                return True
        return False
    else:
        for itemSet in supportedItemFreq:
            if (type(itemSet) == frozenset) and len(itemSet) == (check_depth + 1):
                return True
        return False


def self_join_items(join_depth):
    uniqueElements = []

    for key in itemApperanceMap.keys():
        uniqueElements.append(key)

    return itertools.combinations(uniqueElements, join_depth + 1)


def printFrozenSet(fs):
    retval = ''

    for fs_element in fs:
        if type(fs_element) == int:
            retval = retval + str(fs_element) + ' '
        else:
            retval = retval + fs_element + ' '

    return retval


def printTable(hashTable, count):
    for key in hashTable.keys():
        if type(key) == frozenset and len(key) == count:
            print(printFrozenSet(key), ' ', hashTable[key])
        else:
            print(key, ' ', hashTable[key])


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
        if low_freq_item in supportedItemFreq:
            del supportedItemFreq[low_freq_item]


colCount = df.shape[1]
print('Running with min support:', minSupport)

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

print('Completed variable indexing, starting self-join procedure')
remove_low_freq()
depth = 0

while check_depth_support(depth):
    depth = depth + 1
    print('Creating tables with level:', depth + 1)
    selfJoinTableResult = []
    selfJoinTable = self_join_items(depth)

    for selfJoinResult in selfJoinTable:
        selfJoinTableResult.append(selfJoinResult)

    for selfJoinResultElement in selfJoinTableResult:
        joined_sample = set()
        for elementInner in selfJoinResultElement:
            joined_sample.add(elementInner)

        selfJoinResultElementFrozenSet = frozenset(joined_sample)
        selfJoinResultElementFreq = calculate_set_freq(selfJoinResultElementFrozenSet)
        addKeyToMaps(selfJoinResultElementFrozenSet, selfJoinResultElementFreq)

    print('Completed creating tables with level:', depth + 1, 'testing support range.')
    remove_low_freq()

print('Final depth that we can support:', depth)

printTable(supportedItemFreq, depth)
