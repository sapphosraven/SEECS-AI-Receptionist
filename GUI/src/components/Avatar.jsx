import { useAnimations, useFBX, useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import React, { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";

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
  const [audio, setAudio] = useState(null);
  const [jsonFile, setJsonFile] = useState(null);
  const [lipsync, setLipsync] = useState(null);
  const [animation, setAnimation] = useState("Idle");

  const { nodes, materials } = useGLTF("/models/673fb6204788fd52690ac86e.glb");
  const { animations: idleAnimation } = useFBX("/animations/Idle.fbx");

  const group = useRef();
  const { actions } = useAnimations([idleAnimation[0]], group);

  idleAnimation[0].name = "Idle";

  useEffect(() => {
    actions[animation]?.reset().fadeIn(0.5).play();
    return () => actions[animation]?.fadeOut(0.5);
  }, [animation]);

  // Function to fetch the latest file
  const fetchLatestFile = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/latest-file");
      const { wavFile, jsonFile } = response.data;
      setAudio(new Audio(`/audios/${wavFile}`));
      const jsonContent = await axios.get(`/audios/${jsonFile}`);
      setJsonFile(jsonFile);
      setLipsync(jsonContent.data);
      setAnimation("Idle");
    } catch (error) {
      console.error("Error fetching latest file:", error);
    }
  };

  useEffect(() => {
    // Polling to check for new files every 0.1 seconds
    const interval = setInterval(fetchLatestFile, 100);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!audio || !lipsync) return;

    const handleAudioEnd = () => {
      setAnimation("Idle");
      fetchLatestFile(); // Check for new files after playback ends
    };

    audio.play();
    audio.addEventListener("ended", handleAudioEnd);

    return () => audio.removeEventListener("ended", handleAudioEnd);
  }, [audio, lipsync]);

  useFrame(() => {
    if (!audio || !lipsync) return;

    const currentAudioTime = audio.currentTime;
    Object.values(corresponding).forEach((value) => {
      nodes.Wolf3D_Head.morphTargetInfluences[
        nodes.Wolf3D_Head.morphTargetDictionary[value]
      ] = 0;
    });

    for (let i = 0; i < lipsync.mouthCues.length; i++) {
      const mouthCue = lipsync.mouthCues[i];
      if (
        currentAudioTime >= mouthCue.start &&
        currentAudioTime <= mouthCue.end
      ) {
        nodes.Wolf3D_Head.morphTargetInfluences[
          nodes.Wolf3D_Head.morphTargetDictionary[corresponding[mouthCue.value]]
        ] = 1;
        break;
      }
    }
  });

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
    );
  }

  useGLTF.preload(
    "https://models.readyplayer.me/65a8dba831b23abb4f401bae.glb?lod=2&textureAtlas=none"
  );
