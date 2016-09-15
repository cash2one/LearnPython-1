import json
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

path = "../data/usagov_bitly_data2012-03-16-1331923249.txt"
records = [json.loads(line) for line in open(path)]
print records[0]
print records[0]['tz']
time_zones = [rec['tz'] for rec in records if 'tz' in rec]


def get_counts(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] = +1
    return counts


counts = get_counts(time_zones)

counts['America/New_York']

Counter(time_zones)

frame = DataFrame(records)
