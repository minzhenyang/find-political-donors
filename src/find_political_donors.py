#!/usr/bin/env python
import logging
import os
import sys
from itertools import groupby

def median(l):
    """Calculate median of a string list.
    afljdka
    """
    half = len(l) // 2
    l.sort()
    if not len(l) % 2:
        return round( (l[half - 1] + l[half]) / 2.0)
    return l[half]

# group by functions against a list and group by keys
# lists: input list to group by, 
# keys: lambda function for sorting and groupby
# aggr_index: index that aggregation function are against
# return a list with group by key, median/count/sum of indexed element in the list
# Improvement to be more generic on aggregate functions using a  hash to choose different 
# aggregate function on different index such as in the following options:
# {'count':index of item in the list,'sum':index,'mean':index}
def groupby_list(lists, keys, aggr_index):
	for k, records in groupby(sorted(lists, key=keys ), keys ):
		all_list = list(records)
		this_record=list(k)
		g_list = [ int(record[aggr_index] ) for record in all_list]
		c = len(g_list)
		s = sum(g_list)
		m = int(median(g_list))		
		this_record.extend([str(m), str(c), str(s)])
		d_list.append(this_record)
	return d_list	

# cumulative group by functions against a list and group by keys
# lists: input list to group by, 
# klist: index list for group by keys
# all_hash: hash table with keys and cumulative aggregate values
# all_list: list with keys, and cumulative median/count/sum
# aggr_index: index that aggregation function are against
def cum_groupby(lists, klist, all_hash, all_list,aggr_index):
	temp_hash = {}
	keys = '_'.join(klist)
	this_record = klist
	if keys in all_hash:
		g_list = all_hash.get(keys)
		g_list.append(int(line[aggr_index]))
		c = len(g_list)
		s = sum(g_list)
		m = int(median(g_list))	
		temp_hash[keys] = g_list
		this_record.extend([str(m), str(c), str(s)])
		all_list.append(this_record)
	else :
		temp_hash[keys] =  [ int(line[aggr_index]) ] 	
		this_record.extend([line[aggr_index], '1', line[aggr_index] ])
		all_list.append(this_record)	
	all_hash.update(temp_hash)

    
if __name__ == '__main__':
	logging.basicConfig(format = '%(asctime)s %(levelname)s: '
			'%(message)s', level = logging.INFO)
	if len(sys.argv) < 4:
		logging.exception('number of arugments needs to be 3')
		sys.exit(1)
	else:   
		fname = sys.argv[1]
		outzip = sys.argv[2]
		outdate = sys.argv[3]
		with open(fname) as fp:
			lines = [ m for m in [l.rstrip().split('|') for l in fp.readlines() ] if m[15] == '' ]
			d_list = []
			amt_list = []
			d_list = groupby_list(lines, lambda k:(k[0],k[13]), 14)
			
			hash_idzip = {}
			zip_list = []
			amt_list = []
			for line in lines:
				zipkey = [line[0],line[10][:5] ] 
				cum_groupby(line, zipkey, hash_idzip, zip_list,14)

		file1 = open(sys.argv[2],"w")
		with open(sys.argv[2],"w") as file1:
			for record in zip_list:
				file1.write('|'.join(record) + '\n')
				print('|'.join(record))

		with open(sys.argv[3],"w") as file2:
			for record in d_list:
				file2.write('|'.join(record) + '\n')
				print('|'.join(record))	