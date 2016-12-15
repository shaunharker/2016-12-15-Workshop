### Chain.py
### MIT LICENSE 2016 Shaun Harker

class Chain:
  """
  Implements a chain in a cell complex
  """
  def __init__(self, dimension_, ring_):
    self.D = dimension_
    self.R = ring_
    self.zero = self.ring()(0)
    self.data = {}

  def dimension(self):
    """
    Return dimension associated with chain
    """
    return self.D

  def ring(self):
    """
    Return ring associated with chain
    """
    return self.R

  def __iter__(self):
    """
    Allows for the semantics
      [cell for cell in chain]
    """
    return iter(self.data)

  def __setitem__(self, key, item):
    """
    Allows for the semantics
      chain[cell] = coefficient
    """
    self.data[key] = item 

  def __getitem__(self, key):
    """
    Allows for the semantics
      coefficient = chain[cell]
    """
    return self.data.get(key, self.zero)

  def __add__(self, rhs):
    """
    Allows for the semantics
      chain1 = chain2 + chain3
    """
    result = Chain(self.dimension(),self.ring())
    for cell in self.data:
      result[cell] = self[cell]
    for cell in rhs:
      result[cell] = result.data.get(cell,self.zero) + rhs[cell]
    result.data = { key : result.data[key] for key in result.data if result.data[key] != self.zero }

    return result

  def __sub__(self, rhs):
    """
    Allows for the semantics
      chain1 = chain2 + chain3
    """
    result = Chain(self.dimension(),self.ring())
    for cell in self.data:
      result[cell] = self[cell]
    for cell in rhs:
      result[cell] = result.data.get(cell,self.zero) - rhs[cell]
    result.data = { key : result.data[key] for key in result.data if result.data[key] != self.zero }
    return result

  def __mul__(self, rhs):
    """
    Allows for the semantics
      chain1 = chain2 * coef
    """
    result = Chain(self.dimension(),self.ring())
    if rhs != self.zero:
      for cell in self.data:
        result[cell] = self[cell] * rhs
    return result

  def __rmul__(self, lhs):
    """
    Allows for the semantics
      chain1 = coef * chain2
    """
    result = Chain(self.dimension(),self.ring())
    if lhs != self.zero:
      for cell in self.data:
        result[cell] = lhs * self[cell]
    return result

  def __repr__(self):
    """
    Provide an unambiguous string representation
    """
    result = '+'.join([ '(' + str(self[cell]) + ')*[' + str(cell) + ']' for cell in self ])
    return result if result else "0"

  def __str__(self):
    """
    Provide a human readable string
    """
    result = '+'.join([ '(' + str(self[cell]) + ')*[' + str(cell) + ']' for cell in self ])
    return result if result else "0"

def ElementaryChain(cell, ring = int):
  """
  Return an elementary chain corresponding to cell
  """
  result = Chain(cell.dimension(), ring)
  result[cell] = ring(1)
  return result
