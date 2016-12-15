### CubicalComplex.py
### MIT LICENSE 2016 Shaun Harker

import itertools
from Chain import *

# TODO: don't use raw cube data for cubical cells, too slow.
# Instead, create a library of cubes which memoizes result of boundary
# operations, and use their indices. Make the new implementation a 
# drop-in replacement of CubicalCell so that CubicalComplex will not
# even see the difference except in performance.  

class CubicalCell:
  def __init__(self, bounds_):
    """
    Create a cube from a tuple of tuples representing bounds
    """
    self.bounds_ = tuple( tuple(interval) for interval in bounds_)
    self.D = sum(interval[0] != interval[1] for interval in self.bounds())

  def bounds(self):
    """
    Return bounds of cube as list of intervals, 
    where intervals are length 2 tuples.
    Interpret non-degenerate intervals as open, 
    and degenerate intervals as closed.
    """
    return self.bounds_

  def dimension(self):
    return self.D

  def boundary(self, ring = int):
    """
    Return boundary of elementary chain
    in a hypothetical full complex
    """
    # d((x,y))  = (dx, y) + (-1)**(dim(x)) (x,dy)
    result = Chain(self.D - 1, ring)
    sign = 1
    for d, interval in enumerate(self.bounds()):
      if interval[0] == interval[1]: continue
      left = list(self.bounds())
      right = list(self.bounds())
      left[d] = (interval[0], interval[0])
      right[d] = (interval[1], interval[1])
      result[CubicalCell(left)] = ring( -sign ) 
      result[CubicalCell(right)] = ring( sign )
      sign = sign * -1
    return result
      
  def __repr__(self):
    """
    Provide an unambiguous string representation
    """
    return self.bounds().__repr__()

  def __str__(self):
    """
    Provide a human readable string
    """
    return "x".join([ '(' + str(interval[0]) + ',' + str(interval[1]) + ')' if interval[0] != interval[1] else '{' + str(interval[0]) + '}' 
      for interval in self.bounds() ])

  def __hash__(self):
    """
    Make CubicalCell hashable to enable
    usage as the keys in dictionaries
    """
    return hash(self.bounds())

  def __eq__(self, rhs):
    """
    CubicalCell equality testing
    (required for usability as dictionary key)
    """
    return (self.dimension() == rhs.dimension() and
           all ( lhs_interval == rhs_interval for (lhs_interval, rhs_interval) in zip(self.bounds(),rhs.bounds())))

class CubicalComplex:
  """
  CubicalComplex implementation.
  A type of cell complex.
  """
  def __init__(self, cells_, ring = int ):
    self.cells_ = frozenset(cells_)
    self.R = ring 
    self.D = max( cell.dimension() for cell in self );

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
    return self.R

  def cells(self):
    """
    Return the set of cells 
    """
    return self.cells_

  def dimension(self):
    """
    Return the dimension of the complex
    """
    return self.D 

  def boundary(self, chain_or_cell):
    """
    Return the boundary of the given chain or cell
    """
    if isinstance(chain_or_cell, CubicalCell):
      result = chain_or_cell.boundary(self.ring())
    else:
      result = sum([ chain_or_cell[cell] * cell.boundary(self.ring()) for cell in chain_or_cell ], Chain(self.dimension(), self.ring()))
    # Project out cells not in complex
    return sum([ result[cell] * ElementaryChain(cell,self.ring()) for cell in result if cell in self.cells() ], Chain(self.dimension(), self.ring()) )
    
def CubicalGrid( list_of_lists_of_thresholds ):
  """
  Make a Cubical Complex with all cells for a rectangular prism subdivided according to input
  Example: [ [1.0, 2.0, 3.0], [1.5, 2.0, 3.5] ] yields a 2D cubical complex with the following 
           2-cells:  [1.0,2.0] x [1.5,2.0]  [1.0,2.0] x [2.0,3.5] 
                     [2.0,3.0] x [1.5,2.0]  [3.0,3.0] x [2.0,3.5] 
           and 1-cells and 0-cells corresponding to the boundary cells of those 2-cells.
  """
  # The algorithm consists of constructing a set of CubicalCell objects to
  # pass to the constructor of CubicalComplex
  cells = set()
  # Function to turn a list [a,b,c] into [[a,b],[b,c],[a,a],[b,b],[c,c]]
  def make_intervals(list): return [ [a,b] for (a,b) in zip(list[:-1],list[1:]) ] + [ [a,a] for a in list ]
  # Map previous function onto input
  interval_lists = [ make_intervals(threshold_list) for threshold_list in list_of_lists_of_thresholds]
  # Form cartesian product and iterate through all possible products of intervals
  for element in itertools.product(*interval_lists):
    cells.add(CubicalCell(element))
  # Return cubical complex
  return cells
