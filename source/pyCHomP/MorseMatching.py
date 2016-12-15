### MorseMatching.py
### MIT LICENSE 2016 Shaun Harker

from collections import defaultdict

def MorseMatching(cellcomplex):
  """
  Return an acyclic partial matching M on the cells of cellcomplex.
  i.e. an involution M : Cells -> Cells
  such that 
    * M(a) = b implies | dim(a) - dim(b) | = 1
    * If we define 
      * Aces := { v : M(v) = v }
      * Queens := { v : dim(v) < dim(M(v)) }
      * Kings := { v : dim(v) > dim(M(v)) }
    * Then, for Q1, Q2 \in Queen, 
        Q1 < Q2 whenever Q1 in bd(M(Q2)) 
      is a strict partial order. 
  """
  # Our approach is the following greedy algorithm
  # We iterate the following procedure:
  #   At each stage a cell is either classified or unclassified.
  #   We check if there are any unclassified cells with precisely one
  #   unclassified cell in the boundary.
  #   If there are, we form a K,Q pairs from them.
  #   Otherwise, we pick a minimal dimensional cell and classify it as A.
  # In order to implement this efficiently we need a way to 
  # quickly find unclassified cells with one unclassified cell in their boundary.
  # One approach is to be able to efficiently compute coboundary to do a reverse
  # lookup. However we do not require our complexes provide efficient algorithms
  # for computing the transpose of their boundary operator. This means that we
  # must build this information ourselves

  M = {}

  def bd(chain): return cellcomplex.boundary(chain)
  boundary_count = {}
  unlabelled = set()
  coreducible = set()
  ace_candidates = set()
  coboundary = defaultdict(set)
  for b in cellcomplex:
    unlabelled.add(b)
    boundary_cells = [ a for a in bd(b) ]
    boundary_count[b] = len(boundary_cells)
    if boundary_count[b] == 1:
      coreducible.add(b)
    if boundary_count[b] == 0:
      ace_candidates.add(b)
    for a in boundary_cells:
      coboundary[a].add(b)

  def process(removed_cell):
    unlabelled.remove(removed_cell)
    coreducible.discard(removed_cell)
    ace_candidates.discard(removed_cell)
    for cell in coboundary[removed_cell]:
      boundary_count[cell] -= 1
      if boundary_count[cell] == 1:
        coreducible.add(cell)
      if boundary_count[cell] == 0:
        coreducible.discard(cell)
        ace_candidates.add(cell)

  while unlabelled:
    if coreducible:
      K = coreducible.pop()
      Q = [ cell for cell in bd(K) if cell in unlabelled ][0]
      M[K] = Q
      M[Q] = K
      process(Q)
      process(K)
    else:
      A = ace_candidates.pop()
      M[A] = A
      process(A)

  return lambda cell : M[cell]

