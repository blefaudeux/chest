# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:58:12 2013

@author: blefaudeux
"""

import random as rdm

def randomSeqGenerator(alphabet, sequence_length):
  list = []

  for i in range(sequence_length):
    list.append(alphabet[rdm.randint(0, len(alphabet) -1)])

  return list

def run():

  # Get the number of basis in the sequence
  n_items_gathered = False

  while not n_items_gathered :
    n_items = raw_input("Number of bases in the random sequence :\n")
    n_items_gathered = n_items.isdigit()

  # Generate the random seq :
  list = randomSeqGenerator(('A', 'T', 'C', 'G'), int(n_items))

  # Return result
  print "Generated sequence :"
  for item in list:
    print item,

  raw_input("\n\n\nPress a key to exit")


## Execute script
run()