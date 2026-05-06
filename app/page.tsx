"use client";

import React, { useRef, useState, useEffect, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Sphere } from "@react-three/drei";
import * as THREE from "three";
import { Settings2, Mic, MicOff, Activity, Play, Pause, Square, Volume2, Hand } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import * as handPoseDetection from '@tensorflow-models/hand-pose-detection';
import '@tensorflow/tfjs-backend-webgl';

// Hook to capture audio volume
const useAudioAnalyzer = () => {
  const [isListening, setIsListening] = useState(false);
  const analyzerRef = useRef<AnalyserNode | null>(null);
  const dataArrayRef = useRef<Uint8Array | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const AudioContextCtor = window.AudioContext || (window as any).webkitAudioContext;
      audioContextRef.current = new AudioContextCtor();
      
      analyzerRef.current = audioContextRef.current.createAnalyser();
      analyzerRef.current.fftSize = 256;
      analyzerRef.current.smoothingTimeConstant = 0.8;
      
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyzerRef.current);
      
      dataArrayRef.current = new Uint8Array(analyzerRef.current.frequencyBinCount);
      setIsListening(true);
    } catch (err) {
      console.error("Error accessing mic:", err);
      throw err;
    }
  };

  const stopListening = () => {
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
    }
    setIsListening(false);
  };

  const getVolume = () => {
    if (!analyzerRef.current || !dataArrayRef.current || !isListening) return 0;
    analyzerRef.current.getByteFrequencyData(dataArrayRef.current as any);
    
    let sum = 0;
    for (let i = 0; i < dataArrayRef.current.length; i++) {
      sum += dataArrayRef.current[i];
    }
    return sum / dataArrayRef.current.length; 
  };

  return { isListening, startListening, stopListening, getVolume };
};

// Space/Galaxy visualization -> Jarvis style network sphere
const JarvisOrb = ({ getVolume }: { getVolume: () => number }) => {
  const groupRef = useRef<THREE.Group>(null);
  
  const particleTexture = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const context = canvas.getContext('2d');
    if (context) {
      const gradient = context.createRadialGradient(32, 32, 0, 32, 32, 32);
      gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
      gradient.addColorStop(0.3, 'rgba(0, 190, 255, 0.8)'); // Deep cyan glow
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      context.fillStyle = gradient;
      context.fillRect(0, 0, 64, 64);
    }
    return new THREE.CanvasTexture(canvas);
  }, []);

  const [geometry] = useState(() => {
    const geo = new THREE.BufferGeometry();
    const particleCount = 20000;
    const positions = new Float32Array(particleCount * 3);
    const basePositions = new Float32Array(particleCount * 3);
    const noiseFactors = new Float32Array(particleCount);
    
    for (let i = 0; i < particleCount; i++) {
        const theta = Math.random() * 2.0 * Math.PI;
        const phi = Math.acos((Math.random() * 2.0) - 1.0);
        
        let x = Math.sin(phi) * Math.cos(theta);
        let y = Math.sin(phi) * Math.sin(theta);
        let z = Math.cos(phi);

        basePositions[i * 3] = x;
        basePositions[i * 3 + 1] = y; 
        basePositions[i * 3 + 2] = z;

        positions[i * 3] = x * 2;
        positions[i * 3 + 1] = y * 2;
        positions[i * 3 + 2] = z * 2;

        noiseFactors[i] = Math.sin(theta * 12) * Math.cos(phi * 10) + Math.sin(theta * 6 + phi * 6);
    }
    
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('basePosition', new THREE.BufferAttribute(basePositions, 3));
    geo.setAttribute('noiseFactor', new THREE.BufferAttribute(noiseFactors, 1));
    return geo;
  });

  const materialRef = useRef<THREE.PointsMaterial>(null);
  const meshRef = useRef<THREE.MeshBasicMaterial>(null);

  useFrame((state, delta) => {
    if (!groupRef.current) return;
    
    const rawVolume = getVolume();
    const volume = Math.min(rawVolume / 30, 2.5);

    const targetScale = 1 + volume * 0.05;
    groupRef.current.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.1);
    
    groupRef.current.rotation.y += delta * 0.05;
    groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.2) * 0.02;

    if (materialRef.current) {
      materialRef.current.size = 0.04 + (volume * 0.02);
      materialRef.current.opacity = 0.5 + (volume * 0.5);
    }
    if (meshRef.current) {
      meshRef.current.opacity = 0.1 + (volume * 0.1);
    }

    const positions = geometry.attributes.position.array as Float32Array;
    const basePositions = geometry.attributes.basePosition.array as Float32Array;
    const noiseFactors = geometry.attributes.noiseFactor.array as Float32Array;
    const t = state.clock.elapsedTime * 2;
    const smoothVol = volume * volume;

    for (let i = 0; i < 20000; i++) {
        const bx = basePositions[i * 3];
        const by = basePositions[i * 3 + 1];
        const bz = basePositions[i * 3 + 2];

        let distance = 2.0;

        if (smoothVol > 0.005) {
            const organicSpikes = noiseFactors[i] * 1.5;
            distance += organicSpikes * (smoothVol * 0.8);
            distance += (Math.random() - 0.5) * (smoothVol * 0.3);
            distance += Math.sin(t + bx * 3 + bz * 3) * (smoothVol * 0.2);
        }

        const targetX = bx * distance;
        const targetY = by * distance;
        const targetZ = bz * distance;

        positions[i * 3] += (targetX - positions[i * 3]) * 0.2;
        positions[i * 3 + 1] += (targetY - positions[i * 3 + 1]) * 0.2;
        positions[i * 3 + 2] += (targetZ - positions[i * 3 + 2]) * 0.2;
    }

    geometry.attributes.position.needsUpdate = true;
  });

  return (
    <group ref={groupRef}>
      <points geometry={geometry}>
        <pointsMaterial
          ref={materialRef}
          color="#a5f3fc"
          size={0.04}
          map={particleTexture}
          transparent={true}
          opacity={0.5}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          sizeAttenuation={true}
        />
      </points>
      
      <Sphere args={[1.7, 32, 32]}>
        <meshBasicMaterial
          ref={meshRef}
          color="#0284c7"
          wireframe={true}
          transparent={true}
          opacity={0.1}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </Sphere>
    </group>
  );
};

