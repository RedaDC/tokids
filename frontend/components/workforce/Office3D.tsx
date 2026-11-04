'use client';

import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Float, Stars } from '@react-three/drei';
import * as THREE from 'three';
import { Agent, AgentRole } from '@/lib/types';

interface Office3DProps {
  agents: Agent[];
  onSelectAgent: (agent: Agent) => void;
}

// -------------------------------------------------------------
// Procedural 3D Mesh Component per Agent Role
// -------------------------------------------------------------
const AgentMesh: React.FC<{
  role: AgentRole;
  isWorking: boolean;
  status: string;
}> = ({ role, isWorking, status }) => {
  const meshRef = useRef<THREE.Group>(null);
  const ringRef = useRef<THREE.Mesh>(null);

  // Status color configuration
  const getColor = () => {
    if (status === 'working') return '#A855F7'; // Electric Purple
    if (status === 'completed') return '#10B981'; // Emerald
    if (status === 'failed') return '#F43F5E'; // Rose
    return '#38BDF8'; // Sky Blue / Idle
  };

  const mainColor = getColor();

  useFrame((state, delta) => {
    if (meshRef.current) {
      const speed = isWorking ? 2.5 : 0.8;
      meshRef.current.rotation.y += delta * speed;
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime * (isWorking ? 3 : 1.5)) * 0.15;
    }
    if (ringRef.current) {
      ringRef.current.rotation.x += delta * 2;
      ringRef.current.rotation.z += delta * 1.5;
    }
  });

  switch (role) {
    case 'ceo':
      return (
        <group ref={meshRef}>
          {/* Golden sphere */}
          <mesh castShadow>
            <sphereGeometry args={[0.5, 32, 32]} />
            <meshStandardMaterial
              color="#F59E0B"
              metalness={0.9}
              roughness={0.2}
              emissive="#D97706"
              emissiveIntensity={isWorking ? 0.8 : 0.2}
            />
          </mesh>
          {/* Orbiting ring */}
          <mesh ref={ringRef}>
            <torusGeometry args={[0.8, 0.04, 16, 64]} />
            <meshStandardMaterial color="#FBBF24" emissive="#F59E0B" emissiveIntensity={0.6} />
          </mesh>
        </group>
      );

    case 'creative':
      return (
        <group ref={meshRef}>
          {/* Color-shifting crystal */}
          <mesh castShadow>
            <octahedronGeometry args={[0.55, 0]} />
            <meshStandardMaterial
              color={mainColor}
              roughness={0.1}
              metalness={0.7}
              emissive={mainColor}
              emissiveIntensity={isWorking ? 0.9 : 0.3}
              wireframe={false}
            />
          </mesh>
        </group>
      );

    case 'generator':
      return (
        <group ref={meshRef}>
          {/* Spinning cog / gear */}
          <mesh castShadow>
            <torusGeometry args={[0.45, 0.15, 16, 32]} />
            <meshStandardMaterial
              color={mainColor}
              metalness={0.8}
              roughness={0.3}
              emissive={mainColor}
              emissiveIntensity={isWorking ? 0.8 : 0.2}
            />
          </mesh>
          {[0, 60, 120, 180, 240, 300].map((deg) => (
            <mesh
              key={deg}
              rotation={[0, 0, (deg * Math.PI) / 180]}
              position={[Math.cos((deg * Math.PI) / 180) * 0.45, Math.sin((deg * Math.PI) / 180) * 0.45, 0]}
            >
              <boxGeometry args={[0.15, 0.15, 0.2]} />
              <meshStandardMaterial color={mainColor} />
            </mesh>
          ))}
        </group>
      );

    case 'quality':
      return (
        <group ref={meshRef}>
          {/* Shield mesh */}
          <mesh castShadow rotation={[0, 0, 0]}>
            <coneGeometry args={[0.5, 0.7, 4]} />
            <meshStandardMaterial
              color={mainColor}
              metalness={0.8}
              roughness={0.2}
              emissive={mainColor}
              emissiveIntensity={isWorking ? 0.8 : 0.2}
            />
          </mesh>
        </group>
      );

    case 'compliance':
      return (
        <group ref={meshRef}>
          {/* Lock body & shackle */}
          <mesh castShadow position={[0, -0.15, 0]}>
            <boxGeometry args={[0.5, 0.4, 0.25]} />
            <meshStandardMaterial
              color={mainColor}
              metalness={0.8}
              roughness={0.3}
              emissive={mainColor}
              emissiveIntensity={isWorking ? 0.7 : 0.2}
            />
          </mesh>
          <mesh position={[0, 0.2, 0]}>
            <torusGeometry args={[0.2, 0.05, 16, 32, Math.PI]} />
            <meshStandardMaterial color="#94A3B8" metalness={0.9} roughness={0.1} />
          </mesh>
        </group>
      );

    case 'seo':
      return (
        <group ref={meshRef}>
          {/* Magnifying glass */}
          <mesh castShadow>
            <torusGeometry args={[0.35, 0.06, 16, 32]} />
            <meshStandardMaterial
              color={mainColor}
              metalness={0.8}
              roughness={0.2}
              emissive={mainColor}
              emissiveIntensity={isWorking ? 0.8 : 0.2}
            />
          </mesh>
          <mesh position={[0.3, -0.3, 0]} rotation={[0, 0, -Math.PI / 4]}>
            <cylinderGeometry args={[0.05, 0.05, 0.4, 16]} />
            <meshStandardMaterial color="#475569" />
          </mesh>
        </group>
      );

    case 'research':
      return (
        <group ref={meshRef}>
          {/* Rotating document / book */}
          <mesh castShadow>
            <boxGeometry args={[0.55, 0.7, 0.1]} />
            <meshStandardMaterial
              color={mainColor}
              roughness={0.4}
              emissive={mainColor}
              emissiveIntensity={isWorking ? 0.7 : 0.2}
            />
          </mesh>
        </group>
      );

    case 'portfolio':
      return (
        <group ref={meshRef}>
          {/* Catalog folder */}
          <mesh castShadow>
            <boxGeometry args={[0.6, 0.45, 0.15]} />
            <meshStandardMaterial
              color={mainColor}
              metalness={0.5}
              roughness={0.3}
              emissive={mainColor}
              emissiveIntensity={isWorking ? 0.7 : 0.2}
            />
          </mesh>
        </group>
      );

    case 'analytics':
    default:
      return (
        <group ref={meshRef}>
          {/* Bar chart bars */}
          <mesh position={[-0.2, -0.1, 0]}>
            <boxGeometry args={[0.12, 0.3, 0.12]} />
            <meshStandardMaterial color={mainColor} emissive={mainColor} emissiveIntensity={0.4} />
          </mesh>
          <mesh position={[0, 0.05, 0]}>
            <boxGeometry args={[0.12, 0.6, 0.12]} />
            <meshStandardMaterial color={mainColor} emissive={mainColor} emissiveIntensity={0.6} />
          </mesh>
          <mesh position={[0.2, 0.2, 0]}>
            <boxGeometry args={[0.12, 0.9, 0.12]} />
            <meshStandardMaterial color={mainColor} emissive={mainColor} emissiveIntensity={0.8} />
          </mesh>
        </group>
      );
  }
};

