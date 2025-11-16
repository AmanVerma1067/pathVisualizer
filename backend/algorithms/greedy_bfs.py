import heapq
from typing import List, Tuple
import numpy as np

def heuristic(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """Manhattan distance heuristic"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def greedy_bfs_grid(grid: np.ndarray, start: int, end: int, rows: int, cols: int) -> Tuple[List[int], List[int]]:
    """
    Greedy Best-First Search implementation
    Returns: (visited_order, path_indexes)
    """
    start_pos = (start // cols, start % cols)
    end_pos = (end // cols, end % cols)
    
    visited = set()
    visited_order = []
    parent = {}
    
    pq = [(heuristic(start_pos, end_pos), start_pos)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while pq:
        _, current = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        visited_order.append(current[0] * cols + current[1])
        
        if current == end_pos:
            break
            
        for dy, dx in directions:
            ny, nx = current[0] + dy, current[1] + dx
            
            if 0 <= ny < rows and 0 <= nx < cols:
                neighbor = (ny, nx)
                
                if grid[ny, nx] == 1 or neighbor in visited:
                    continue
                    
                parent[neighbor] = current
                h = heuristic(neighbor, end_pos)
                heapq.heappush(pq, (h, neighbor))
    
    # Reconstruct path
    path = []
    if end_pos in parent or end_pos == start_pos:
        current = end_pos
        while current != start_pos:
            path.append(current[0] * cols + current[1])
            if current not in parent:
                break
            current = parent[current]
        path.append(start)
        path.reverse()
    
    return visited_order, path