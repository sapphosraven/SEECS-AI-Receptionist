import React, { useEffect, useState, useRef} from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { useGLTF } from "@react-three/drei";

const corresponding = {
  A: "viseme_PP",
  B: "viseme_kk",
  C: "viseme_I",
  D: "viseme_AA",
  E: "viseme_O",
  F: "viseme_U",
  G: "viseme_FF",
  H: "viseme_TH",
  X: "viseme_PP",
};

export function Avatar(props) {
  const group = useRef();
  const [audio, setAudio] = useState(null);
  const [lipsync, setLipsync] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isReady, setIsReady] = useState(false); // Track if both audio and lipsync data are ready
  const [lastReceivedFile, setLastReceivedFile] = useState(null); // Track the last received file
  const { nodes, materials } = useGLTF("/models/673fb6204788fd52690ac86e.glb");

  // WebSocket setup to listen for new files
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:5000");

    socket.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data);

      // Check if the audio or lipsync data has changed
      if (data.audioFile && data.jsonData && data.audioFile !== lastReceivedFile) {
        // If the new file is different from the last received file, process it
        setLastReceivedFile(data.audioFile);

        // Set audio
        const newAudio = new Audio(data.audioFile);
        setAudio(newAudio);

        // Set lipsync data
        setLipsync(data.jsonData);

        // Once both are set, mark as ready
        setIsReady(true);
      }
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    // Cleanup on component unmount
    return () => {
      socket.close();
    };
  }, [lastReceivedFile]); // Add `lastReceivedFile` to dependencies to re-run when it changes

// Handle audio playback and lip sync
useEffect(() => {
  console.log("is Ready " + isReady);
  console.log("is Playing " + isPlaying);
  if (isReady && !isPlaying && audio) {
    // Check if the new audio file is different from the previous one
    if (audio.src !== lastReceivedFile) {
      setIsPlaying(true);
      audio.play().catch((err) => console.error("Error playing audio:", err));
      audio.onended = () => setIsPlaying(false); // Reset the state after audio ends

      // Update the last received file to the current one
      setLastReceivedFile(audio.src);
    }
  }
}, [isReady, audio, isPlaying, lastReceivedFile]); // Add `lastReceivedFile` to dependencies to ensure it's updated correctly


  // Frame updates for lip-syncing
  useFrame(() => {
    if (!audio || !lipsync || !isPlaying) return;

    const currentAudioTime = audio.currentTime;

    // Reset morph targets for the head node
    const headNode = nodes.Wolf3D_Head;
    if (headNode?.morphTargetInfluences) {
      Object.values(corresponding).forEach((key) => {
        const index = headNode.morphTargetDictionary[key];
        if (index !== undefined) {
          headNode.morphTargetInfluences[index] = THREE.MathUtils.lerp(
            headNode.morphTargetInfluences[index],
            0,
            0.5
          );
        }
      });

      // Apply active morph target based on audio time
      lipsync.mouthCues.forEach((cue) => {
        if (currentAudioTime >= cue.start && currentAudioTime <= cue.end) {
          const index = headNode.morphTargetDictionary[corresponding[cue.value]];
          if (index !== undefined) {
            headNode.morphTargetInfluences[index] = 1;
          }
        }
      });
    }
  });

  return (
    <group {...props} dispose={null} ref={group}>
      <primitive object={nodes.Hips} />
      {Object.entries(nodes).map(([name, node]) => {
        if (node.isSkinnedMesh) {
          return (
            <skinnedMesh
              key={name}
              name={name}
              geometry={node.geometry}
              material={materials[node.material.name]}
              skeleton={node.skeleton}
              morphTargetDictionary={node.morphTargetDictionary}
              morphTargetInfluences={node.morphTargetInfluences}
            />
          );
        }
        return null;
      })}
    </group>
  );
}

useGLTF.preload("/models/673fb6204788fd52690ac86e.glb");
