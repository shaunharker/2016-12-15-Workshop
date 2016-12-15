### Fibration.py
### MIT LICENSE 2016 Shaun Harker

import graphviz
from collections import defaultdict, Counter

class Fibration:
  """
  Implements a cell fibration
  """
  def __init__(self, complex_, poset_, cell_fibration_):
    """
    complex_        : the underlying complex
    poset_          : the target poset
    cell_fibration_ : a function from complex.cells() to poset
              such that the preimages of down sets 
              correspond to closed subcomplexes
    """
    self.complex_ = complex_
    self.poset_ = poset_
    self.cell_fibration_ = cell_fibration_
    self.preimages_ = defaultdict(set)
    for cell in self.complex(): self.preimages_[self(cell)].add(cell) 

  def complex(self):
    """
    Return the associated complex
    """
    return self.complex_

  def poset(self):
    """
    Return the associated poset
    """
    return self.poset_

  def cell_fibration(self):
    """
    Return the map from cells to poset vertices
    """
    return self.cell_fibration_

  def __call__(self, cell):
    """
    If given a cell, return the corresponding poset vertex
    """
    if cell not in self.complex().cells():
      raise ValueError("Fibration not defined for cell presented")
    return self.cell_fibration_[cell]

  def preimage(self, poset_vertex):
    """
    Return the preimage of the cell fibration map
    """
    return self.preimages_[poset_vertex]

  def graphviz(self):
    """ Return a graphviz string describing the graph and its labels """
    gv = 'digraph {\n'
    indices = { v : str(k) for k,v in enumerate(self.poset().vertices())}
    def vertex_label(v):
      dim_counts = Counter([ cell.dimension() for cell in self.preimage(v) ])
      if dim_counts:
        return str(v) + ':('+','.join([str(dim_counts[i]) for i in range(0,self.complex().dimension()+1)])+')'
      else:
        return str(v)
    for v in self.poset().vertices(): 
      gv += indices[v] + '[label="' + vertex_label(v) + ('", style=filled, fillcolor=cyan];\n' if self.preimage(v) else '"];\n')
    for v in self.poset().vertices(): 
      for u in self.poset().children(v):
        gv += indices[v] + ' -> ' + indices[u] + ';\n'
    return gv + '}\n'

  def _repr_svg_(self):
    return graphviz.Source(self.graphviz())._repr_svg_()
