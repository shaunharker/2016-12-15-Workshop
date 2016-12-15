### Subcomplex.py
### MIT LICENSE 2016 Shaun Harker

from Chain import *

class Subcomplex:
  """
  Implements a subcomplex
  """
  def __init__(self, supercomplex_, cells_):
    self.supercomplex_ = supercomplex_
    self.cells_ = frozenset(cells_)
    self.ring_ = supercomplex_.ring()
    self.dimension_ = max( [-1] + [ cell.dimension() for cell in self.cells() ])

  def __iter__(self):
    """
    Allows for the semantics
      [cell for cell in cubicalcomplex]
    """
    return iter(self.cells())

  def ring(self):
    """
    Return the ring used by the complex
    """
    return self.ring_

  def cells(self):
    """
    Return the set of cells 
    """
    return self.cells_

  def supercomplex(self):
    """
    Return the supercomplex, i.e. the complex this 
    complex is a subcomplex of
    """
    return self.supercomplex_

  def dimension(self):
    """
    Return the dimension of the complex
    """
    return self.dimension_

  def include(self, chain):
    """
    Return a chain to include in the supercomplex
    Note: this function does nothing except check to make sure
          that the chain really ought to live in the subcomplex 
          to begin with
    """
    if not all( cell in self.cells() for cell in chain ):
      raise ValueError("Subcomplex.include: chain does not belong to complex")
    return chain

  def project(self, chain):
    """
    Return the projection of a chain in the supercomplex
    into the current complex. (i.e. drop cells not in self.cells())
    """
    return sum((chain[cell] * ElementaryChain(cell, self.ring()) for cell in chain if cell in self.cells()), Chain(chain.dimension(), self.ring()))

  def boundary(self, chain_or_cell):
    """
    Return the boundary of a chain or cell
    """
    chain = chain_or_cell if isinstance(chain_or_cell, Chain) else ElementaryChain(chain_or_cell, self.ring())
    return self.project(self.supercomplex().boundary(self.include(chain)))
