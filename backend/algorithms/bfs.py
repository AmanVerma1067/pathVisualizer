from collections import deque
from typing import List, Tuple
import numpy as np

def bfs_grid(grid: np.ndarray, start: int, end: int, rows: int, cols: int) -> Tuple[List[int], List[int]]:
    """
    BFS algorithm implementation
    Returns: (visited_order, path_indexes)
    """
    start_pos = (start // cols, start % cols)
    end_pos = (end // cols, end % cols)
    
    visited = set([start_pos])
    visited_order = [start]
    parent = {}
    
    queue = deque([start_pos])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    found = False
    
    while queue and not found:
        current = queue.popleft()
        
        if current == end_pos:
            found = True
            break
            
        for dy, dx in directions:
            ny, nx = current[0] + dy, current[1] + dx
            
            if 0 <= ny < rows and 0 <= nx < cols:
                neighbor = (ny, nx)
                neighbor_idx = ny * cols + nx
                
                if grid[ny, nx] != 1 and neighbor not in visited:
                    visited.add(neighbor)
                    visited_order.append(neighbor_idx)
                    parent[neighbor] = current
                    queue.append(neighbor)
    
    # Reconstruct path
    path = []
    if found:
        current = end_pos
        while current != start_pos:
            path.append(current[0] * cols + current[1])
            current = parent[current]
        path.append(start)
        path.reverse()
    
    return visited_order, path