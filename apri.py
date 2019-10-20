import pandas as pd

dataSet = './adult.data'
df = pd.read_csv(dataSet, header=None)

minSupport = 2
minConfidence = 60

itemAppearanceSet = {}
colCount = df.shape[1]
itemFreq = {}
for index, row in df.iterrows():
    for i in range(colCount):
        val = row[i]
        if not pd.isna(df.iloc[index, i]):
            if val not in itemAppearanceSet:
                appearanceSet = set()
                itemAppearanceSet[val] = appearanceSet

            itemAppearanceSet[val].add(index)

            if val in itemFreq:
                itemFreq[val] += 1
            else:
                itemFreq[val] = 1


def remove_low_freq():
    low_freq_items = []

    for item_set in itemFreq:
        freq = itemFreq[item_set]
        if freq < minSupport:
            low_freq_items.append(item_set)

    for low_freq_item in low_freq_items:
        del itemFreq[low_freq_item]


remove_low_freq()
itemSetFreq = {}
items = []
for item in itemFreq:
    items.append(item)


def calculate_set_freq(item_set):
    common = set()
    uncommon_items = []

    for set_item in item_set:
        if len(common) == 0:
            common.update(itemAppearanceSet[set_item])
        else:
            tmp = itemAppearanceSet[set_item]
            for maybeCommonItem in common:
                if maybeCommonItem not in tmp:
                    uncommon_items.append(maybeCommonItem)

    for un_common_item in uncommon_items:
        common.remove(un_common_item)

    item_set_freq = len(common)
    itemFreq[item_set] = item_set_freq
    return item_set_freq


for i in range(len(items) - 1):
    for j in range(i + 1, len(items)):
        itemSet = frozenset([items[i], items[j]])
        itemSetFreq[itemSet] = calculate_set_freq(itemSet)

remove_low_freq()

print(itemFreq)
