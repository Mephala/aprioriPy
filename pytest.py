from datetime import datetime
import itertools

time1 = datetime.now().microsecond
time2 = datetime.now().microsecond
time3 = datetime.now().microsecond
time4 = datetime.now().microsecond


ezgim = ['a', 'b', 'c', 'd', 'e']
ezgim3 = itertools.combinations(ezgim, 3)
for ezgimm in ezgim3:
    print(ezgimm)
