import React, { useEffect, useState, useRef, useContext } from "react";
import { useFrame } from "@react-three/fiber";
import { useGLTF, useFBX, useAnimations } from "@react-three/drei";
import * as THREE from "three";
import { AnimationContext } from "../App"; // Import the context

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
  const { isThinking, setIsThinking } = useContext(AnimationContext); // Access the context

  const { nodes, materials } = useGLTF("/models/673fb6204788fd52690ac86e.glb");
  const [audio, setAudio] = useState(null);
  const [lipsync, setLipsync] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const [lastReceivedFile, setLastReceivedFile] = useState(null);

  // Load animations (Idle, Think, ThinkStart, ThinkEnd)
  const { animations: idleAnimation } = useFBX("/animations/Idle.fbx");
  const { animations: thinkAnimation } = useFBX("/animations/Think.fbx");
  const { animations: thinkStart } = useFBX("/animations/Think-Start.fbx");
  const { animations: thinkEnd } = useFBX("/animations/Think-End.fbx");

  idleAnimation[0].name = "Idle";
  thinkAnimation[0].name = "Think";
  thinkStart[0].name = "ThinkStart";
  thinkEnd[0].name = "ThinkEnd";

  const [animation, setAnimation] = useState("Idle");
  const { actions } = useAnimations(
    [idleAnimation[0], thinkAnimation[0], thinkStart[0], thinkEnd[0]],
    group
  );


  useEffect(() => {
    actions[animation].reset().fadeIn(0.5).play();
    return () => actions[animation].fadeOut(0.5);
  }, [animation]);

  
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
  }, [lastReceivedFile]);

  // Handle audio playback and lip sync
  useEffect(() => {
    if (isReady && !isPlaying && audio) {
      if (audio.src !== lastReceivedFile) {
        setIsPlaying(true);
        audio.play().catch((err) => console.error("Error playing audio:", err));
        audio.onended = () => setIsPlaying(false);
        setLastReceivedFile(audio.src);
      }
    }
  }, [isReady, audio, isPlaying, lastReceivedFile]);

  // Update animation based on thinking state
  useEffect(() => {
    if (isThinking) {
      setAnimation("ThinkStart"); // Transition to ThinkStart
      setTimeout(() => setAnimation("Think"), 1000); // Stay in Think animation
    } else {
      setAnimation("ThinkEnd");
      setTimeout(() => setAnimation("Idle"), 1000); // Transition back to Idle
    }
  }, [isThinking]);

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

  // Render the avatar
  return (
    <group {...props} dispose={null} ref={group}>
      <primitive object={nodes.Hips} />
      <skinnedMesh
        geometry={nodes.Wolf3D_Body.geometry}
        material={materials.Wolf3D_Body}
        skeleton={nodes.Wolf3D_Body.skeleton}
      />
      <skinnedMesh
        geometry={nodes.Wolf3D_Outfit_Bottom.geometry}
        material={materials.Wolf3D_Outfit_Bottom}
        skeleton={nodes.Wolf3D_Outfit_Bottom.skeleton}
      />
      <skinnedMesh
        geometry={nodes.Wolf3D_Outfit_Footwear.geometry}
        material={materials.Wolf3D_Outfit_Footwear}
        skeleton={nodes.Wolf3D_Outfit_Footwear.skeleton}
      />
      <skinnedMesh
        geometry={nodes.Wolf3D_Outfit_Top.geometry}
        material={materials.Wolf3D_Outfit_Top}
        skeleton={nodes.Wolf3D_Outfit_Top.skeleton}
      />
      <skinnedMesh
        name="EyeLeft"
        geometry={nodes.EyeLeft.geometry}
        material={materials.Wolf3D_Eye}
        skeleton={nodes.EyeLeft.skeleton}
        morphTargetDictionary={nodes.EyeLeft.morphTargetDictionary}
        morphTargetInfluences={nodes.EyeLeft.morphTargetInfluences}
      />
      <skinnedMesh
        name="EyeRight"
        geometry={nodes.EyeRight.geometry}
        material={materials.Wolf3D_Eye}
        skeleton={nodes.EyeRight.skeleton}
        morphTargetDictionary={nodes.EyeRight.morphTargetDictionary}
        morphTargetInfluences={nodes.EyeRight.morphTargetInfluences}
      />
      <skinnedMesh
        name="Wolf3D_Head"
        geometry={nodes.Wolf3D_Head.geometry}
        material={materials.Wolf3D_Skin}
        skeleton={nodes.Wolf3D_Head.skeleton}
        morphTargetDictionary={nodes.Wolf3D_Head.morphTargetDictionary}
        morphTargetInfluences={nodes.Wolf3D_Head.morphTargetInfluences}
      />
      <skinnedMesh
        name="Wolf3D_Hair"
        geometry={nodes.Wolf3D_Hair.geometry}
        material={materials.Wolf3D_Hair}
        skeleton={nodes.Wolf3D_Hair.skeleton}
        morphTargetDictionary={nodes.Wolf3D_Hair.morphTargetDictionary}
        morphTargetInfluences={nodes.Wolf3D_Hair.morphTargetInfluences}
      />
      <skinnedMesh
        name="Wolf3D_Teeth"
        geometry={nodes.Wolf3D_Teeth.geometry}
        material={materials.Wolf3D_Teeth}
        skeleton={nodes.Wolf3D_Teeth.skeleton}
        morphTargetDictionary={nodes.Wolf3D_Teeth.morphTargetDictionary}
        morphTargetInfluences={nodes.Wolf3D_Teeth.morphTargetInfluences}
      />
    </group>
    )
}

useGLTF.preload("/models/673fb6204788fd52690ac86e.glb");
