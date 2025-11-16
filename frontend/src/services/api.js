// Use the production backend URL when in production
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.PROD 
    ? 'https://path-visualizer-backend.onrender.com' 
    : 'http://localhost:8000');

export const algorithmEndpoints = {
  dijkstra: '/api/dijkstra',
  astar: '/api/astar',
  bfs: '/api/bfs',
  dfs: '/api/dfs',
  greedyBfs: '/api/greedy-bfs',
  bellmanFord: '/api/bellman-ford',
  biSwarm: '/api/bi-swarm',
  maze: '/api/maze',
};

export async function runAlgorithm(endpoint, grid, start, end, rows, cols) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        grid: Array.from(grid),
        start,
        end,
        rows,
        cols,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorData.detail || 'Unknown error'}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error('Algorithm execution failed:', error);
    throw error;
  }
}

export async function generateMaze(start, end, rows, cols) {
  try {
    const response = await fetch(`${API_BASE_URL}${algorithmEndpoints.maze}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        start,
        end,
        rows,
        cols,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorData.detail || 'Unknown error'}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error('Maze generation failed:', error);
    throw error;
  }
}