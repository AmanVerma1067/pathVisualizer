from collections import deque
from typing import List, Tuple, Set, Dict
import numpy as np

def bi_swarm_grid(grid: np.ndarray, start: int, end: int, rows: int, cols: int) -> Tuple[List[int], List[int]]:
    """
    Bidirectional Swarm algorithm implementation
    Returns: (visited_order, path_indexes)
    """
    start_pos = (start // cols, start % cols)
    end_pos = (end // cols, end % cols)
    
    # Forward search from start
    forward_queue = deque([start_pos])
    forward_visited = {start_pos}
    forward_parent = {}
    
    # Backward search from end
    backward_queue = deque([end_pos])
    backward_visited = {end_pos}
    backward_parent = {}
    
    visited_order = [start]
    meeting_point = None
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while forward_queue and backward_queue and meeting_point is None:
        # Forward search step
        level_size = len(forward_queue)
        for _ in range(level_size):
            current = forward_queue.popleft()
            
            if current in backward_visited:
                meeting_point = current
                break
                
            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                
                if 0 <= ny < rows and 0 <= nx < cols:
                    neighbor = (ny, nx)
                    
                    if grid[ny, nx] != 1 and neighbor not in forward_visited:
                        forward_visited.add(neighbor)
                        forward_parent[neighbor] = current
                        forward_queue.append(neighbor)
                        visited_order.append(ny * cols + nx)
                        
                        if neighbor in backward_visited:
                            meeting_point = neighbor
                            break
            
            if meeting_point:
                break
        
        if meeting_point:
            break
            
        # Backward search step
        level_size = len(backward_queue)
        for _ in range(level_size):
            current = backward_queue.popleft()
            
            if current in forward_visited:
                meeting_point = current
                break
                
            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                
                if 0 <= ny < rows and 0 <= nx < cols:
                    neighbor = (ny, nx)
                    
                    if grid[ny, nx] != 1 and neighbor not in backward_visited:
                        backward_visited.add(neighbor)
                        backward_parent[neighbor] = current
                        backward_queue.append(neighbor)
                        visited_order.append(ny * cols + nx)
                        
                        if neighbor in forward_visited:
                            meeting_point = neighbor
                            break
            
            if meeting_point:
                break
    
    # Reconstruct path
    path = []
    if meeting_point:
        # Forward path: start -> meeting
        forward_path = []
        current = meeting_point
        while current != start_pos:
            forward_path.append(current[0] * cols + current[1])
            if current not in forward_parent:
                break
            current = forward_parent[current]
        forward_path.append(start)
        forward_path.reverse()
        
        # Backward path: meeting -> end
        backward_path = []
        current = meeting_point
        while current != end_pos:
            if current not in backward_parent:
                break
            current = backward_parent[current]
            backward_path.append(current[0] * cols + current[1])
        
        path = forward_path + backward_path
    
    return visited_order, path