import PathVisualizer from "./PathVisualizer/PathVisualizer.jsx";
function App() {
    function handlemouse(e){
        e.preventDefault();
    }
  return (
    <div onClick={handlemouse} onMouseDown={handlemouse}>
      <PathVisualizer  />
    </div>
  )
}

export default App
