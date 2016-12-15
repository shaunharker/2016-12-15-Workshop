### MorseComplex.py
### MIT LICENSE 2016 Shaun Harker

from Chain import *

class MorseComplex:
  """
  Class to hold the reduced complex achieved via
  discrete Morse theory
  """
  def __init__(self, supercomplex_, critical_cells_, homotopy_):
    """
    Given a complex C and a Morse homotopy, construct:
      * the associated Morse complex
      * the discrete Morse chain equivalences 
          lower : C -> M, lift : M -> C
    """
    self.supercomplex_ = supercomplex_
    self.critical_cells_ = frozenset(critical_cells_)
    self.homotopy_ = homotopy_
    self.ring_ = self.supercomplex().ring()
    self.dimension_ = max( cell.dimension() for cell in self );

  def __iter__(self):
    """
    Allows for the semantics
      [cell for cell in complex]
    """
    return iter(self.cells())

  def ring(self):
    """
    Return the ring used by the complex
    """
    return self.ring_

  def homotopy(self, chain):
    """
    Apply the discrete Morse homotopy
    """
    return self.homotopy_(chain)
    
  def supercomplex(self):
    """
    Return the original complex this 
    Morse complex is a reduction of
    """
    return self.supercomplex_

  def cells(self):
    """
    Return the set of cells 
    """
    return self.critical_cells_

  def dimension(self):
    """
    Return the dimension of the complex
    """
    return self.dimension_

  def include(self, chain):
    """
    Trivial inclusion
    """
    if not all( cell in self.cells() for cell in chain ):
      raise ValueError("MorseComplex.include: chain does not consist entirely of critical cells")
    return chain

  def project(self, chain):
    """
    Project away all cells except critical cells
    """
    return sum((chain[cell] * ElementaryChain(cell,self.ring()) for cell in chain if cell in self.cells()), Chain(chain.dimension(),self.ring()))

  def boundary(self, chain_or_cell):
    """
    Implement the Morse complex boundary
    """
    chain = chain_or_cell if isinstance(chain_or_cell, Chain) else ElementaryChain(chain_or_cell, self.ring())
    return self.lower(self.supercomplex().boundary(self.include(chain)))

  def lower(self, chain):
    """
    Implements chain equivalence lower : C -> M
    """
    return self.project(chain - self.supercomplex().boundary(self.homotopy(chain)))

  def lift(self,chain):
    """
    Implements chain equivalence lift : M -> C
    """
    included_chain = self.include(chain)
    return included_chain - self.homotopy(self.supercomplex().boundary(included_chain))
