import pandas as pd
import itertools
import time

start=time.time()

#dataSet = './adult.data'
dataSet = './adultap100.csv'


df = pd.read_csv(dataSet, header=None)

itemApperanceMap = {}
itemFreq = {}
supportedItemFreq = {}
minSupport = 2


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


def get_sets_to_join(retrieve_depth):
    retval = []
    for item_set in itemFreq:
        if type(item_set) == frozenset and len(item_set) == retrieve_depth:
            retval.append(item_set)
    return retval


def find_common_elements(lhs, rhs):
    if lhs is None or rhs is None:
        return 0

    if len(lhs) == 0 or len(rhs) == 0:
        return 0

    retval = []

    for element in lhs:
        if element in rhs:
            retval.append(element)

    return retval


def find_uncommon_elements(lhs, rhs):
    if lhs is None or rhs is None:
        return 0

    if len(lhs) == 0 or len(rhs) == 0:
        return 0

    retval = []

    if len(lhs) > len(rhs):
        for element in lhs:
            if element not in rhs:
                retval.append(element)
    else:
        for element in rhs:
            if element not in lhs:
                retval.append(element)

    return retval


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
    if depth == 1:
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
    else:
        sets_to_join = get_sets_to_join(depth)
        join_set_len = len(sets_to_join)

        if join_set_len < 2:
            continue

        for i in range(join_set_len - 1):
            left_side_set = sets_to_join[i]
            for j in range(1, join_set_len):
                right_side_set = sets_to_join[j]

                # common elements' size must be depth - 1
                common_elements = find_common_elements(left_side_set, right_side_set)
                if len(common_elements) == depth - 1:
                    uncommon_elements = find_uncommon_elements(left_side_set, right_side_set)

                    for uncommon_element in uncommon_elements:
                        base_set = set(common_elements)
                        base_set.add(uncommon_element)
                        joined_set = frozenset(base_set)

                        joined_set_freq = calculate_set_freq(joined_set)
                        if joined_set_freq < minSupport:
                            continue

                        addKeyToMaps(joined_set, joined_set_freq)



print('Final depth that we can support:', depth)

printTable(supportedItemFreq, depth)

difference = time.time() - start

print('Run time:', difference, ' seconds.')