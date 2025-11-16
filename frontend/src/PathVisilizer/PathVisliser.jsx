import styled from "styled-components";
import Constants from "./constants.js";
import { getTwoUniqueRandomNumbers } from "../HelperFunctions.js";
import { useEffect, useState } from "react";

// Import Components
import Node from "./Node.jsx";
import Nav from "./Components/Navbar.jsx";
import Loading from "./Components/Loading.jsx";
import AlgoPicker from "./Components/Card.jsx";
import Benchmark from "./Components/Benchmark.jsx";

// Import API
import { runAlgorithm, generateMaze, algorithmEndpoints } from "../services/api.js";

const Columns = Math.floor(window.innerWidth / Constants.nodeWidth);
const Rows = Math.floor(window.innerHeight / Constants.nodeHeight);

export default function PathVisualizer() {
    const [cellState, setCellState] = useState(null);
    const [initialized, setInitialized] = useState(false);
    const [mouseDown, setMouseDown] = useState(false);
    const [AlgoName, setAlgoName] = useState("Dijkstra");
    const [pickerActive, setPickerActive] = useState(false);
    const [speedModifier, setSpeedModifier] = useState(Constants.fastSpeedModifier);
    const [dragMode, setDragMode] = useState(null);
    const [isPlayed, setisPlayed] = useState(false);
    const [previousWallPositions, setPreviousWallPositions] = useState([]);
    const [isAnimating, setIsAnimating] = useState(false);
    const [visitedNodes, setVisitedNodes] = useState(0);
    const [totalNonWallNodes, setTotalNonWallNodes] = useState(0);

    const idxes = getTwoUniqueRandomNumbers(Rows * Columns - 1);
    const [start, setStart] = useState(idxes[0]);
    const [end, setEnd] = useState(idxes[1]);
    const [cellsArray, setCellsArray] = useState([]);

    function getSpeedName() {
        switch (speedModifier) {
            case Constants.fastSpeedModifier:
                return "FAST";
            case Constants.normalSpeedModifier:
                return "NORMAL";
            case Constants.slowSpeedModifier:
                return "SLOW";
            default:
                return "FAST";
        }
    }

    function toggleSpeed() {
        const speedOrder = [
            Constants.fastSpeedModifier,
            Constants.normalSpeedModifier,
            Constants.slowSpeedModifier
        ];

        const currentIndex = speedOrder.indexOf(speedModifier);
        const nextIndex = (currentIndex + 1) % speedOrder.length;
        setSpeedModifier(speedOrder[nextIndex]);
    }

    // Initialize grid
    useEffect(() => {
        const buffer = new Uint8Array(Rows * Columns);
        setCellState(buffer);
        setInitialized(true);
    }, []);

    function setWall(idx, flag) {
        if (!cellState || idx >= Rows * Columns) return;
        if (idx === start || idx === end) return;
        const newState = new Uint8Array(cellState);
        newState[idx] = flag;
        setCellState(newState);
    }

    function handleNodeDrag(idx) {
        if (dragMode === 'start' && idx !== end) {
            if (cellState[idx] === 1) {
                setPreviousWallPositions(prev => [...prev, idx]);
                const newState = new Uint8Array(cellState);
                newState[idx] = 0;
                setCellState(newState);
            }
            if (previousWallPositions.includes(start)) {
                const newState = new Uint8Array(cellState);
                newState[start] = 1;
                setCellState(newState);
                setPreviousWallPositions(prev => prev.filter(pos => pos !== start));
            }
            setStart(idx);
        } else if (dragMode === 'end' && idx !== start) {
            if (cellState[idx] === 1) {
                setPreviousWallPositions(prev => [...prev, idx]);
                const newState = new Uint8Array(cellState);
                newState[idx] = 0;
                setCellState(newState);
            }
            if (previousWallPositions.includes(end)) {
                const newState = new Uint8Array(cellState);
                newState[end] = 1;
                setCellState(newState);
                setPreviousWallPositions(prev => prev.filter(pos => pos !== end));
            }
            setEnd(idx);
        }
    }

    async function mazify() {
        setIsAnimating(true);
        try {
            const result = await generateMaze(start, end, Rows, Columns);
            animateMazeGeneration(result.grid);
        } catch (error) {
            console.error("Maze generation failed:", error);
            setIsAnimating(false);
        }
    }

    function animateMazeGeneration(mazeGrid) {
        const wallGrid = new Uint8Array(cellState.length).fill(1);
        wallGrid[start] = 0;
        wallGrid[end] = 0;
        setCellState(wallGrid);

        const rowSize = Columns;
        const numRows = Math.floor(cellState.length / rowSize);
        const animationState = new Uint8Array(wallGrid);
        const finalMaze = new Uint8Array(mazeGrid);

        for (let row = 0; row < numRows; row++) {
            setTimeout(() => {
                for (let col = 0; col < rowSize; col++) {
                    const idx = row * rowSize + col;
                    animationState[idx] = finalMaze[idx];
                }
                setCellState(new Uint8Array(animationState));

                if (row === numRows - 1) {
                    setTimeout(() => {
                        setCellState(finalMaze);
                        setisPlayed(false);
                        setIsAnimating(false);
                    }, Constants.mazeGenerationTimeOut);
                }
            }, row * Constants.mazeGenerationTimeOut);
        }
    }

    const [algo, setAlgo] = useState(0);

    useEffect(() => {
        let algoName = ["Dijkstra", "A Star", "DFS", "BFS", "Greedy BFS", "Bellman Ford", "Bi Swarm"];
        let index = algo % algoName.length;
        setAlgoName(algoName[index]);
        if (initialized) {
            resetNonWallNodes();
            setisPlayed(false);
        }
    }, [algo]);

    function GetComplexity() {
        let complexity = ["O((V+E)logV)", "O(E)", "O(V+E)", "O(V+E)", "O(E)", "O(VE)", "O(VlogV)"];
        return complexity[algo % complexity.length];
    }

    async function playAlgo() {
        setPickerActive(false);
        resetNonWallNodes();
        setisPlayed(true);
        
        const algoEndpoints = [
            algorithmEndpoints.dijkstra,
            algorithmEndpoints.astar,
            algorithmEndpoints.dfs,
            algorithmEndpoints.bfs,
            algorithmEndpoints.greedyBfs,
            algorithmEndpoints.bellmanFord,
            algorithmEndpoints.biSwarm
        ];

        if (algo >= 0 && algo < algoEndpoints.length) {
            await handlePathfinding(algoEndpoints[algo]);
        }
    }

    async function handlePathfinding(endpoint) {
        setIsAnimating(true);
        try {
            const result = await runAlgorithm(
                endpoint,
                cellState,
                start,
                end,
                Rows,
                Columns
            );

            const { visited_order, path_indexes } = result;
            setVisitedNodes(visited_order.length);
            
            // Calculate non-wall nodes
            let nonWalls = 0;
            for (let i = 0; i < cellState.length; i++) {
                if (cellState[i] !== 1) nonWalls++;
            }
            setTotalNonWallNodes(nonWalls);

            const currentCellState = new Uint8Array(cellState);
            animatePath(currentCellState, visited_order, path_indexes);
        } catch (error) {
            console.error("Pathfinding failed:", error);
            setIsAnimating(false);
        }
    }

    function animatePath(initialCellState, visitedNodes, pathNodes) {
        let currentCellState = new Uint8Array(initialCellState);
        let previousNodeIdx = null;
        let currentSpeedVisited = Constants.visitedAnimationTimeOut + speedModifier;
        let currentSpeedShortest = Constants.pathAnimationTimeOut + speedModifier;

        // Animate visited nodes first
        for (let i = 0; i < visitedNodes.length; i++) {
            setTimeout(() => {
                const animationState = new Uint8Array(currentCellState);
                const idx = visitedNodes[i];

                if (previousNodeIdx !== null) {
                    animationState[previousNodeIdx] = 2;
                }
                animationState[idx] = 4;
                previousNodeIdx = idx;
                currentCellState = animationState;
                setCellState(animationState);
            }, i * currentSpeedVisited);
        }

        if (visitedNodes.length > 0) {
            setTimeout(() => {
                const lastIdx = visitedNodes[visitedNodes.length - 1];
                const animationState = new Uint8Array(currentCellState);
                animationState[lastIdx] = 2;
                currentCellState = animationState;
                setCellState(animationState);
            }, visitedNodes.length * currentSpeedVisited);
        }

        // Then animate shortest path nodes
        let previousPathIdx = null;
        for (let i = 0; i < pathNodes.length; i++) {
            setTimeout(() => {
                const animationState = new Uint8Array(currentCellState);
                const idx = pathNodes[i];
                if (previousPathIdx !== null) {
                    animationState[previousPathIdx] = 3;
                }
                animationState[idx] = 4;
                previousPathIdx = idx;
                currentCellState = animationState;
                setCellState(animationState);
            }, (visitedNodes.length * currentSpeedVisited) + (i * currentSpeedShortest));
        }

        if (pathNodes.length > 0) {
            setTimeout(() => {
                const lastIdx = pathNodes[pathNodes.length - 1];
                const animationState = new Uint8Array(currentCellState);
                animationState[lastIdx] = 3;
                setCellState(animationState);
                setIsAnimating(false);
            }, (visitedNodes.length * currentSpeedVisited) + (pathNodes.length * currentSpeedShortest));
        } else {
            setTimeout(() => {
                setIsAnimating(false);
            }, visitedNodes.length * currentSpeedVisited + 100);
        }
    }

    useEffect(() => {
        if (initialized) {
            renderGrid();
        }
    }, [initialized, cellState, start, end, mouseDown, dragMode]);

    useEffect(() => {
        if (initialized && isPlayed) {
            // Re-run algorithm when start/end changes
            playAlgo();
        }
    }, [start, end]);

    function resetNonWallNodes() {
        if (!cellState) return;
        const newState = new Uint8Array(cellState);
        for (let i = 0; i < newState.length; i++) {
            if (newState[i] !== 1) {
                newState[i] = 0;
            }
        }
        setCellState(newState);
    }

    function clearGrid() {
        if (!cellState) return;
        const newState = new Uint8Array(cellState.length);
        setCellState(newState);
        setisPlayed(false);
    }

    const renderGrid = () => {
        let cells = [];

        for (let i = 0; i < Rows; i++) {
            for (let j = 0; j < Columns; j++) {
                const currentCellIdx = Columns * i + j;
                let cell = (
                    <Node
                        key={currentCellIdx.toString()}
                        idx={currentCellIdx}
                        setWall={setWall}
                        stateValue={cellState ? cellState[currentCellIdx] : 0}
                        isStart={currentCellIdx === start}
                        isEnd={currentCellIdx === end}
                        mouseIsPressed={mouseDown}
                        onMouseDown={setMouseDown}
                        dragMode={dragMode}
                        setDragMode={setDragMode}
                        handleNodeDrag={handleNodeDrag}
                    />
                );
                cells.push(cell);
            }
        }
        setCellsArray(cells);
    };

    function refreshCells() {
        renderGrid();
    }

    function getVisitedPercentage() {
        if (totalNonWallNodes === 0) return 0;
        return (visitedNodes / totalNonWallNodes) * 100;
    }

    return (
        <>
            <StyledDiv>
                <div className="NavContainer">
                    <Nav
                        handlePlay={playAlgo}
                        AlgoName={AlgoName}
                        EnablePicker={setPickerActive}
                        toggleSpeed={toggleSpeed}
                        speed={getSpeedName}
                        maze={mazify}
                        refresh={() => {
                            clearGrid();
                            refreshCells();
                        }}
                        setisPlayed={setisPlayed}
                    />
                </div>
                {pickerActive ? (
                    <div className="algoPicker">
                        <AlgoPicker changeFlag={setAlgo} Enable={setPickerActive} />
                    </div>
                ) : null}
                {isPlayed && !isAnimating ? (
                    <div className="Benchmark">
                        <Benchmark
                            AlgoName={AlgoName}
                            visited={visitedNodes}
                            percentage={getVisitedPercentage()}
                            complexity={GetComplexity()}
                        />
                    </div>
                ) : null}
                <div className="gridContainer">
                    {!initialized ? (
                        <div className="Loading">
                            <Loading />
                        </div>
                    ) : (
                        cellsArray
                    )}
                </div>
                {isAnimating && (
                    <div
                        style={{
                            position: 'fixed',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            zIndex: 9999,
                            cursor: 'not-allowed'
                        }}
                        onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                        }}
                    />
                )}
            </StyledDiv>
        </>
    );
}

