# Chris Cook
# 4553 Spatial Data Structures
# Program 2 Part 1
# Due: June 20, 2017

import pprint as pp
import os,sys

# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))

def read_crime_data(filename):
    keys = []
    crimes = []

    got_keys = False

   # filtered_crimes_bronx.csv
    with open(DIRPATH+'/../NYPD_CrimeData/filtered_crimes_'+filename+'.csv') as f:
    # with open(DIRPATH+'/'+'nypd_small_data.txt') as f:
        for line in f:
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            line = line.strip().split(',')
            if not got_keys:
                keys = line
               # print(keys)
                got_keys = True
                continue

        #d = {}
        # for i in range(len(line)-1):
        #     d[keys[i]] = line[i]
            crimes.append(line)
    return crimes

#for crime in crimes:
   # print((crime[19],crime[20]))
