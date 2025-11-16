from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple
import numpy as np

from algorithms.dijkstra import dijkstra_grid
from algorithms.a_star import astar_grid
from algorithms.bfs import bfs_grid
from algorithms.dfs import dfs_grid
from algorithms.greedy_bfs import greedy_bfs_grid
from algorithms.bellman_ford import bellman_ford_grid
from algorithms.bi_swarm import bi_swarm_grid
from maze import generate_maze

app = FastAPI(title="Path Visualizer API")

# CORS configuration - Updated to allow your Vercel domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://path1067.vercel.app",  # Your production URL
        "https://*.vercel.app",          # All Vercel preview deployments
        "http://localhost:5173",         # Local development
        "http://localhost:3000",         # Alternative local port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GridRequest(BaseModel):
    grid: List[int]
    start: int
    end: int
    rows: int
    cols: int

class MazeRequest(BaseModel):
    start: int
    end: int
    rows: int
    cols: int

class PathResponse(BaseModel):
    visited_order: List[int]
    path_indexes: List[int]
    grid: List[int]

class MazeResponse(BaseModel):
    grid: List[int]

@app.get("/")
async def root():
    return {"message": "Path Visualizer API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/dijkstra", response_model=PathResponse)
async def run_dijkstra(request: GridRequest):
    try:
        grid = np.array(request.grid, dtype=np.int32).reshape(request.rows, request.cols)
        visited_order, path_indexes = dijkstra_grid(
            grid, request.start, request.end, request.rows, request.cols
        )
        return PathResponse(
            visited_order=visited_order,
            path_indexes=path_indexes,
            grid=grid.flatten().tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astar", response_model=PathResponse)
async def run_astar(request: GridRequest):
    try:
        grid = np.array(request.grid, dtype=np.int32).reshape(request.rows, request.cols)
        visited_order, path_indexes = astar_grid(
            grid, request.start, request.end, request.rows, request.cols
        )
        return PathResponse(
            visited_order=visited_order,
            path_indexes=path_indexes,
            grid=grid.flatten().tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bfs", response_model=PathResponse)
async def run_bfs(request: GridRequest):
    try:
        grid = np.array(request.grid, dtype=np.int32).reshape(request.rows, request.cols)
        visited_order, path_indexes = bfs_grid(
            grid, request.start, request.end, request.rows, request.cols
        )
        return PathResponse(
            visited_order=visited_order,
            path_indexes=path_indexes,
            grid=grid.flatten().tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dfs", response_model=PathResponse)
async def run_dfs(request: GridRequest):
    try:
        grid = np.array(request.grid, dtype=np.int32).reshape(request.rows, request.cols)
        visited_order, path_indexes = dfs_grid(
            grid, request.start, request.end, request.rows, request.cols
        )
        return PathResponse(
            visited_order=visited_order,
            path_indexes=path_indexes,
            grid=grid.flatten().tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/greedy-bfs", response_model=PathResponse)
async def run_greedy_bfs(request: GridRequest):
    try:
        grid = np.array(request.grid, dtype=np.int32).reshape(request.rows, request.cols)
        visited_order, path_indexes = greedy_bfs_grid(
            grid, request.start, request.end, request.rows, request.cols
        )
        return PathResponse(
            visited_order=visited_order,
            path_indexes=path_indexes,
            grid=grid.flatten().tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bellman-ford", response_model=PathResponse)
async def run_bellman_ford(request: GridRequest):
    try:
        grid = np.array(request.grid, dtype=np.int32).reshape(request.rows, request.cols)
        visited_order, path_indexes = bellman_ford_grid(
            grid, request.start, request.end, request.rows, request.cols
        )
        return PathResponse(
            visited_order=visited_order,
            path_indexes=path_indexes,
            grid=grid.flatten().tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bi-swarm", response_model=PathResponse)
async def run_bi_swarm(request: GridRequest):
    try:
        grid = np.array(request.grid, dtype=np.int32).reshape(request.rows, request.cols)
        visited_order, path_indexes = bi_swarm_grid(
            grid, request.start, request.end, request.rows, request.cols
        )
        return PathResponse(
            visited_order=visited_order,
            path_indexes=path_indexes,
            grid=grid.flatten().tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/maze", response_model=MazeResponse)
async def create_maze(request: MazeRequest):
    try:
        grid = generate_maze(request.rows, request.cols, request.start, request.end)
        return MazeResponse(grid=grid.flatten().tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)