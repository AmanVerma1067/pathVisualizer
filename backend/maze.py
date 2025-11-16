import numpy as np
import random
from typing import Tuple

def generate_maze(rows: int, cols: int, start: int, end: int) -> np.ndarray:
    """
    Generate a maze using depth-first search
    Returns: maze grid as numpy array
    """
    # Initialize all cells as walls
    grid = np.ones((rows, cols), dtype=np.int32)
    
    start_pos = (start // cols, start % cols)
    end_pos = (end // cols, end % cols)
    
    # Make start and end positions open
    grid[start_pos] = 0
    grid[end_pos] = 0
    
    # Start maze generation from (1, 1)
    if rows > 2 and cols > 2:
        start_maze = (1, 1)
        grid[start_maze] = 0
        
        stack = [start_maze]
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            current = stack[-1]
            neighbors = []
            
            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                
                if 0 <= ny < rows and 0 <= nx < cols and grid[ny, nx] == 1:
                    neighbors.append((ny, nx))
            
            if neighbors:
                next_cell = random.choice(neighbors)
                # Carve path
                wall_y = (current[0] + next_cell[0]) // 2
                wall_x = (current[1] + next_cell[1]) // 2
                grid[wall_y, wall_x] = 0
                grid[next_cell] = 0
                stack.append(next_cell)
            else:
                stack.pop()
    
    # Ensure start and end are accessible
    grid[start_pos] = 0
    grid[end_pos] = 0
    
    return grid