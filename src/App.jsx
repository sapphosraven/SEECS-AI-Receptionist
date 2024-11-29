import { Canvas } from "@react-three/fiber";
import { Experience } from "./components/Experience";
import ChatOverlay from "./components/ChatOverlay";
import "./styles/ChatOverlay.css";

function App() {
  return (
    <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
      {/* 3D Canvas */}
      <Canvas shadows camera={{ position: [0, 0, 8], fov: 42 }}>
        <color attach="background" args={["#ececec"]} />
        <Experience />
      </Canvas>

      {/* Chat Overlay */}
      <ChatOverlay />
    </div>
  );
}

export default App;
