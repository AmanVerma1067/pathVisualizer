from typing import List, Tuple
import numpy as np

def dfs_grid(grid: np.ndarray, start: int, end: int, rows: int, cols: int) -> Tuple[List[int], List[int]]:
    """
    DFS algorithm implementation
    Returns: (visited_order, path_indexes)
    """
    start_pos = (start // cols, start % cols)
    end_pos = (end // cols, end % cols)
    
    visited = set()
    visited_order = []
    parent = {}
    
    stack = [start_pos]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    found = False
    
    while stack and not found:
        current = stack.pop()
        
        if current in visited:
            continue
            
        visited.add(current)
        visited_order.append(current[0] * cols + current[1])
        
        if current == end_pos:
            found = True
            break
            
        for dy, dx in reversed(directions):
            ny, nx = current[0] + dy, current[1] + dx
            
            if 0 <= ny < rows and 0 <= nx < cols:
                neighbor = (ny, nx)
                
                if grid[ny, nx] != 1 and neighbor not in visited:
                    parent[neighbor] = current
                    stack.append(neighbor)
    
    # Reconstruct path
    path = []
    if found:
        current = end_pos
        while current != start_pos:
            path.append(current[0] * cols + current[1])
            if current not in parent:
                break
            current = parent[current]
        path.append(start)
        path.reverse()
    
    return visited_order, path