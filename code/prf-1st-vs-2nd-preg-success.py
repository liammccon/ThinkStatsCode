#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:54:37 2024

@author: liammccon
"""


"""

Are 2nd Pregnancies usually more successful?
I think my initial question (How are age and first-pregnancy-success correlated) was too much right now - focus on comparing means first.

Sample

Women who had at least 2 pregnancies -> look at resp data
NUMPREGS (96 - 97): all ids where numpregs >= 2
First and Second unaborted pregnancy pairing, from preg data in nsfg
OUTCOME (277 - 277): SUCCESS 1 (live) / NOT-SUCCESS: 3 (stillbirth), 4 (miscarriage), 5 (ectopic)
pregordr (13 - 14): look at ( pregorder = 1, pregorder = 2 )
Check:

Is the success rate of first pregnancies lower or higher than second pregnancies, by how much?
Get the pregnancy and respondant data, with code from: Allen B. Downey MIT License: https://opensource.org/licenses/MIT

from os.path import basename, exists
def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("Downloaded " + local)

download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemPreg.dct")
download(
    "https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemPreg.dat.gz"
)
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemResp.dct")
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemResp.dat.gz")

import numpy as np
import nsfg
preg = nsfg.ReadFemPreg()
resp = nsfg.ReadFemResp()
"""

from os.path import basename, exists
def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("Downloaded " + local)

download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemPreg.dct")
download(
    "https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemPreg.dat.gz"
)
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemResp.dct")
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemResp.dat.gz")

import numpy as np
import nsfg
preg = nsfg.ReadFemPreg()
resp = nsfg.ReadFemResp()

# Verify the preg data by comparing outcomes with codebook
def sortedValueCounts(series):
    return series.value_counts().sort_index()
    
print(sortedValueCounts(preg.outcome))


# Get a list of all respondent IDs (caseid) for whom numpregs is >= 2
mult_preg_resp = resp[(resp.numpregs >= 2) & (resp.numpregs != 98)] 
mult_preg_ids = mult_preg_resp.caseid
# Verify the counts
sortedValueCounts(mult_preg_resp.numpregs)

# Get the pregnancies that are from women who've had multiple pregnancies
one_preg_of_mult = preg[preg.caseid.isin(mult_preg_ids)]

# Verify that women who had one pregnancy are not in the list
single_preg_ids = resp[resp.numpregs == 1].caseid
is_in_mult = one_preg_of_mult.caseid.isin(single_preg_ids)
if(is_in_mult.any()):
    print("ERROR IN SAMPLE!")
else:
    print("All good")
    
    
# Filter down to pregnancies that are from women with multiple pregnancies, where
# none of the pregnancies were aborted or unfinished

first_or_second_preg = one_preg_of_mult[(one_preg_of_mult.pregordr == 1) | (one_preg_of_mult.pregordr == 2)]

dic = {
    'id': 0,
    'first': True,
    'second': False,
}
pairings = []

for id in first_or_second_preg.caseid:
    id_preg = first_or_second_preg[first_or_second_preg.caseid == id]
    first_id_preg = id_preg[id_preg.pregordr == 1]
    first_outcome = first_id_preg.outcome.values[0]

    second_id_preg = id_preg[id_preg.pregordr == 2]
    second_outcome = second_id_preg.outcome.values[0]

    if first_outcome == 2 or first_outcome == 6 or second_outcome == 2 or second_outcome == 6:
        continue
    
    pair_success = {
        'id': id,
        'success_1': first_outcome == 1,
        'success_2': second_outcome == 1,
    }
    pairings.append(pair_success)