// -------------------------------------------------------------
// Workstation Pod with Floor Base & Hologram Monitor Screen
// -------------------------------------------------------------
const StationPod: React.FC<{
  agent: Agent;
  position: [number, number, number];
  onClick: () => void;
}> = ({ agent, position, onClick }) => {
  const [hovered, setHovered] = useState(false);
  const isWorking = agent.status === 'working';

  return (
    <group position={position}>
      {/* Pod Base Platform */}
      <mesh position={[0, -0.4, 0]} receiveShadow>
        <cylinderGeometry args={[1.2, 1.4, 0.2, 32]} />
        <meshStandardMaterial
          color={hovered ? '#1E1B4B' : '#0B1120'}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>

      {/* Pod Neon Edge Ring */}
      <mesh position={[0, -0.29, 0]}>
        <ringGeometry args={[1.15, 1.25, 32]} />
        <meshBasicMaterial
          color={isWorking ? '#7C3AED' : hovered ? '#38BDF8' : '#1E293B'}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* 3D Floating Avatar */}
      <Float speed={2} rotationIntensity={0.4} floatIntensity={0.3}>
        <group
          position={[0, 0.6, 0]}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
          onClick={(e) => {
            e.stopPropagation();
            onClick();
          }}
        >
          <AgentMesh role={agent.role} isWorking={isWorking} status={agent.status} />
        </group>
      </Float>

      {/* Holographic Monitor Screen Above Pod */}
      <group position={[0, 1.8, 0]}>
        {/* Screen Background Panel */}
        <mesh>
          <planeGeometry args={[1.6, 0.65]} />
          <meshStandardMaterial
            color="#050810"
            transparent
            opacity={0.85}
            roughness={0.2}
          />
        </mesh>
        {/* Screen Frame Glow */}
        <lineSegments>
          <edgesGeometry args={[new THREE.PlaneGeometry(1.6, 0.65)]} />
          <lineBasicMaterial color={isWorking ? '#7C3AED' : '#3B82F6'} />
        </lineSegments>

        {/* Text Labels */}
        <Text
          position={[0, 0.14, 0.02]}
          fontSize={0.12}
          color="#FFFFFF"
          anchorX="center"
          anchorY="middle"
        >
          {`${agent.name} (${agent.displayName})`}
        </Text>
        <Text
          position={[0, -0.1, 0.02]}
          fontSize={0.08}
          color={isWorking ? '#C084FC' : '#94A3B8'}
          anchorX="center"
          anchorY="middle"
          maxWidth={1.4}
        >
          {agent.currentTask ? agent.currentTask.slice(0, 32) + '...' : 'Idle'}
        </Text>
      </group>

      {/* Local Spotlight */}
      <pointLight
        position={[0, 2.2, 0]}
        intensity={isWorking ? 1.5 : 0.6}
        color={isWorking ? '#9333EA' : '#38BDF8'}
        distance={4}
      />
    </group>
  );
};