const StyledDiv = styled.div`
    .NavContainer {
        display: flex;
        position: absolute;
        left: 35%;
        width: auto;
        height: 5vh;
        justify-content: center;
        align-items: center;
        z-index: 99;
        opacity: 0.4;
        transition: 0.2s ease-out;
    }
    .NavContainer:hover {
        transition: 0.2s ease-in;
        opacity: 1;
    }
    .algoPicker {
        display: flex;
        position: absolute;
        right: 0;
        bottom: 15%;
        width: auto;
        height: 5vh;
        justify-content: center;
        align-items: center;
        z-index: 99;
        opacity: 0.7;
        transition: 0.2s ease-out;
    }
    .algoPicker:hover {
        transition: 0.2s ease-in;
        opacity: 1;
    }
    .Benchmark {
        display: flex;
        position: absolute;
        right: 0;
        top: 2%;
        width: auto;
        height: 5vh;
        justify-content: center;
        align-items: center;
        z-index: 99;
        opacity: 0.8;
        transition: 0.2s ease-out;
    }
    .Benchmark:hover {
        transition: 0.2s ease-in;
        opacity: 1;
    }
    .gridContainer {
        background-color: ${Constants.BackgroundColor};
        display: grid;
        grid-template-columns: repeat(${Columns}, 3fr);
        gap: 0;
        width: 100%;
        border: 1px solid black;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        overflow: hidden;
    }
    .Loading {
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
`;