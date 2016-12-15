### Braids.py
### MIT LICENSE 2016 Shaun Harker

from CubicalComplex import *
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

class BraidDiagram:
  def __init__(self, braid_skeleton):
    """
    Inputs:
      braid_skeleton : a list of lists such that 
         braid_skeleton[i][j] gives the value of strand i at position j
    Outputs:
      braid_specification: a tuple (n, m, x, pi) 
                           where n : number of strands 
                                 m : number of waypoints 
                                 x(i,j) means the value of strand i at position j
                                 pi is a permutation such that x(i,j+m) == x(pi(i),j)
    """
    self.n = len(braid_skeleton)
    self.m = len(braid_skeleton[0]) - 1
    self.permute_ = {}
    for i in range(0,self.n):
      for j in range(0,self.n):
        if braid_skeleton[i][self.m] == braid_skeleton[j][0]:
          self.permute_[i] = j
    self.braid_skeleton_ = braid_skeleton
      
  def __call__(self, i, j):
    """
    Return the height of strand i at position j
    """
    return self.braid_skeleton_[i][j]

  def pi(self,i):
    """
    pi is a permutation such that x(i,j+m) == x(pi(i),j)
    """
    return self.permute_[i]

  def lap(self, domain):
    """
    Compute the lap number for a domain
    """
    midpoints = [ sum(domain.bounds()[j]) / 2.0 for j in (range(0,self.m) + [0]) ] 
    return sum(self(i,j) <= midpoints[j] and self(i,j+1) >= midpoints[j+1] for j in range(0,self.m) for i in range(0,self.n))

  def __repr__(self):
    x = np.arange(self.m+1)
    for i in range(0,self.n):
      plt.plot(x, [self(i,j) for j in range(0,self.m+1)])
    plt.show()
    return "Braid Diagram"

def BraidComplex( braid_diagram ):
  """
  Overview:
    Given a specification for a "braids" dynamical system,
    return the associated cubical complex and flow graph.
  """

  # Unpack the input
  n = braid_diagram.n
  m = braid_diagram.m
  x = lambda i,j : braid_diagram(i,j)
  pi = lambda i : braid_diagram.pi(i)

  # Create the associated cubical complex
  thresholds = [ [float("-inf")] + sorted( [x(i,j) for i in range(0,n)] ) + [float("inf")] for j in range(0,m) ]
  complex = CubicalComplex(CubicalGrid(thresholds))

  # Construct the domains
  domains = [cell for cell in complex.cells() if cell.dimension() == m]
  walls = [cell for cell in complex.cells() if cell.dimension() == m-1]

  ## NOTE: DRY SMELL BEGIN
  # We need coboundary information
  coboundary = defaultdict(list)
  for b in complex:
    for a in [ a for a in complex.boundary(b) ]:
      coboundary[a].append(b)

  # We also need to know the top cells surrounding a vertex
  def star(cell):
    result = set()
    stack = [ v for v in coboundary[cell] ]
    while stack:
      v = stack.pop()
      result.add(v)
      for u in coboundary[v]:
        stack.append(u)
    return result
  ## NOTE: DRY SMELL END

  # Construct the edge set
  edges = defaultdict(set)
  for wall in walls:
    # A wall can have 1 adjacent domain if it is off at infinity
    if len(coboundary[wall]) == 1: continue
    # Otherwise, it has precisely 2 adjacent domains
    [u, v] = coboundary[wall]
    if braid_diagram.lap(u) <= braid_diagram.lap(v):
      edges[u].add(v)
    if braid_diagram.lap(u) >= braid_diagram.lap(v):
      edges[v].add(u)

  # Identify collapsed strands
  collapsed_strands = [ i for i in range(0,n) if pi(i) == i ]
  collapsed_vertices = [ CubicalCell([ [ x(i,j), x(i,j) ] for j in range(0,m) ]) for i in collapsed_strands ]

  # Connect all cubes in the star of any collapsed strand
  for v in collapsed_vertices:
    surrounding_walls = [ cell for cell in star(v) if cell.dimension() == m-1 ]
    for wall in surrounding_walls:
      if len(coboundary[wall]) == 1: continue
      [u, v] = coboundary[wall]
      edges[u].add(v)
      edges[v].add(u)

  return (complex, lambda v : edges[v] )