export default function App() {
  const { isListening: isMicActive, startListening: startMic, stopListening: stopMic, getVolume } = useAudioAnalyzer();
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [logs, setLogs] = useState<{type: string, text: string}[]>([]);
  const [flaskUrl, setFlaskUrl] = useState("http://localhost:8080");
  const [groqKey, setGroqKey] = useState("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");
  const [showSettings, setShowSettings] = useState(false);
  const [history, setHistory] = useState<{role: string, content: string}[]>([]);
  const [mounted, setMounted] = useState(false);
  const [musicPlaying, setMusicPlaying] = useState(false);
  const [musicVolume, setMusicVolume] = useState(0.05);
  const [handTrackingActive, setHandTrackingActive] = useState(false);
  const [currentTab, setCurrentTab] = useState(0);
  const [clickMode, setClickMode] = useState(false);
  const [dragMode, setDragMode] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const logEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const detectorRef = useRef<any>(null);
  const animationFrameRef = useRef<number | undefined>(undefined);
  const lastGestureTimeRef = useRef<number>(0);

  const tabs = ["Home", "Music", "Settings", "Logs", "System"];

  const addLog = (type: string, text: string) => {
    setLogs(prev => [...prev, {type, text}].slice(-50));
  };

  // Hand tracking functions
  const startHandTracking = async () => {
    try {
      const model = handPoseDetection.SupportedModels.MediaPipeHands;
      const detectorConfig = {
        runtime: 'tfjs' as const,
        modelType: 'lite' as const,
        maxHands: 1,
      };
      
      detectorRef.current = await handPoseDetection.createDetector(model, detectorConfig);
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        
        // Video yüklendiğinde hand detection başlat
        videoRef.current.onloadedmetadata = () => {
          console.log("Video metadata loaded:", videoRef.current?.videoWidth, videoRef.current?.videoHeight);
          videoRef.current?.play().then(() => {
            console.log("Video playing");
            setHandTrackingActive(true);
            addLog("system", "🖐️ Hand tracking activated!");
            detectHands();
          }).catch(err => {
            console.error("Video play error:", err);
            addLog("error", "Video play failed");
          });
        };
      }
    } catch (err) {
      console.error("Hand tracking error:", err);
      addLog("error", "Hand tracking failed");
    }
  };

  const stopHandTracking = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    setHandTrackingActive(false);
    addLog("system", "Hand tracking stopped");
  };

  const calculateDistance = (point1: any, point2: any) => {
    const dx = point1.x - point2.x;
    const dy = point1.y - point2.y;
    return Math.sqrt(dx * dx + dy * dy);
  };

  const detectHands = async () => {
    if (!detectorRef.current || !videoRef.current || !canvasRef.current) return;
    
    // Video hazır değilse bekle
    if (videoRef.current.readyState !== 4) {
      animationFrameRef.current = requestAnimationFrame(detectHands);
      return;
    }
    
    // Video boyutu 0 ise bekle
    if (videoRef.current.videoWidth === 0 || videoRef.current.videoHeight === 0) {
      animationFrameRef.current = requestAnimationFrame(detectHands);
      return;
    }

    const hands = await detectorRef.current.estimateHands(videoRef.current);
    const ctx = canvasRef.current.getContext('2d');
    
    if (ctx && canvasRef.current) {
      // Canvas'ı temizle
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      
      // Canvas boyutlarını ayarla
      const videoWidth = videoRef.current.videoWidth || 640;
      const videoHeight = videoRef.current.videoHeight || 480;
      const scaleX = canvasRef.current.width / videoWidth;
      const scaleY = canvasRef.current.height / videoHeight;
      
      if (hands.length > 0) {
        const hand = hands[0];
        const keypoints = hand.keypoints;
        
        // Tüm el iskeletini çiz
        const connections = [
          [0, 1], [1, 2], [2, 3], [3, 4],
          [0, 5], [5, 6], [6, 7], [7, 8],
          [0, 9], [9, 10], [10, 11], [11, 12],
          [0, 13], [13, 14], [14, 15], [15, 16],
          [0, 17], [17, 18], [18, 19], [19, 20],
          [5, 9], [9, 13], [13, 17]
        ];
        
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.lineWidth = 2;
        connections.forEach(([start, end]) => {
          const startPoint = keypoints[start];
          const endPoint = keypoints[end];
          ctx.beginPath();
          ctx.moveTo(startPoint.x * scaleX, startPoint.y * scaleY);
          ctx.lineTo(endPoint.x * scaleX, endPoint.y * scaleY);
          ctx.stroke();
        });
        
        // Tüm noktaları çiz
        keypoints.forEach((point: any) => {
          ctx.fillStyle = 'rgba(255, 100, 100, 0.8)';
          ctx.beginPath();
          ctx.arc(point.x * scaleX, point.y * scaleY, 4, 0, 2 * Math.PI);
          ctx.fill();
        });
        
        // Parmak uçları
        const thumb = keypoints[4];      // Baş parmak
        const indexFinger = keypoints[8]; // İşaret parmağı
        const ringFinger = keypoints[16]; // Yüzük parmağı
        
        const thumbX = thumb.x * scaleX;
        const thumbY = thumb.y * scaleY;
        const indexX = indexFinger.x * scaleX;
        const indexY = indexFinger.y * scaleY;
        const ringX = ringFinger.x * scaleX;
        const ringY = ringFinger.y * scaleY;
        
        // Mesafeleri hesapla
        const distanceIndex = calculateDistance({x: thumbX, y: thumbY}, {x: indexX, y: indexY});
        const distanceRing = calculateDistance({x: thumbX, y: thumbY}, {x: ringX, y: ringY});
        
        // Baş parmak - Cyan
        ctx.fillStyle = '#00bfff';
        ctx.beginPath();
        ctx.arc(thumbX, thumbY, 12, 0, 2 * Math.PI);
        ctx.fill();
        ctx.strokeStyle = '#00bfff';
        ctx.lineWidth = 3;
        ctx.stroke();
        ctx.fillStyle = '#00bfff';
        ctx.font = 'bold 10px Arial';
        ctx.fillText('THUMB', thumbX - 20, thumbY - 15);
        
        // İşaret parmağı - Yeşil
        ctx.fillStyle = distanceIndex < 30 ? '#00ff00' : '#00ff00';
        ctx.beginPath();
        ctx.arc(indexX, indexY, 12, 0, 2 * Math.PI);
        ctx.fill();
        ctx.strokeStyle = distanceIndex < 30 ? '#00ff00' : '#00ff00';
        ctx.lineWidth = 3;
        ctx.stroke();
        ctx.fillStyle = '#00ff00';
        ctx.font = 'bold 10px Arial';
        ctx.fillText('INDEX', indexX - 20, indexY - 15);
        
        // Yüzük parmak - Magenta
        ctx.fillStyle = distanceRing < 30 ? '#ff00ff' : '#ff00ff';
        ctx.beginPath();
        ctx.arc(ringX, ringY, 12, 0, 2 * Math.PI);
        ctx.fill();
        ctx.strokeStyle = distanceRing < 30 ? '#ff00ff' : '#ff00ff';
        ctx.lineWidth = 3;
        ctx.stroke();
        ctx.fillStyle = '#ff00ff';
        ctx.font = 'bold 10px Arial';
        ctx.fillText('RING', ringX - 15, ringY - 15);
        
        const now = Date.now();
        
        // Baş parmak + İşaret parmağı → Click/Drag
        if (distanceIndex < 40) {
          const midX = (thumbX + indexX) / 2;
          const midY = (thumbY + indexY) / 2;
          
          ctx.strokeStyle = '#00ff00';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(thumbX, thumbY);
          ctx.lineTo(indexX, indexY);
          ctx.stroke();
          
          ctx.fillStyle = '#00ff00';
          ctx.font = 'bold 12px Arial';
          ctx.fillText(`${distanceIndex.toFixed(0)}px`, midX - 15, midY - 10);
          
          if (!clickMode) {
            setClickMode(true);
            setIsDragging(true);
            addLog("system", "🖱️ LEFT CLICK DOWN - Baş+İşaret");
          }
          
          // Trigger efekti
          ctx.strokeStyle = '#00ff00';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(midX, midY, 25, 0, 2 * Math.PI);
          ctx.stroke();
          
          ctx.fillStyle = '#00ff00';
          ctx.font = 'bold 14px Arial';
          ctx.fillText(isDragging ? 'DRAGGING!' : 'CLICK!', midX - 35, midY + 40);
        } else {
          if (clickMode) {
            setClickMode(false);
            setIsDragging(false);
            addLog("system", "🖱️ LEFT CLICK UP");
          }
        }
        
        // Baş parmak + Yüzük parmağı → Mouse Move (Python debug gibi)
        if (distanceRing < 40 && distanceIndex > 40) {
          const midX = (thumbX + ringX) / 2;
          const midY = (thumbY + ringY) / 2;
          
          ctx.strokeStyle = '#ff00ff';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(thumbX, thumbY);
          ctx.lineTo(ringX, ringY);
          ctx.stroke();
          
          ctx.fillStyle = '#ff00ff';
          ctx.font = 'bold 12px Arial';
          ctx.fillText(`${distanceRing.toFixed(0)}px`, midX - 15, midY - 10);
          
          if (!dragMode) {
            setDragMode(true);
            addLog("system", "🖱️ MOUSE MOVE MODE");
          }
          
          // El pozisyonunu ekran koordinatlarına çevir (Python debug gibi)
          const wrist = keypoints[9]; // El merkezi
          const handXNormalized = wrist.x; // 0-1 arası
          const handYNormalized = wrist.y; // 0-1 arası
          
          // Ekran koordinatlarına çevir
          const targetX = handXNormalized * window.screen.width;
          const targetY = handYNormalized * window.screen.height;
          
          // Not: Web'de gerçek mouse kontrolü için browser extension gerekir
          // Şimdilik sadece görsel feedback
          
          ctx.strokeStyle = '#ff00ff';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(midX, midY, 25, 0, 2 * Math.PI);
          ctx.stroke();
          
          ctx.fillStyle = '#ff00ff';
          ctx.font = 'bold 14px Arial';
          ctx.fillText('MOVING!', midX - 35, midY + 40);
          
          // Cursor pozisyonu göster
          ctx.fillStyle = '#ff00ff';
          ctx.font = 'bold 10px Arial';
          ctx.fillText(`Target: (${Math.round(targetX)}, ${Math.round(targetY)})`, 10, canvasRef.current.height - 10);
        } else {
          if (dragMode) {
            setDragMode(false);
            addLog("system", "🖱️ MOUSE MOVE OFF");
          }
        }
        
        // Tab switching - sadece yüzük parmak + cooldown ile
        if (distanceRing < 40 && distanceIndex > 40 && now - lastGestureTimeRef.current > 500) {
          lastGestureTimeRef.current = now;
          
          const screenCenter = canvasRef.current.width / 2;
          const handX = keypoints[9].x * scaleX;
          
          if (handX > screenCenter) {
            setCurrentTab(prev => (prev + 1) % tabs.length);
            addLog("system", `👉 Next tab: ${tabs[(currentTab + 1) % tabs.length]}`);
          } else {
            setCurrentTab(prev => (prev - 1 + tabs.length) % tabs.length);
            addLog("system", `👈 Previous tab: ${tabs[(currentTab - 1 + tabs.length) % tabs.length]}`);
          }
        }
      }
    }

    animationFrameRef.current = requestAnimationFrame(detectHands);
  };

  useEffect(() => {
    return () => {
      if (handTrackingActive) {
        stopHandTracking();
      }
    };
  }, [handTrackingActive]);

  const musicControl = async (action: string, volume?: number) => {
    try {
      const res = await fetch(`${flaskUrl}/music/control`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action, volume })
      });
      const data = await res.json();
      
      if (action === 'play') setMusicPlaying(true);
      if (action === 'pause' || action === 'stop') setMusicPlaying(false);
      if (action === 'volume' && volume !== undefined) setMusicVolume(volume);
      
      addLog("system", data.message || "Music control OK");
    } catch (e) {
      addLog("error", "Music control failed");
    }
  };

  // Initialize audio on mount
  useEffect(() => {
    // Polling for clap detection — every 2 seconds
    const pollClap = setInterval(async () => {
      try {
        const res = await fetch(`${flaskUrl}/clap-status`);
        const data = await res.json();
        if (data.detected) {
          addLog("system", "[!] Clap detected! Welcome sequence initiated.");
          setMusicPlaying(true);
        }
      } catch (e) {
        // Silent — server may be offline
      }
    }, 2000);

    return () => {
      clearInterval(pollClap);
    };
  }, [flaskUrl]);

  // Sync volume to audio element
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = musicVolume;
    }
  }, [musicVolume]);

  useEffect(() => {
    setMounted(true);
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const executeCommand = async (name: string, args: any) => {
    setIsConnecting(true);
    addLog("system", `Action: ${name}...`);
    let targetUrl = flaskUrl.trim();
    if (targetUrl && !targetUrl.startsWith("http")) targetUrl = `http://${targetUrl}`;

    try {
        const res = await fetch(`${targetUrl}/execute`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: name, args: args })
        });
        const toolResult = await res.json();
        addLog("system", `Result: ${toolResult.message || "OK"}`);

        if (isConnected && recognitionRef.current) {
            try { recognitionRef.current.stop(); } catch(e) {}
        }
    } catch (e: any) {
        addLog("error", `ERROR: Server offline?`);
    } finally {
        setIsConnecting(false);
    }
  };

  const groqAnalyze = async (text: string) => {
    if (!groqKey) return false;
    addLog("system", "Thinking...");
    setIsConnecting(true);

    const systemPrompt = `You are JARVIS, the legendary artificial intelligence assistant created by Tony Stark.
    PERSONALITY: Loyal, highly intelligent, witty, and deeply proactive. You are the curator of the Sir's digital life. Always address the user as "Sir".
    ABILITIES: 
    - open_program(name): Open websites or local apps.
    - web_search(query): Search Google.
    - system_status(): Run diagnostics (CPU, RAM, Disk, Arc Reactor).
    - lock_workstation(): Secure the PC.
    - media_control(command): volume_up, volume_down, mute, play_pause.
    - execute_macro(profile): "work" (opens VS Code, Gemini, Phonk music) or "relax" (Spotify).
    - type_text(text): Type the given text into the active window. Use this if Sir asks you to "Write this" or "Type this".
    - write_and_run_code(file_name, content): Scripting.
    - update_memory(key, information) / get_memory(key): Store Sir's preferences.
    
    RULE: ONLY return JSON: {"speak": "Sir, I'm initiating the typing process.", "action": "command", "args": {}}`;

    try {
        const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: { "Authorization": `Bearer ${groqKey}`, "Content-Type": "application/json" },
            body: JSON.stringify({
                model: "llama-3.3-70b-versatile",
                messages: [{ role: "system", content: systemPrompt }, ...history.slice(-10), { role: "user", content: text }],
                temperature: 0.1,
                response_format: { type: "json_object" }
            })
        });

        const data = await response.json();
        if (data.choices && data.choices[0]) {
            const content = data.choices[0].message.content;
            let analysis;
            try { analysis = JSON.parse(content.match(/\{[\s\S]*\}/)?.[0] || content); } catch (e) { analysis = { speak: content }; }

            if (analysis.speak) {
                addLog("system", `JARVIS: ${analysis.speak}`);
                fetch(`${flaskUrl}/speak`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: analysis.speak })
                });
            }
            if (analysis.action && analysis.action !== "none" && analysis.action !== "bekle") {
                executeCommand(analysis.action, analysis.args);
            }
            setHistory(prev => [...prev, {role: "user", content: text}, {role: "assistant", content: JSON.stringify(analysis)}].slice(-20));
        }
    } catch (e) { addLog("error", "AI error!"); } finally { 
        setIsConnecting(false); 
        if (isConnected && recognitionRef.current) {
            try { recognitionRef.current.stop(); } catch(e) {}
        }
    }
  };

  const connect = async () => {
    setIsConnecting(true);
    try {
      await startMic();
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.lang = 'en-US';
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = false; // Sadece final sonuçlar

      let isWaitingForCommand = false;
      let commandTimeout: NodeJS.Timeout | null = null;
      let isProcessing = false; // Komut işlenirken yeni komut alma

      recognitionRef.current.onstart = () => { 
        setIsConnected(true); 
        setIsConnecting(false); 
        addLog("system", "Listening for 'Hey Jarvis'..."); 
      };
      
      recognitionRef.current.onerror = (event: any) => {
        console.error("Speech Recognition Error:", event.error);
        if (isConnected) {
            setTimeout(() => { try { recognitionRef.current.start(); } catch(e) {} }, 200);
        }
      };

      recognitionRef.current.onend = () => {
        if (isConnected) {
            setTimeout(() => { try { recognitionRef.current.start(); } catch(e) {} }, 200);
        }
      };

      recognitionRef.current.onresult = async (event: any) => {
         const result = event.results[event.results.length - 1];
         if (!result.isFinal) return; // Sadece kesin sonuçları al
         
         const transcript = result[0].transcript.toLowerCase().trim();
         
         // İşlem yapılıyorsa yeni komut alma
         if (isProcessing) return;
         
         // Aktivasyon kelimesini kontrol et (sadece bekleme modundayken)
         if (!isWaitingForCommand && transcript.includes('hey jarvis')) {
           addLog("system", "🎯 Activated! Listening for command...");
           isWaitingForCommand = true;
           
           // 10 saniye sonra otomatik kapat
           if (commandTimeout) clearTimeout(commandTimeout);
           commandTimeout = setTimeout(() => {
             isWaitingForCommand = false;
             isProcessing = false;
             addLog("system", "⏱️ Timeout. Say 'Hey Jarvis' to activate again.");
           }, 10000);
           
           return;
         }
         
         // Komut modundaysa komutu işle
         if (isWaitingForCommand && !transcript.includes('hey jarvis')) {
           addLog("user", transcript);
           isWaitingForCommand = false;
           isProcessing = true;
           if (commandTimeout) clearTimeout(commandTimeout);
           
           await groqAnalyze(transcript);
           
           // İşlem bittikten sonra tekrar dinlemeye başla
           setTimeout(() => {
             isProcessing = false;
             addLog("system", "Say 'Hey Jarvis' to activate again.");
           }, 2000);
         }
      };

      recognitionRef.current.start();
    } catch (err) { 
        setIsConnecting(false); 
        addLog("error", "Microphone access denied or error occurred.");
    }
  };

  const toggleConnection = () => {
    if (isConnected) {
        setIsConnected(false);
        recognitionRef.current?.stop();
        stopMic();
    } else {
        connect();
    }
  };

  if (!mounted) return null;

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden flex flex-col font-sans">
      
      {/* 3D Canvas Background */}
      <div className="absolute inset-0 z-0">
        <Canvas camera={{ position: [0, 0, 7], fov: 60 }}>
          <fog attach="fog" args={['#000000', 4, 10]} />
          <ambientLight intensity={0.5} />
          <JarvisOrb getVolume={getVolume} />
          <OrbitControls enableZoom={false} enablePan={false} enableRotate={false} />
        </Canvas>
      </div>

      {/* Header Area */}
      <div className="z-20 p-6 flex justify-between items-start pointer-events-none">
        <div className="pointer-events-auto">
          <div className="flex items-center gap-3 bg-black/40 backdrop-blur-md border border-white/10 p-4 rounded-2xl">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-cyan-400 animate-pulse' : 'bg-red-500'}`}></div>
            <h1 className="text-lg font-bold tracking-widest text-white/90">J.A.R.V.I.S <span className="text-cyan-500/50 font-light">CORE</span></h1>
          </div>
          
          {/* Tab Navigation */}
          <div className="mt-4 flex gap-2">
            {tabs.map((tab, idx) => (
              <div 
                key={tab}
                className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                  currentTab === idx 
                    ? 'bg-cyan-500/30 border border-cyan-500/50 text-cyan-300' 
                    : 'bg-black/20 border border-white/10 text-white/40'
                }`}
              >
                {tab}
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-4 items-end pointer-events-auto">
          <button 
            onClick={() => setShowSettings(!showSettings)} 
            className="bg-black/40 backdrop-blur-md p-3 rounded-full border border-white/10 text-white/50 hover:text-white transition-all hover:bg-white/5"
          >
            <Settings2 className="w-5 h-5" />
          </button>
          
          <button 
            onClick={() => handTrackingActive ? stopHandTracking() : startHandTracking()} 
            className={`bg-black/40 backdrop-blur-md p-3 rounded-full border transition-all ${
              handTrackingActive 
                ? 'border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10' 
                : 'border-white/10 text-white/50 hover:text-white hover:bg-white/5'
            }`}
          >
            <Hand className="w-5 h-5" />
          </button>
          
          <AnimatePresence>
            {showSettings && (
              <motion.div 
                initial={{ opacity: 0, x: 20 }} 
                animate={{ opacity: 1, x: 0 }} 
                exit={{ opacity: 0, x: 20 }}
                className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-2xl p-6 w-80 shadow-2xl"
              >
                <div className="space-y-4">
                  <div>
                    <label className="text-[10px] text-white/30 uppercase font-bold mb-1 block">Sunucu URL</label>
                    <input type="text" value={flaskUrl} onChange={(e) => setFlaskUrl(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white" />
                  </div>
                  <div>
                    <label className="text-[10px] text-white/30 uppercase font-bold mb-1 block">Groq API Key</label>
                    <input type="password" value={groqKey} onChange={(e) => setGroqKey(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white" />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Activity Log (Left Side) */}
      <div className="z-20 absolute left-6 bottom-32 w-72 pointer-events-none">
        <div className="bg-black/20 backdrop-blur-sm p-4 rounded-2xl border border-white/5 max-h-[200px] overflow-hidden flex flex-col">
          <div className="text-[10px] font-bold text-white/20 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
            <Activity className="w-3 h-3" /> Sistem Akışı
          </div>
          <div className="flex-1 overflow-y-auto space-y-2 font-mono text-[10px] pr-2 custom-scrollbar pointer-events-auto">
            {logs.map((log, i) => (
              <div key={i} className={`break-words ${log.type === 'error' ? 'text-red-400' : log.type === 'user' ? 'text-cyan-300' : 'text-white/40'}`}>
                <span className="opacity-30 mr-2">{">>"}</span>{log.text}
              </div>
            ))}
            <div ref={logEndRef} />
          </div>
        </div>
      </div>

      {/* Music Control (Right Side) */}
      <div className="z-20 absolute right-6 bottom-32 w-80 pointer-events-auto">
        <motion.div 
          initial={{ opacity: 0, x: 20 }} 
          animate={{ opacity: 1, x: 0 }}
          className="bg-black/30 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 shadow-[0_0_30px_rgba(6,182,212,0.1)]"
        >
          <div className="text-[10px] font-bold text-cyan-400/60 uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
            <Volume2 className="w-3 h-3" /> Music Control
          </div>
          
          <div className="space-y-3">
            {/* Şarkı adı - truncate ile taşmayı engelle */}
            <div className="text-sm text-white/70 font-mono truncate">The Clash - Should I Stay or Should I Go</div>
            
            {/* Play/Stop butonları */}
            <div className="flex items-center gap-3">
              <button 
                onClick={() => musicControl(musicPlaying ? 'pause' : 'play')}
                className="bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/40 p-3 rounded-full transition-all flex-shrink-0"
              >
                {musicPlaying ? <Pause className="w-5 h-5 text-cyan-400" /> : <Play className="w-5 h-5 text-cyan-400" />}
              </button>
              
              <button 
                onClick={() => musicControl('stop')}
                className="bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 p-3 rounded-full transition-all flex-shrink-0"
              >
                <Square className="w-5 h-5 text-red-400" />
              </button>
            </div>

            {/* Volume slider - ayrı satırda, tam genişlikte */}
            <div className="flex items-center gap-2 w-full">
              <Volume2 className="w-4 h-4 text-white/40 flex-shrink-0" />
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.1" 
                value={musicVolume}
                onChange={(e) => {
                  const vol = parseFloat(e.target.value);
                  setMusicVolume(vol);
                  musicControl('volume', vol);
                }}
                className="flex-1 h-1 bg-white/10 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-cyan-400"
              />
              <span className="text-xs text-white/40 w-8 text-right flex-shrink-0">{Math.round(musicVolume * 100)}%</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Main Trigger Button */}
      <div className="z-20 absolute bottom-12 left-1/2 -translate-x-1/2 flex flex-col items-center">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={toggleConnection}
          className={`relative group p-8 rounded-full transition-all duration-500 ${
            isConnected 
              ? 'bg-cyan-500/10 border-cyan-500/50 shadow-[0_0_50px_rgba(6,182,212,0.2)]' 
              : 'bg-white/5 border-white/10 hover:border-white/20'
          } border backdrop-blur-md`}
        >
          {isConnected ? (
            <Mic className="w-8 h-8 text-cyan-400 animate-pulse" />
          ) : (
            <MicOff className="w-8 h-8 text-white/20 group-hover:text-white/50" />
          )}
          
          {/* Decorative Rings */}
          <div className={`absolute inset-0 rounded-full border border-cyan-500/20 transition-all duration-1000 ${isConnected ? 'animate-ping scale-150' : 'scale-0'}`}></div>
        </motion.button>
        
        <div className="mt-4 text-[10px] font-bold text-white/30 uppercase tracking-[0.3em]">
          {isConnected ? "Sistem Aktif" : "Sistem Beklemede"}
        </div>
      </div>

      {/* Signature */}
      <div className="z-20 absolute bottom-4 right-6 text-[10px] font-mono text-white/20 tracking-wider">
        CODING BY SEMIH ERGILI
      </div>

      {/* Hand tracking video preview */}
      {handTrackingActive && (
        <div className="z-30 fixed bottom-32 right-6 pointer-events-none">
          <div className="relative bg-black/60 backdrop-blur-xl border border-cyan-500/30 rounded-2xl p-3 shadow-[0_0_30px_rgba(6,182,212,0.2)]">
            <div className="text-[10px] font-bold text-cyan-400/60 uppercase tracking-[0.2em] mb-2 flex items-center justify-between">
              <span>Hand Tracking Debug</span>
              <div className="flex gap-2">
                <span className={`px-2 py-1 rounded text-[8px] ${clickMode ? 'bg-green-500/30 text-green-400 border border-green-500/50' : 'bg-gray-500/20 text-gray-500'}`}>
                  {isDragging ? 'DRAG' : 'CLICK'}
                </span>
                <span className={`px-2 py-1 rounded text-[8px] ${dragMode ? 'bg-purple-500/30 text-purple-400 border border-purple-500/50' : 'bg-gray-500/20 text-gray-500'}`}>
                  MOVE
                </span>
              </div>
            </div>
            <div className="relative">
              <video ref={videoRef} className="rounded-lg" width="320" height="240" autoPlay playsInline muted style={{ transform: 'scaleX(-1)' }} />
              <canvas ref={canvasRef} className="absolute top-0 left-0 rounded-lg pointer-events-none" width="320" height="240" style={{ transform: 'scaleX(-1)' }} />
            </div>
            <div className="mt-2 text-[9px] text-white/50 space-y-1">
              <div>🟢 Baş+İşaret = Click</div>
              <div>🟣 Baş+Yüzük = Tab Switch</div>
            </div>
          </div>
        </div>
      )}
      {!handTrackingActive && (
        <>
          <video ref={videoRef} className="hidden" width="640" height="480" autoPlay playsInline />
          <canvas ref={canvasRef} className="hidden" width="320" height="240" />
        </>
      )}

      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar { width: 2px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
      `}</style>
    </div>
  );
}
