'''  
=================================================================
	@version  2.0
	@author   Chinonso Okereke
	@title    Testing.


	Random Priorization module.
=================================================================
'''
import random
import subprocess
import sys

'''Intializations'''


def pri(tests):

	#random.shuffle(tests) python2 code

	#python3 code
	# Convert the dictionary values to a list
	items = list(tests.items())
	list_of_lists = [list(item) for item in items]
	# print(items)
	# print(list_of_lists)

	# Shuffle the list of values
	random.shuffle(items)

	# If you need to maintain the keys and shuffle the values, you can create a new dictionary
	priority_tests = items
	# print(priority_tests)
	pr_shuffle = dict(priority_tests)
	shuffled_tests = dict(items)
	# shuffled_tests = dict(zip(tests.keys(), values))

	with open('output_file1.txt', 'w') as f:
		for key, value in shuffled_tests.items():
			f.write(f"{key}:{value}\n")

	with open('output_file2.txt', 'w') as f:
		for key, value in pr_shuffle.items():
			f.write(f"{key}:{value}\n")
	rand_ids = list(pr_shuffle.keys())

	return shuffled_tests, rand_ids






