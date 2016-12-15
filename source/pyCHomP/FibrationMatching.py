### FibrationMatching.py
### MIT LICENSE 2016 Shaun Harker

from MorseMatching import *
from Subcomplex import *

def FibrationMatching(fibration):
  """
  We produce a discrete Morse theory acyclic partial matching
  for fibration.complex() which respects the fibration in the
  sense that M(K) = Q iff fibration(K) = fibration(Q)
  """
  M = { v : MorseMatching(Subcomplex(fibration.complex(), fibration.preimage(v))) for v in fibration.poset().vertices()}
  return lambda cell : M[fibration(cell)](cell)
