### ConnectionFibration.py
### MIT LICENSE 2016 Shaun Harker

from FibrationMatching import *
from MorseFibration import *

import functools

def composition(functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def ConnectionFibration(fibration):
  """
  Given a fibration, return a 
  strictly equivalent connection fibration
  """
  
  # We need to detect when we have finished
  # Note -- for fields, this works. If not a field, it
  # could mean there is some torsional subgroup
  def isConnectionFibration(f):
    M = FibrationMatching(f)
    return all( M(v) == v for v in f.complex().cells() )

  # Iterate until fixed point is reached
  f = fibration
  phi = []
  psi = []
  while not isConnectionFibration(f): 
    f = MorseFibration(f)
    phi.append(lambda chain : f.complex().lower(chain))
    psi.append(lambda chain : f.complex().lift(chain))
  return f, (composition(reversed(phi)),composition(psi))
