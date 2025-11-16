import heapq
from typing import List, Tuple
import numpy as np

def dijkstra_grid(grid: np.ndarray, start: int, end: int, rows: int, cols: int) -> Tuple[List[int], List[int]]:
    """
    Dijkstra's algorithm implementation
    Returns: (visited_order, path_indexes)
    """
    start_pos = (start // cols, start % cols)
    end_pos = (end // cols, end % cols)
    
    visited = set()
    visited_order = []
    distances = {start_pos: 0}
    parent = {}
    
    pq = [(0, start_pos)]
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
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
                neighbor_idx = ny * cols + nx
                
                if grid[ny, nx] == 1 or neighbor in visited:
                    continue
                    
                new_dist = current_dist + 1
                
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
    
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