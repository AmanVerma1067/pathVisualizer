from typing import List, Tuple, Dict, Optional
import numpy as np

def bellman_ford_grid(grid: np.ndarray, start: int, end: int, rows: int, cols: int) -> Tuple[List[int], List[int]]:
    """
    Bellman-Ford algorithm implementation
    Returns: (visited_order, path_indexes)
    """
    start_pos = (start // cols, start % cols)
    end_pos = (end // cols, end % cols)
    
    # Build adjacency list
    graph = {}
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                continue
            pos = (r, c)
            graph[pos] = []
            for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ny, nx = r + dy, c + dx
                if 0 <= ny < rows and 0 <= nx < cols and grid[ny, nx] != 1:
                    graph[pos].append((ny, nx))
    
    # Initialize
    distances = {start_pos: 0}
    parent = {}
    visited_order = [start]
    visited = {start_pos}
    
    # Add neighbors of start
    for neighbor in graph.get(start_pos, []):
        distances[neighbor] = 1
        parent[neighbor] = start_pos
        visited.add(neighbor)
        visited_order.append(neighbor[0] * cols + neighbor[1])
        if neighbor == end_pos:
            break
    
    # Relax edges V-1 times
    for _ in range(len(graph) - 1):
        updated = False
        for node in graph:
            if node not in distances:
                continue
            dist_node = distances[node]
            
            for neighbor in graph[node]:
                new_dist = dist_node + 1
                
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parent[neighbor] = node
                    updated = True
                    
                    if neighbor not in visited:
                        visited.add(neighbor)
                        visited_order.append(neighbor[0] * cols + neighbor[1])
                    
                    if neighbor == end_pos:
                        break
        
        if not updated or end_pos in distances:
            break
    
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