// -------------------------------------------------------------
// Central Elevated Platform for CEO Agent
// -------------------------------------------------------------
const CentralDesk: React.FC = () => {
  return (
    <group position={[0, 0, 0]}>
      {/* Elevated Tier */}
      <mesh position={[0, -0.2, 0]} receiveShadow>
        <cylinderGeometry args={[2.2, 2.5, 0.4, 48]} />
        <meshStandardMaterial color="#0A0F1D" metalness={0.9} roughness={0.1} />
      </mesh>
      {/* Neon Concentric Rings */}
      <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.8, 1.9, 48]} />
        <meshBasicMaterial color="#7C3AED" side={THREE.DoubleSide} />
      </mesh>
      <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.2, 1.3, 48]} />
        <meshBasicMaterial color="#06B6D4" side={THREE.DoubleSide} />
      </mesh>
    </group>
  );
};

// -------------------------------------------------------------
// Main Office 3D Canvas
// -------------------------------------------------------------
export const Office3D: React.FC<Office3DProps> = ({ agents, onSelectAgent }) => {
  const [hasWebGL, setHasWebGL] = useState(true);

  useEffect(() => {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (!gl) setHasWebGL(false);
    } catch {
      setHasWebGL(false);
    }
  }, []);

  if (!hasWebGL) {
    return (
      <div className="flex h-[600px] w-full items-center justify-center rounded-2xl border border-white/5 bg-slate-950 p-8 text-center">
        <p className="text-slate-400">
          WebGL is not supported in this browser environment. Switched to 2D Workforce Matrix.
        </p>
      </div>
    );
  }

  // Separate CEO from other 8 circular pods
  const ceoAgent = agents.find((a) => a.role === 'ceo') || agents[0];
  const perimeterAgents = agents.filter((a) => a.id !== ceoAgent.id);

  // Compute circular layout for the other 8 agents
  const radius = 6.8;

  return (
    <div className="relative h-[650px] w-full overflow-hidden rounded-2xl border border-white/10 bg-[#040711] shadow-2xl">
      {/* Top Overlay Legend & Controls hint */}
      <div className="absolute top-4 left-4 z-10 pointer-events-none rounded-xl border border-white/10 bg-slate-950/70 p-3 backdrop-blur-md">
        <p className="text-xs font-semibold text-white">3D Autonomous Cyber Office</p>
        <p className="text-[11px] text-slate-400">
          Orbit: Left Click Drag • Pan: Right Click • Zoom: Scroll
        </p>
      </div>

      <Canvas
        camera={{ position: [0, 9, 14], fov: 45 }}
        gl={{ antialias: true, alpha: false }}
        style={{ background: '#040711' }}
      >
        <ambientLight intensity={0.4} />
        <directionalLight position={[10, 20, 10]} intensity={1.2} castShadow />

        {/* Space Star Field */}
        <Stars radius={100} depth={50} count={3000} factor={4} saturation={0.5} fade speed={1} />

        {/* Central Desk & CEO Station */}
        <CentralDesk />
        {ceoAgent && (
          <StationPod
            agent={ceoAgent}
            position={[0, 0.4, 0]}
            onClick={() => onSelectAgent(ceoAgent)}
          />
        )}

        {/* Circular Perimeter Pods */}
        {perimeterAgents.map((agent, index) => {
          const angle = (index / perimeterAgents.length) * Math.PI * 2;
          const x = Math.cos(angle) * radius;
          const z = Math.sin(angle) * radius;

          return (
            <StationPod
              key={agent.id}
              agent={agent}
              position={[x, 0, z]}
              onClick={() => onSelectAgent(agent)}
            />
          );
        })}

        {/* Grid Floor */}
        <gridHelper args={[30, 30, '#7C3AED', '#1E293B']} position={[0, -0.41, 0]} />

        {/* Orbit Controls with bounded angles */}
        <OrbitControls
          enableZoom={true}
          maxPolarAngle={Math.PI / 2.1}
          minDistance={5}
          maxDistance={25}
          dampingFactor={0.05}
        />
      </Canvas>
    </div>
  );
};

export default Office3D;
