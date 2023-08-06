#!/usr/bin/env python

'''
foxglovetree/__init__.py - Foxglovetree module, the first version
'''

__author__  = 'Kohji'
__date__    = '2023-04-01'
__version__ = 0.1

series = 4

def factorial(k: int) -> int:
  y = 1
  if k == 0: return y
  for i in range(k): y *= (i + 1)
  return y

def cos(*args) -> float:
  global series
  x = args[0]
  if len(args) == 2: series = int(args[1])
  y = 0
  for i in range(series):
    y += ((-1) ** i) * (x ** (i * 2)) / factorial(i * 2)
  return y

if __name__ == '__main__':
  print(__file__.split('/')[-1].split('.')[0], __version__)
