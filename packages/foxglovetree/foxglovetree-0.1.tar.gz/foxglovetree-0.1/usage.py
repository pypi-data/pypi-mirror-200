#!/usr/bin/env python

'''
usage.py - show how to use foxglovetree
'''

import sys
import math
import numpy
import foxglovetree

def calc_cos():
  x = float(sys.argv[1])

  cos_math         = math.cos(x)
  cos_numpy        = numpy.cos(x)
  cos_foxglovetree = foxglovetree.cos(x)

  print(f'cos({x}) = {cos_math} (math)')
  print(f'cos({x}) = {cos_numpy} (numpy)')
  print(f'cos({x}) = {cos_foxglovetree} (foxglovetree)')

  for i in range(10):
    print(f'{i:4d}: cos({x}) = {foxglovetree.cos(x, i)}')

if __name__ == '__main__':
  if len(sys.argv) < 2: sys.exit(20)
  calc_cos()
