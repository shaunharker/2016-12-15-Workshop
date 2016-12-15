### MorseFibration.py
### MIT LICENSE 2016 Shaun Harker

from MorseMatchingHomotopy import *
from FibrationMatching import *
from MorseComplex import *
from Fibration import *

def MorseFibration(fibration):
  """
  Given a fibration, we construct a new fibration
  which is strictly equivalent via discrete Morse theory
  """
  critical_cells, homotopy = MorseMatchingHomotopy(FibrationMatching(fibration), fibration.complex())
  morse_complex = MorseComplex(fibration.complex(), critical_cells, homotopy)
  return Fibration(morse_complex, fibration.poset(), fibration.cell_fibration())