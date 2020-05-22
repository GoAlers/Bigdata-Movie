import sys

#
for line in sys.stdin:
	ss = line.strip().split(' ')
	for word in ss:
		print('\t'.join([word.strip(), '1']))
#
# import sys
# for line in sys.stdin:
# 	ss=line.strip().split(' ')
# 	for word in ss:
# 		print ('\t'.join(word.strip(),'1'))
