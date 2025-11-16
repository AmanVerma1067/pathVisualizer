# 🧭 Path Visualizer

**Path Visualizer** is a web-based tool for visualizing classic pathfinding algorithms. Built with a high-performance **Python/FastAPI** backend and responsive **React** frontend.

🔗 **Live Demo**: [path-visualizer.vercel.app](https://path-visualizer.vercel.app)

---

## ✨ Features

- 🔳 **Interactive Grid Editor**  
  Draw walls, set start/end nodes, and reset with ease.

- 🧠 **Algorithm Visualizations**  
  Watch these algorithms solve the grid in real time:
  - Dijkstra's Algorithm
  - A* Search
  - Greedy Best-First Search
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Bellman-Ford Algorithm
  - Bidirectional Swarm (BiSwarm)

- ⚡ **Python Backend with FastAPI**  
  High-performance REST API handling all pathfinding computations.

- 🖥️ **Modern Frontend with React + Vite**  
  Fast and responsive UI with smooth animations.

---

## 🛠️ Getting Started

### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js + npm](https://nodejs.org/)

---

### Installation
```bash
# 1. Clone the repo
git clone https://github.com/Priyansh6747/Path-Visualizer.git
cd Path-Visualizer

# 2. Set up the backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Set up the frontend
cd ../frontend
npm install

# 4. Run the application
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🏗️ Architecture

### Backend (Python + FastAPI)
- **FastAPI** REST API
- **NumPy** for efficient grid operations
- Separate algorithm modules for maintainability
- Async endpoints for better performance

### Frontend (React + Vite)
- **React 19** for UI components
- **Styled Components** for styling
- **Vite** for fast development and builds
- State management with React hooks

---

## 🤝 Contributing

Contributions are welcome! Whether it's improving the UI, optimizing algorithms, adding new features, or fixing bugs.

### How to Contribute
```bash
# 1. Fork the repo
# 2. Create a feature branch
git checkout -b your-feature-name

# 3. Commit and push your changes
git commit -m "Add: feature description"
git push origin your-feature-name

# 4. Open a pull request (PR)
```

---

## 📁 Project Structure
```
Path-Visualizer/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── algorithms/          # Algorithm implementations
│   ├── maze.py             # Maze generation
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── PathVisilizer/  # Main visualizer component
│   │   ├── services/       # API service layer
│   │   └── App.jsx
│   └── package.json
└── README.md
```

---

## 🚀 Deployment

### Backend Deployment (Railway/Render/Heroku)
```bash
cd backend
# Add Procfile: web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend Deployment (Vercel/Netlify)
```bash
cd frontend
npm run build
# Deploy the dist/ folder
```

---

## 📝 License

This project is licensed under the MIT License.