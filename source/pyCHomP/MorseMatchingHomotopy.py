### MorseMatchingHomotopy.py
### MIT LICENSE 2016 Shaun Harker

from queue import *
import copy
from TopologicalSort import *
from Chain import *

def MorseMatchingHomotopy(M, cellcomplex):
  """
  Return a function to evaluate the discrete Morse homotopy 
  associated with an acyclic partial matching
  """
  # Semantic sugar
  def bd(chain): return cellcomplex.boundary(chain)
  def dim(chain_or_cell): return chain_or_cell.dimension()
  def isAce(cell): return dim(cell) == dim(M(cell))
  def isKing(cell): return dim(cell) > dim(M(cell))
  def isQueen(cell): return dim(cell) < dim(M(cell))
  # Compute critical cells from matching
  critical_cells = [ cell for cell in cellcomplex if isAce(cell) ]
  # Homotopy function definition
  def homotopy(chain):
    """
    Implement the discrete Morse homotopy gamma
    """
    # We clone the input chain to prevent unexpected alterations
    work_chain = copy.deepcopy(chain)

    # We create a dictionary "priority" which gives the rank of queens.
    # Lower priority numbers will be processed first (i.e. priority ranking, not priority value)
    Queens = [Q for Q in cellcomplex if isQueen(Q)]
    def AdjacentQueens(Q): return [ q for q in bd(M(Q)) if isQueen(q) and q != Q ]
    priority = { Q : rank for (rank, Q) in enumerate(TopologicalSort(Queens, AdjacentQueens)) }

    # We arrange the priority queue for queens.
    # We use an auxiliary set "enqueued" to prevent the same queen from being
    # placed in the priority queue twice.
    work_queue = PriorityQueue()
    enqueued = set()
    def enqueue(list_of_queens):
      for Q in list_of_queens:
        if Q in enqueued: continue
        enqueued.add(Q)
        work_queue.put((-priority[Q], Q))

    # Initialize queue with the queens in the original chain
    enqueue([ Q for Q in work_chain if isQueen(Q) ])

    # Make a zero chain of correct dimension to store result in
    gamma_chain = Chain(dim(chain) + 1, cellcomplex.ring())

    # We iteratively process the maximal queen in "work_chain", each time
    # adding the appropriate multiple of the boundary of its mating king in 
    # order to cancel it. Doing this can add new queens, which we enqueue.
    # A theorem prevents previously processed queens from being "new_queens" 
    # We keep track of the king chain as we go.
    while not work_queue.empty():
      (rank, Q) = work_queue.get()
      a = work_chain[Q]
      if a == 0: continue
      K = M(Q)
      bd_K = bd(K)
      b = bd_K[Q]
      c = -a/b
      gamma_chain[K] += c
      work_chain += c * bd_K
      enqueue([ q for q in bd_K if isQueen(q) and q != Q ])
    return gamma_chain
  return (critical_cells, homotopy)
