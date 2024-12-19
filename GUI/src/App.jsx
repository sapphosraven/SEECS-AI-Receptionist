import { Canvas } from "@react-three/fiber";
import { Experience } from "./components/Experience";
import ChatOverlay from "./components/ChatOverlay";
import { Avatar } from "./components/Avatar";
import React, { createContext, useState } from "react";

// Create context for animation control
export const AnimationContext = createContext();

function App() {
  const [isThinking, setIsThinking] = useState(); // State to track thinking animation

  return (
    <AnimationContext.Provider value={{ isThinking, setIsThinking }}>
      <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
        {/* 3D Canvas */}
        <Canvas shadows camera={{ position: [0, 0, 8], fov: 42 }}>
          <color attach="background" args={["#ececec"]} />
          <Experience>
            <Avatar /> {/* Pass context to Avatar for animation control */}
          </Experience>
        </Canvas>

        {/* Chat Overlay */}
        <ChatOverlay />
      </div>
    </AnimationContext.Provider>
  );
}

export default App;
