import numpy as np

def build_markov_matrix_from_edges(edges,n_nodes):
    """
    Build a dense column-stochastic Markov matrix from an edge list.
    edges: list of (from_node, to_node) tuples (directed edges)
    """
    # Initialize adjacency matrix A[i, j] = 1 if j -> i
    A = np.zeros((n_nodes, n_nodes))
    for u, v in edges:
        A[v, u] = 1.0

    # Handle dangling nodes (columns with no outgoing edges)
    col_sums = A.sum(axis=0)
    for j in range(n_nodes):
        if col_sums[j] == 0:
            A[:, j] = 1.0
    col_sums = A.sum(axis=0)

    # Normalize columns -> make it column-stochastic
    M = A / col_sums
    return M

def pagerank(M, damping=0.85, tol=1e-6, max_iter=1000):
    """
    Compute PageRank vector for a dense Markov matrix.
    """
    n = M.shape[0]
    teleport = np.ones(n) / n
    rank = teleport.copy()

    for i in range(max_iter):
        new_rank = damping * (M @ rank) + (1 - damping) * teleport
        norm = np.linalg.norm(new_rank - rank, 1)
        if norm <= tol:
            print(f"Converged after {i+1} iterations.")
            return new_rank
        rank = new_rank

    print(f"Did not converge max_it = {max_iter}, norm = {norm} > {tol}")
    return rank

# Example usage
if __name__ == "__main__":
    # https://commons.wikimedia.org/wiki/File:PageRanks-Example.svg
    # Edge list (from -> to)
    edges = [
        (1, 2), # B -> C
        (2, 1), # C -> B
        (3, 0),
        (3, 1),
        (4, 1),
        (4, 3),
        (4, 5),
        (5, 1),
        (5, 4),
        (6, 1),
        (6, 4),
        (7, 1),
        (7, 4),
        (8, 1),
        (8, 4),
        (9, 4),
        (10, 4),
    ]
    nodes = 11

    M = build_markov_matrix_from_edges(edges,nodes)
    pr = pagerank(M)

    print("\nMarkov matrix (M):")
    print(M)
    print("\nPageRank vector:")
    for i, val in enumerate(pr):
        print(f"Node {i}: {val:.4f}")
    print("Sum of PageRank values:", np.sum(pr))

