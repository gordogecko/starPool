import streamlit as st
import streamlit.components.v1 as components

# Configure the Streamlit page layout
st.set_page_config(
    page_title="3D Zero-Gravity Pool - Star Pool Pocket Edition",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit header/footer elements for an immersive full-screen feel
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Embed the complete HTML, CSS, and JavaScript game code inside the Streamlit component
game_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>3D Zero-Gravity Pool - Star Pool Pocket Edition</title>
    <style>
        :root {
            --hull-blue: #09172e;
            --laser-cyan: #00f3ff;
            --plasma-orange: #ff5500;
            --shield-purple: #9d00ff;
            --carbon-grey: #22252a;
            --glass-bg: rgba(6, 15, 34, 0.75);
            --border-glow: rgba(0, 243, 255, 0.4);
        }

        body, html {
            margin: 0;
            padding: 0;
            overflow: hidden;
            width: 100vw;
            height: 100vh;
            background-color: #02020a;
            font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
            color: #fff;
            user-select: none;
            -webkit-user-select: none;
        }

        canvas {
            display: block;
            width: 100vw;
            height: 100vh;
            position: absolute;
            z-index: 1;
        }

        /* HUD & Space Console Container */
        #hud-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 10;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
            padding: 16px;
        }

        .interactive {
            pointer-events: auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
        }

        .space-panel {
            background: var(--glass-bg);
            border: 1.5px solid var(--laser-cyan);
            border-radius: 6px;
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.25), inset 0 0 10px rgba(0, 243, 255, 0.1);
            padding: 10px 16px;
            backdrop-filter: blur(8px);
        }

        .title-panel h1 {
            margin: 0;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 2px;
            color: var(--laser-cyan);
            text-shadow: 0 0 8px var(--laser-cyan);
            text-transform: uppercase;
        }

        .stats-panel {
            font-size: 13px;
            letter-spacing: 1.5px;
            font-weight: 600;
            display: flex;
            gap: 15px;
            border-color: var(--shield-purple);
            box-shadow: 0 0 15px rgba(157, 0, 255, 0.25), inset 0 0 10px rgba(157, 0, 255, 0.1);
        }

        .stat-val {
            color: var(--laser-cyan);
            text-shadow: 0 0 5px var(--laser-cyan);
        }

        .quit-btn {
            background: rgba(255, 30, 30, 0.15);
            color: #ff4444;
            border: 1.5px solid #ff4444;
            padding: 8px 16px;
            font-family: inherit;
            font-weight: bold;
            font-size: 12px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border-radius: 4px;
            cursor: pointer;
            box-shadow: 0 0 8px rgba(255, 0, 0, 0.3);
            transition: all 0.2s ease;
        }

        .quit-btn:hover {
            background: #ff4444;
            color: #000;
            box-shadow: 0 0 18px #ff4444;
        }

        /* Controls Panel Grid */
        .controls-bottom {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            width: 100%;
            margin-bottom: 5px;
        }

        /* Radar styled Aim Joystick */
        .joystick-outer {
            width: 184px;
            height: 184px;
            border-radius: 50%;
            background: rgba(2, 6, 18, 0.85);
            border: 2px solid var(--laser-cyan);
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.25);
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            touch-action: none;
        }

        .joystick-outer::before {
            content: "";
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(from 0deg, rgba(0, 243, 255, 0.15) 0%, rgba(0,243,255,0) 50%);
            animation: radar-sweep 4s linear infinite;
            pointer-events: none;
        }

        @keyframes radar-sweep {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .joystick-outer::after {
            content: "";
            position: absolute;
            width: 80%;
            height: 80%;
            border-radius: 50%;
            border: 1px dashed rgba(0, 243, 255, 0.35);
            pointer-events: none;
        }

        .joystick-inner {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: radial-gradient(circle, #ffffff 10%, var(--laser-cyan) 60%, #008fa6 100%);
            box-shadow: 0 0 12px var(--laser-cyan);
            position: absolute;
            cursor: pointer;
            transition: transform 0.05s ease;
        }

        .joystick-label {
            position: absolute;
            top: -24px;
            font-size: 10px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: var(--laser-cyan);
            text-shadow: 0 0 6px var(--laser-cyan);
            white-space: nowrap;
        }

        /* Space Weapon Trigger styled Strike button */
        .strike-center-panel {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }

        .strike-btn {
            width: 96px;
            height: 96px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--shield-purple) 0%, #3a0066 100%);
            border: 2px solid var(--laser-cyan);
            color: var(--laser-cyan);
            font-family: inherit;
            font-weight: 700;
            font-size: 15px;
            letter-spacing: 2px;
            text-transform: uppercase;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(157, 0, 255, 0.4), inset 0 0 10px rgba(0, 243, 255, 0.3);
            transition: all 0.1s ease;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .strike-btn:hover {
            background: radial-gradient(circle, #b833ff 0%, #4c0080 100%);
            box-shadow: 0 0 25px var(--laser-cyan), inset 0 0 15px rgba(157, 0, 255, 0.4);
            color: #fff;
        }

        .strike-btn:active {
            transform: scale(0.92);
            background: var(--laser-cyan);
            color: #02020a;
            box-shadow: 0 0 30px var(--laser-cyan);
        }

        /* Spaceship Engine Throttle Lever */
        .power-throttle-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 150px;
            position: relative;
        }

        .power-track {
            width: 20px;
            height: 110px;
            background: rgba(3, 10, 24, 0.9);
            border: 2.5px solid var(--shield-purple);
            box-shadow: 0 0 12px rgba(157, 0, 255, 0.3);
            border-radius: 6px;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: flex-end;
            cursor: pointer;
            touch-action: none;
        }

        .power-fill {
            width: 100%;
            height: 60%;
            background: linear-gradient(to top, var(--shield-purple), var(--laser-cyan), #ffffff);
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.6);
            transition: height 0.05s linear;
        }

        .power-handle {
            width: 30px;
            height: 12px;
            background: var(--laser-cyan);
            border: 1.5px solid #fff;
            box-shadow: 0 0 10px var(--laser-cyan);
            border-radius: 3px;
            position: absolute;
            left: -7px;
            bottom: 60%;
            transform: translateY(50%);
            pointer-events: none;
            transition: bottom 0.05s linear;
        }

        .power-label {
            font-size: 10px;
            color: var(--laser-cyan);
            text-shadow: 0 0 5px var(--laser-cyan);
            margin-top: 6px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        /* Overlay screens */
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(2, 4, 10, 0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 100;
            box-sizing: border-box;
            padding: 20px;
            transition: opacity 0.3s ease;
        }

        .overlay-content {
            max-width: 500px;
            text-align: center;
            border: 2px solid var(--laser-cyan);
            border-radius: 8px;
            box-shadow: 0 0 35px rgba(0, 243, 255, 0.35), inset 0 0 15px rgba(0, 243, 255, 0.15);
            background: rgba(4, 9, 21, 0.98);
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 25px;
        }

        .overlay h2 {
            margin: 0;
            font-size: 26px;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: var(--laser-cyan);
            text-shadow: 0 0 10px var(--laser-cyan);
        }

        .overlay h2.alert-text {
            color: #ff3333;
            text-shadow: 0 0 10px #ff3333;
            border-color: #ff3333;
        }

        .overlay p {
            font-size: 14px;
            line-height: 1.6;
            color: #abbccd;
            margin: 0;
        }

        .menu-btn {
            background: rgba(0, 243, 255, 0.15);
            color: var(--laser-cyan);
            border: 1.5px solid var(--laser-cyan);
            padding: 12px 32px;
            font-family: inherit;
            font-weight: bold;
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            border-radius: 4px;
            cursor: pointer;
            box-shadow: 0 0 12px rgba(0, 243, 255, 0.25);
            transition: all 0.2s ease;
        }

        .menu-btn:hover {
            background: var(--laser-cyan);
            color: #000;
            box-shadow: 0 0 25px var(--laser-cyan);
        }

        .menu-btn.alt-btn {
            background: rgba(255, 50, 50, 0.15);
            color: #ff4444;
            border-color: #ff4444;
            box-shadow: 0 0 12px rgba(255, 70, 70, 0.25);
        }

        .menu-btn.alt-btn:hover {
            background: #ff4444;
            color: #000;
            box-shadow: 0 0 25px #ff4444;
        }

        /* Screen Danger Alert */
        #alert-panel {
            position: absolute;
            top: 25%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 50;
            background: rgba(255, 30, 30, 0.9);
            border: 2px solid #fff;
            box-shadow: 0 0 30px #ff0000;
            border-radius: 6px;
            padding: 14px 30px;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 2.5px;
            color: #fff;
            text-transform: uppercase;
            text-align: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }

        .hidden {
            display: none !important;
            opacity: 0;
        }

        @media (max-width: 600px) {
            #hud-container { padding: 12px; }
            .title-panel h1 { font-size: 13px; letter-spacing: 1px; }
            .stats-panel { font-size: 11px; gap: 10px; padding: 8px 10px; }
            .quit-btn { padding: 6px 12px; font-size: 11px; }
            .joystick-outer { width: 90px; height: 90px; }
            .joystick-inner { width: 32px; height: 32px; }
            .strike-btn { width: 76px; height: 76px; font-size: 12px; }
            .power-throttle-container { height: 120px; }
            .power-track { width: 16px; height: 85px; }
            .power-handle { width: 24px; height: 8px; left: -6px; }
            .overlay-content { padding: 25px; }
            .overlay h2 { font-size: 19px; }
        }
    </style>

    <script async src="https://unpkg.com/es-module-shims@1.8.0/dist/es-module-shims.js"></script>
    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }
        }
    </script>
</head>
<body>
    <!-- Welcome Overlay -->
    <div id="welcome-overlay" class="overlay">
        <div class="overlay-content">
            <h2>STAR POOL POCKET</h2>
            <p>Welcome to deep orbit, Captain. You are situated at the viewport of a high-containment magnetic rectangular chamber floating within a gorgeous glowing stellar nebula.</p>
            <p style="color: var(--laser-cyan);">Align the Holographic Laser Cue with the Left Radar Joystick.<br>Throttle Engine Power with the Right Energy Track.<br>Launch strikes to displace kinetic bodies.</p>
            <p style="color: var(--plasma-orange); font-size: 11px;">Mission objective: Warp ALL target balls (8 through 15) into any corner gravitational vortex. Avoid losing the White Cue Ball to the gravity wells.</p>
            <button id="start-game-btn" class="menu-btn interactive">INITIATE MISSION</button>
        </div>
    </div>

    <!-- Confirm Quit Overlay -->
    <div id="quit-overlay" class="overlay hidden">
        <div class="overlay-content" style="border-color:#ff4444; box-shadow: 0 0 30px rgba(255,0,0,0.4);">
            <h2 class="alert-text">ABORT MISSION?</h2>
            <p>Ejecting from current space-drift coordinate sector will scrap all stellar progress.</p>
            <div style="display:flex; gap:15px; width:100%;">
                <button id="confirm-quit-btn" class="menu-btn alt-btn interactive" style="flex:1;">ABORT FLIGHT</button>
                <button id="cancel-quit-btn" class="menu-btn interactive" style="flex:1;">STAY ON BRIDGE</button>
            </div>
        </div>
    </div>

    <!-- Game Over Screen -->
    <div id="gameover-overlay" class="overlay hidden">
        <div class="overlay-content" style="border-color:#ff4444; box-shadow: 0 0 30px rgba(255,0,0,0.4);">
            <h2 class="alert-text">COSMIC TERMINATION</h2>
            <p>Drifting in space. The navigation bridge has shut down.</p>
            <button id="restart-gameover-btn" class="menu-btn interactive">REBOOT CORE</button>
        </div>
    </div>

    <!-- Victory Overlay -->
    <div id="victory-overlay" class="overlay hidden">
        <div class="overlay-content" style="border-color:var(--laser-cyan); box-shadow: 0 0 30px rgba(0,243,255,0.4);">
            <h2 style="color: var(--laser-cyan);">ORBIT ACHIEVED!</h2>
            <p>Excellent shot sequence! The gravity anchor has absorbed a target ball safely.</p>
            <p style="font-size: 18px; color: #fff;">FLIGHT MANEUVERS: <span id="final-shots" class="stat-val">0</span></p>
            <p style="font-size: 18px; color: #fff;">SCORE: <span id="final-score" class="stat-val">0</span></p>
            <button id="victory-restart-btn" class="menu-btn interactive">NEXT EXPEDITION</button>
        </div>
    </div>

    <!-- Screen Hazard Warning -->
    <div id="alert-panel">GRAVITY WELL SCRATCH</div>

    <!-- MAIN HUD CONSOLE -->
    <div id="hud-container">
        <header>
            <div class="space-panel title-panel">
                <h1>STAR POOL POCKET // SHIP CONSOLE</h1>
            </div>
            <div class="space-panel stats-panel">
                <div>SCORE: <span id="hud-score" class="stat-val">0</span></div>
                <div>MANEUVERS: <span id="hud-shots" class="stat-val">0</span></div>
                <div>GRAV CORE: <span id="hud-status" style="color:var(--plasma-orange); text-shadow:0 0 5px var(--plasma-orange);">STABLE</span></div>
            </div>
            <button id="top-quit-btn" class="quit-btn interactive">EJECT</button>
        </header>

        <div style="display:none;">
            <input type="range" id="h-angle" min="0" max="360" value="45">
            <input type="range" id="v-angle" min="-90" max="90" value="15">
            <input type="range" id="power" min="5" max="100" value="60">
        </div>

        <div class="controls-bottom">
            <div class="joystick-outer interactive" id="joystick-boundary">
                <span class="joystick-label">AZIMUTH AIM</span>
                <div class="joystick-inner" id="joystick-knob"></div>
            </div>

            <div class="strike-center-panel">
                <button id="strike-btn" class="strike-btn interactive">FIRE</button>
            </div>

            <div class="power-throttle-container interactive" id="power-throttle-zone">
                <div class="power-track" id="power-slider-track">
                    <div class="power-fill" id="power-fill-bar"></div>
                    <div class="power-handle" id="power-handle-indicator"></div>
                </div>
                <span class="power-label">THRUST</span>
            </div>
        </div>
    </div>

    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

        let shotsCount = 0;
        let playerScore = 0;
        let isGameOver = false;
        let aimingHorizontal = 45; 
        let aimingVertical = 15;   
        let strikePower = 60;      
        let cueOffset = 0;         
        let strikeState = "idle";  
        let pullbackProgress = 0;
        let releaseProgress = 0;
        let recoilProgress = 0;

        let cueAnchorPosition = new THREE.Vector3();
        let cueAnchorDirection = new THREE.Vector3();
        let isCueLocked = false;

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        function playSciFiSound(type) {
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            if (type === 'clack') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(500, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(150, audioCtx.currentTime + 0.12);
                
                const filter = audioCtx.createBiquadFilter();
                filter.type = 'bandpass';
                filter.frequency.setValueAtTime(450, audioCtx.currentTime);
                filter.Q.setValueAtTime(8, audioCtx.currentTime);
                osc.disconnect(gain);
                osc.connect(filter);
                filter.connect(gain);

                gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.005, audioCtx.currentTime + 0.12);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.13);
            } 
            else if (type === 'thud') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(140, audioCtx.currentTime);
                osc.frequency.linearRampToValueAtTime(60, audioCtx.currentTime + 0.2);
                
                gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.21);
            } 
            else if (type === 'pocket') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(400, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.5);
                
                gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.51);
            } 
            else if (type === 'laser') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(60, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.14);
                
                gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.005, audioCtx.currentTime + 0.15);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.15);
            }
            else if (type === 'reward') {
                const now = audioCtx.currentTime;
                const playTone = (freq, start, duration) => {
                    const oscTone = audioCtx.createOscillator();
                    const gainTone = audioCtx.createGain();
                    oscTone.type = 'sine';
                    oscTone.frequency.setValueAtTime(freq, start);
                    oscTone.frequency.exponentialRampToValueAtTime(freq * 1.5, start + duration);
                    
                    gainTone.gain.setValueAtTime(0, start);
                    gainTone.gain.linearRampToValueAtTime(0.2, start + 0.05);
                    gainTone.gain.exponentialRampToValueAtTime(0.001, start + duration);
                    
                    oscTone.connect(gainTone);
                    gainTone.connect(audioCtx.destination);
                    oscTone.start(start);
                    oscTone.stop(start + duration + 0.05);
                };
                
                playTone(523.25, now, 0.35); // C5
                playTone(659.25, now + 0.08, 0.35); // E5
                playTone(783.99, now + 0.16, 0.35); // G5
                playTone(1046.50, now + 0.24, 0.5); // C6
            }
        }

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020208);
        scene.fog = new THREE.FogExp2(0x020208, 0.012);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(35, 25, 45);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.35;
        document.body.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxDistance = 150;
        controls.minDistance = 5.5;

        const ambientLight = new THREE.AmbientLight(0x180f2d, 0.75);
        scene.add(ambientLight);

        const starLight1 = new THREE.DirectionalLight(0xa6f0ff, 1.3);
        starLight1.position.set(12, 20, 14);
        scene.add(starLight1);

        const starLight2 = new THREE.DirectionalLight(0x9d00ff, 0.85);
        starLight2.position.set(-15, -8, -12);
        scene.add(starLight2);

        const coreLight = new THREE.PointLight(0xff5500, 1.8, 35);
        coreLight.position.set(0, 0, 0);
        scene.add(coreLight);

        const roomW = 32, roomH = 16, roomD = 20;
        const boxGeometry = new THREE.BoxGeometry(roomW, roomH, roomD);

        function createNebulaTexture() {
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');
            
            ctx.fillStyle = '#02020a';
            ctx.fillRect(0, 0, 512, 512);
            
            ctx.globalCompositeOperation = 'screen';
            
            const radGrad1 = ctx.createRadialGradient(150, 150, 20, 180, 180, 240);
            radGrad1.addColorStop(0, 'rgba(157, 0, 255, 0.35)');
            radGrad1.addColorStop(0.5, 'rgba(110, 0, 180, 0.15)');
            radGrad1.addColorStop(1, 'rgba(0,0,0,0)');
            ctx.fillStyle = radGrad1;
            ctx.fillRect(0, 0, 512, 512);

            const radGrad2 = ctx.createRadialGradient(380, 360, 10, 350, 350, 200);
            radGrad2.addColorStop(0, 'rgba(0, 243, 255, 0.35)');
            radGrad2.addColorStop(0.6, 'rgba(0, 120, 180, 0.12)');
            radGrad2.addColorStop(1, 'rgba(0,0,0,0)');
            ctx.fillStyle = radGrad2;
            ctx.fillRect(0, 0, 512, 512);

            const radGrad3 = ctx.createRadialGradient(256, 256, 10, 256, 256, 110);
            radGrad3.addColorStop(0, 'rgba(255, 85, 0, 0.25)');
            radGrad3.addColorStop(1, 'rgba(0,0,0,0)');
            ctx.fillStyle = radGrad3;
            ctx.fillRect(0, 0, 512, 512);

            ctx.fillStyle = '#ffffff';
            ctx.globalCompositeOperation = 'source-over';
            for (let i = 0; i < 220; i++) {
                const sx = Math.random() * 512;
                const sy = Math.random() * 512;
                const size = 0.5 + Math.random() * 1.5;
                ctx.globalAlpha = 0.3 + Math.random() * 0.7;
                ctx.beginPath();
                ctx.arc(sx, sy, size, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.strokeStyle = 'rgba(0, 243, 255, 0.15)';
            ctx.lineWidth = 1;
            ctx.globalAlpha = 0.4;
            ctx.beginPath();
            for (let x = 0; x <= 512; x += 128) {
                ctx.moveTo(x, 0); ctx.lineTo(x, 512);
                ctx.moveTo(0, x); ctx.lineTo(512, x);
            }
            ctx.stroke();

            return new THREE.CanvasTexture(canvas);
        }

        const nebulaTex = createNebulaTexture();
        const boxMaterial = new THREE.MeshPhongMaterial({
            map: nebulaTex,
            transparent: true,
            opacity: 0.55,
            side: THREE.BackSide,
            shininess: 15
        });
        const roomMesh = new THREE.Mesh(boxGeometry, boxMaterial);
        scene.add(roomMesh);

        const edges = new THREE.EdgesGeometry(boxGeometry);
        const lineMaterial = new THREE.LineBasicMaterial({ color: 0x9d00ff, linewidth: 2 });
        const lineSegments = new THREE.LineSegments(edges, lineMaterial);
        scene.add(lineSegments);

        const pocketRadius = 1.35;
        const pocketGeometry = new THREE.SphereGeometry(pocketRadius, 32, 32);

        function createSingularityTexture() {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 256;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = '#020208';
            ctx.fillRect(0, 0, 256, 256);

            const grad = ctx.createRadialGradient(128, 128, 5, 128, 128, 120);
            grad.addColorStop(0, '#000000');
            grad.addColorStop(0.15, '#110022');
            grad.addColorStop(0.4, '#9d00ff');
            grad.addColorStop(0.7, '#ff5500');
            grad.addColorStop(0.95, '#ffffff');
            grad.addColorStop(1, '#020208');

            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, 256, 256);

            ctx.strokeStyle = '#ffffff';
            ctx.globalAlpha = 0.35;
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            for(let th = 0; th < Math.PI * 10; th += 0.08) {
                const radius = th * 3.5;
                const cx = 128 + radius * Math.cos(th + Math.PI);
                const cy = 128 + radius * Math.sin(th + Math.PI);
                if (th === 0) ctx.moveTo(cx, cy);
                else ctx.lineTo(cx, cy);
            }
            ctx.stroke();

            return new THREE.CanvasTexture(canvas);
        }

        const singularityTex = createSingularityTexture();
        const hw = roomW / 2, hh = roomH / 2, hd = roomD / 2;
        const pocketPositions = [
            [hw, hh, hd], [hw, hh, -hd], [hw, -hh, hd], [hw, -hh, -hd],
            [-hw, hh, hd], [-hw, hh, -hd], [-hw, -hh, hd], [-hw, -hh, -hd]
        ];

        const pockets = [];
        pocketPositions.forEach(v => {
            const pMat = new THREE.MeshBasicMaterial({
                map: singularityTex,
                transparent: true,
                opacity: 0.98
            });
            const pocket = new THREE.Mesh(pocketGeometry, pMat);
            pocket.position.set(v[0], v[1], v[2]);
            scene.add(pocket);
            pockets.push(pocket);
        });

        const ballRadius = 0.8;
        const balls = [];

        // Universal Ball Texture Generator for Solids (8) and Stripes (9-15)
        function createNumberedBallTexture(number, color, isStripe) {
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 256;
            const ctx = canvas.getContext('2d');

            if (isStripe) {
                // Solid White Base
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, 512, 256);
                // Color Stripe across the middle
                ctx.fillStyle = color;
                ctx.fillRect(0, 64, 512, 128);
            } else {
                // Solid Color Base
                ctx.fillStyle = color;
                ctx.fillRect(0, 0, 512, 256);
            }

            // Central White Circle
            ctx.fillStyle = '#ffffff';
            ctx.shadowColor = '#aaaaaa';
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.arc(256, 128, 54, 0, Math.PI * 2);
            ctx.fill();

            ctx.shadowBlur = 0;

            // Number
            ctx.fillStyle = '#0c0c0f';
            ctx.font = 'bold 72px "Segoe UI", sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(number.toString(), 256, 128);
            
            // Bottom underline for numbers 9 (to distinguish from 6)
            if (number === 9) {
                ctx.fillRect(236, 160, 40, 6);
            }

            return new THREE.CanvasTexture(canvas);
        }

        function createCueBallTexture() {
            const canvas = document.createElement('canvas');
            canvas.width = 128;
            canvas.height = 128;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, 128, 128);
            return new THREE.CanvasTexture(canvas);
        }

        const cueBallTex = createCueBallTexture();

        function createBall(textureMap, x, y, z, isCue) {
            const geometry = new THREE.SphereGeometry(ballRadius, 64, 64);
            const material = new THREE.MeshStandardMaterial({
                color: 0xffffff,
                map: textureMap,
                roughness: isCue ? 0.08 : 0.05,
                metalness: 0.0,
                emissive: isCue ? 0x3a3a3a : 0x000000,
                clearcoat: 1.0,
                clearcoatRoughness: 0.02
            });
            const ball = new THREE.Mesh(geometry, material);
            ball.position.set(x, y, z);
            ball.userData = { 
                velocity: new THREE.Vector3(0, 0, 0), 
                mass: 1,
                isCue: isCue,
                sunk: false,
                sunkProcessed: false,
                initialPos: new THREE.Vector3(x, y, z)
            };
            scene.add(ball);
            balls.push(ball);
            return ball;
        }

        // Initialize Cue Ball
        const cueBall = createBall(cueBallTex, -8, -3, -2, true);

        // Initialize Target Balls (8 through 15) with their standard colors
        const targetBallsData = [
            { num: 8, color: '#111111', isStripe: false, pos: [6, 0, 0] },     // 8 - Black (Solid)
            { num: 9, color: '#ffcc00', isStripe: true, pos: [8, 2, 2] },      // 9 - Yellow (Stripe)
            { num: 10, color: '#0033cc', isStripe: true, pos: [8, -2, -2] },   // 10 - Blue (Stripe)
            { num: 11, color: '#cc0000', isStripe: true, pos: [10, 4, 4] },    // 11 - Red (Stripe)
            { num: 12, color: '#6600cc', isStripe: true, pos: [10, -4, -4] },  // 12 - Purple (Stripe)
            { num: 13, color: '#ff6600', isStripe: true, pos: [10, 0, 0] },    // 13 - Orange (Stripe)
            { num: 14, color: '#006600', isStripe: true, pos: [12, 2, -2] },   // 14 - Green (Stripe)
            { num: 15, color: '#663300', isStripe: true, pos: [12, -2, 2] }    // 15 - Brown/Maroon (Stripe)
        ];

        targetBallsData.forEach(data => {
            const tex = createNumberedBallTexture(data.num, data.color, data.isStripe);
            createBall(tex, data.pos[0], data.pos[1], data.pos[2], false);
        });

        const cueGroup = new THREE.Group();
        scene.add(cueGroup);

        const shaftLength = 4.2;
        const buttLength = 4.8;

        const shaftGeom = new THREE.CylinderGeometry(0.045, 0.08, shaftLength, 16);
        shaftGeom.translate(0, -shaftLength/2, 0);
        const shaftMat = new THREE.MeshStandardMaterial({
            color: 0x00f3ff,
            emissive: 0x007799,
            roughness: 0.05,
            metalness: 0.9,
            transparent: true,
            opacity: 0.9
        });
        const shaftMesh = new THREE.Mesh(shaftGeom, shaftMat);
        cueGroup.add(shaftMesh);

        const buttGeom = new THREE.CylinderGeometry(0.08, 0.14, buttLength, 16);
        buttGeom.translate(0, -shaftLength - buttLength/2, 0);
        const buttMat = new THREE.MeshStandardMaterial({
            color: 0x1e2126,
            roughness: 0.35,
            metalness: 0.9
        });
        const buttMesh = new THREE.Mesh(buttGeom, buttMat);
        cueGroup.add(buttMesh);

        const bandGeom = new THREE.CylinderGeometry(0.12, 0.12, 0.15, 16);
        bandGeom.translate(0, -shaftLength - 1.2, 0);
        const bandMat = new THREE.MeshBasicMaterial({ color: 0x9d00ff });
        const bandMesh = new THREE.Mesh(bandGeom, bandMat);
        cueGroup.add(bandMesh);

        const tipGeom = new THREE.CylinderGeometry(0.045, 0.045, 0.15, 16);
        tipGeom.translate(0, -0.075, 0);
        const tipMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const tipMesh = new THREE.Mesh(tipGeom, tipMat);
        cueGroup.add(tipMesh);

        const laserGeom = new THREE.CylinderGeometry(0.006, 0.006, 28.0, 8);
        laserGeom.translate(0, 14.0, 0);
        const laserMat = new THREE.MeshBasicMaterial({
            color: 0x9d00ff,
            transparent: true,
            opacity: 0.65
        });
        const laserMesh = new THREE.Mesh(laserGeom, laserMat);
        cueGroup.add(laserMesh);

        function getAimDirection() {
            const h = THREE.MathUtils.degToRad(aimingHorizontal);
            const v = THREE.MathUtils.degToRad(aimingVertical);
            return new THREE.Vector3(
                Math.cos(v) * Math.sin(h),
                Math.sin(v),
                Math.cos(v) * Math.cos(h)
            );
        }

        function updateCuePlacement() {
            if (cueBall.userData.sunk) {
                cueGroup.visible = false;
                return;
            }
            cueGroup.visible = true;

            let dir;
            let basePos = new THREE.Vector3();
            const ballsStopped = balls.every(ball => ball.userData.sunk || ball.userData.velocity.lengthSq() === 0);

            if (strikeState !== "idle") {
                if (!isCueLocked) {
                    cueAnchorPosition.copy(cueBall.position);
                    cueAnchorDirection.copy(getAimDirection());
                    isCueLocked = true;
                }
            } else {
                if (ballsStopped) {
                    isCueLocked = false;
                }
            }

            if (isCueLocked) {
                dir = cueAnchorDirection.clone();
                basePos.copy(cueAnchorPosition);
            } else {
                dir = getAimDirection();
                basePos.copy(cueBall.position);
            }
            
            if (strikeState === "pullback") {
                cueOffset = (strikePower / 100) * 2.3 * pullbackProgress;
            } else if (strikeState === "release") {
                cueOffset = (strikePower / 100) * 2.3 * (1 - releaseProgress) - 0.4 * releaseProgress;
            } else if (strikeState === "recoil") {
                cueOffset = -0.4 * (1 - recoilProgress);
            } else {
                cueOffset = 0;
            }

            const cueDistance = ballRadius + 0.12 + cueOffset;
            cueGroup.position.copy(basePos).addScaledVector(dir, -cueDistance);
            cueGroup.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);

            if (strikeState === "pullback") {
                laserMesh.material.color.setHex(0xff5500);
                laserMesh.material.opacity = 0.3 + 0.7 * pullbackProgress;
                laserMesh.scale.x = 1.0 + pullbackProgress * 1.8;
            } else {
                laserMesh.material.color.setHex(0x9d00ff);
                laserMesh.material.opacity = 0.65;
                laserMesh.scale.x = 1.0;
            }
        }

        function triggerStrike() {
            if (cueBall.userData.sunk || isGameOver || strikeState !== "idle") return;
            strikeState = "pullback";
            pullbackProgress = 0;
            playSciFiSound('laser');
        }

        function executeBallStrike() {
            const dir = getAimDirection();
            const magnitude = (strikePower / 100) * 1.15;
            cueBall.userData.velocity.add(dir.multiplyScalar(magnitude));
            shotsCount++;
            document.getElementById('hud-shots').innerText = shotsCount;
            playSciFiSound('clack');
        }

        const railElasticity = 0.90;
        const ballElasticity = 0.96;
        const dragCoefficient = 0.990;

        function checkWallCollisions(ball) {
            const v = ball.userData.velocity;
            const p = ball.position;
            const r = ballRadius;
            let hit = false;

            if (p.x + r > hw) { p.x = hw - r; v.x *= -railElasticity; hit = true; }
            else if (p.x - r < -hw) { p.x = -hw + r; v.x *= -railElasticity; hit = true; }

            if (p.y + r > hh) { p.y = hh - r; v.y *= -railElasticity; hit = true; }
            else if (p.y - r < -hh) { p.y = -hh + r; v.y *= -railElasticity; hit = true; }

            if (p.z + r > hd) { p.z = hd - r; v.z *= -railElasticity; hit = true; }
            else if (p.z - r < -hd) { p.z = -hd + r; v.z *= -railElasticity; hit = true; }

            if (hit && v.length() > 0.05) {
                playSciFiSound('thud');
            }
        }

        function resolveBallCollision(ball1, ball2) {
            const delta = new THREE.Vector3().subVectors(ball1.position, ball2.position);
            const distance = delta.length();
            const minDistance = ballRadius * 2;

            if (distance < minDistance) {
                const overlap = minDistance - distance;
                const direction = delta.clone().normalize();
                const correction = direction.clone().multiplyScalar(overlap / 2);
                
                ball1.position.add(correction);
                ball2.position.sub(correction);

                const relativeVelocity = new THREE.Vector3().subVectors(ball1.userData.velocity, ball2.userData.velocity);
                const speed = relativeVelocity.dot(direction);

                if (speed > 0) return; 

                const impulse = direction.clone().multiplyScalar(-(1 + ballElasticity) * speed / 2);
                ball1.userData.velocity.add(impulse);
                ball2.userData.velocity.sub(impulse);

                if (Math.abs(speed) > 0.02) {
                    playSciFiSound('clack');
                }
            }
        }

        function checkPocketing() {
            balls.forEach(ball => {
                if (ball.userData.sunk) return;
                pockets.forEach(pocket => {
                    const dist = ball.position.distanceTo(pocket.position);
                    if (dist <= (pocketRadius + ballRadius)) {
                        ball.userData.sunk = true;
                        ball.userData.pocketTarget = pocket.position.clone();
                        playSciFiSound('pocket');
                    }
                });
            });
        }

        function handleFullySunk(ball) {
            if (ball.userData.isCue) {
                showScratchAlert();
                setTimeout(() => { respawnCueBall(); }, 1800);
            } else {
                playerScore += 1000;
                
                // Determine if this was the very last target ball on the table
                const remainingTargets = balls.filter(b => !b.userData.isCue && !b.userData.sunk);
                const isLastBall = remainingTargets.length === 0;
                
                if (isLastBall) {
                    playerScore += 10000;
                }
                
                document.getElementById('hud-score').innerText = playerScore;
                playSciFiSound('reward');

                // Trigger victory condition only if ALL target balls have been sunk
                if (isLastBall) {
                    document.getElementById('hud-status').innerText = "WARPED";
                    document.getElementById('hud-status').style.color = "var(--laser-cyan)";
                    triggerVictory();
                }
            }
        }

        function showScratchAlert() {
            const p = document.getElementById('alert-panel');
            p.style.opacity = '1';
            setTimeout(() => { p.style.opacity = '0'; }, 1400);
        }

        function respawnCueBall() {
            cueBall.position.copy(cueBall.userData.initialPos);
            cueBall.userData.velocity.set(0, 0, 0);
            cueBall.scale.set(0.001, 0.001, 0.001);
            cueBall.userData.sunk = false;
            cueBall.userData.sunkProcessed = false;
            cueBall.visible = true;

            const respawnAnim = () => {
                if (cueBall.scale.x < 1.0) {
                    cueBall.scale.addScalar(0.08);
                    requestAnimationFrame(respawnAnim);
                } else {
                    cueBall.scale.set(1, 1, 1);
                }
            };
            respawnAnim();
        }

        function triggerVictory() {
            isGameOver = true;
            document.getElementById('final-shots').innerText = shotsCount;
            document.getElementById('final-score').innerText = playerScore;
            document.getElementById('victory-overlay').classList.remove('hidden');
        }

        function restartGame() {
            shotsCount = 0;
            playerScore = 0;
            isGameOver = false;
            document.getElementById('hud-shots').innerText = "0";
            document.getElementById('hud-score').innerText = "0";
            document.getElementById('hud-status').innerText = "STABLE";
            document.getElementById('hud-status').style.color = "var(--plasma-orange)";

            balls.forEach(ball => {
                ball.position.copy(ball.userData.initialPos);
                ball.userData.velocity.set(0, 0, 0);
                ball.scale.set(1, 1, 1);
                ball.userData.sunk = false;
                ball.userData.sunkProcessed = false;
                ball.visible = true;
            });

            aimingHorizontal = 45;
            aimingVertical = 15;
            isCueLocked = false;
            syncSlidersAndKnobs();
            
            document.getElementById('welcome-overlay').classList.add('hidden');
            document.getElementById('victory-overlay').classList.add('hidden');
            document.getElementById('quit-overlay').classList.add('hidden');
            document.getElementById('gameover-overlay').classList.add('hidden');
        }

        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);
            const dt = clock.getDelta();

            if (strikeState === "pullback") {
                pullbackProgress += 4.5 * dt;
                if (pullbackProgress >= 1.0) {
                    pullbackProgress = 1.0;
                    strikeState = "release";
                }
            } 
            else if (strikeState === "release") {
                releaseProgress += 19 * dt;
                if (releaseProgress >= 1.0) {
                    releaseProgress = 1.0;
                    executeBallStrike();
                    strikeState = "recoil";
                }
            } 
            else if (strikeState === "recoil") {
                recoilProgress += 5 * dt;
                if (recoilProgress >= 1.0) {
                    recoilProgress = 1.0;
                    strikeState = "idle";
                    pullbackProgress = 0;
                    releaseProgress = 0;
                    recoilProgress = 0;
                    cueOffset = 0;
                }
            }

            updateCuePlacement();

            balls.forEach(ball => {
                if (ball.userData.sunk) {
                    if (ball.scale.x > 0.05) {
                        ball.scale.multiplyScalar(0.85);
                        if (ball.userData.pocketTarget) {
                            ball.position.lerp(ball.userData.pocketTarget, 0.18);
                            ball.rotateOnWorldAxis(new THREE.Vector3(0,1,0), 0.35);
                        }
                    } else {
                        ball.scale.set(0, 0, 0);
                        ball.userData.velocity.set(0, 0, 0);
                        ball.visible = false;
                        if (!ball.userData.sunkProcessed) {
                            ball.userData.sunkProcessed = true;
                            handleFullySunk(ball);
                        }
                    }
                    return;
                }

                const v = ball.userData.velocity;
                v.multiplyScalar(dragCoefficient);
                if (v.length() < 0.003) {
                    v.set(0, 0, 0);
                }
                ball.position.add(v);
                
                if (v.lengthSq() > 0.00001) {
                    const rotAxis = new THREE.Vector3(v.z, 0, -v.x).normalize();
                    const rotAngle = v.length() / ballRadius;
                    ball.rotateOnWorldAxis(rotAxis, rotAngle);
                }

                checkWallCollisions(ball);
            });

            for (let i = 0; i < balls.length; i++) {
                if (balls[i].userData.sunk) continue;
                for (let j = i + 1; j < balls.length; j++) {
                    if (balls[j].userData.sunk) continue;
                    resolveBallCollision(balls[i], balls[j]);
                }
            }

            checkPocketing();

            pockets.forEach(pocket => {
                pocket.rotation.z += 0.015;
            });

            controls.update();
            renderer.render(scene, camera);
        }

        const joystickBoundary = document.getElementById('joystick-boundary');
        const joystickKnob = document.getElementById('joystick-knob');
        let isJoystickActive = false;
        let joystickStartPos = { x: 0, y: 0 };
        const maxRadius = 52;

        function handleJoystickMove(clientVec) {
            const dx = clientVec.x - joystickStartPos.x;
            const dy = clientVec.y - joystickStartPos.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            
            let finalX = dx;
            let finalY = dy;
            if (dist > maxRadius) {
                finalX = (dx / dist) * maxRadius;
                finalY = (dy / dist) * maxRadius;
            }

            joystickKnob.style.transform = `translate(${finalX}px, ${finalY}px)`;

            aimingHorizontal -= (finalX / maxRadius) * 2.6;
            aimingVertical -= (finalY / maxRadius) * 1.5;

            aimingVertical = Math.max(-85, Math.min(85, aimingVertical));
            aimingHorizontal = (aimingHorizontal + 360) % 360;

            syncSlidersAndKnobs();
        }

        joystickBoundary.addEventListener('touchstart', (e) => {
            isJoystickActive = true;
            joystickStartPos = { x: e.touches[0].clientX, y: e.touches[0].clientY };
            joystickKnob.style.transition = 'none';
        });

        document.addEventListener('touchmove', (e) => {
            if (!isJoystickActive) return;
            handleJoystickMove({ x: e.touches[0].clientX, y: e.touches[0].clientY });
        }, { passive: false });

        document.addEventListener('touchend', () => {
            if (!isJoystickActive) return;
            isJoystickActive = false;
            joystickKnob.style.transition = 'transform 0.15s ease';
            joystickKnob.style.transform = 'translate(0px, 0px)';
        });

        joystickBoundary.addEventListener('mousedown', (e) => {
            isJoystickActive = true;
            joystickStartPos = { x: e.clientX, y: e.clientY };
            joystickKnob.style.transition = 'none';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isJoystickActive) return;
            handleJoystickMove({ x: e.clientX, y: e.clientY });
        });

        document.addEventListener('mouseup', () => {
            if (!isJoystickActive) return;
            isJoystickActive = false;
            joystickKnob.style.transition = 'transform 0.15s ease';
            joystickKnob.style.transform = 'translate(0px, 0px)';
        });

        const powerZone = document.getElementById('power-throttle-zone');
        const powerTrack = document.getElementById('power-slider-track');
        const powerFill = document.getElementById('power-fill-bar');
        const powerHandle = document.getElementById('power-handle-indicator');
        let isPowerActive = false;

        function updatePowerFromY(clientY) {
            const rect = powerTrack.getBoundingClientRect();
            let normY = (rect.bottom - clientY) / rect.height;
            normY = Math.max(0, Math.min(1, normY));
            strikePower = Math.round(5 + normY * 95);
            syncSlidersAndKnobs();
        }

        powerZone.addEventListener('touchstart', (e) => {
            isPowerActive = true;
            updatePowerFromY(e.touches[0].clientY);
        });

        document.addEventListener('touchmove', (e) => {
            if (!isPowerActive) return;
            updatePowerFromY(e.touches[0].clientY);
        });

        document.addEventListener('touchend', () => { isPowerActive = false; });

        powerZone.addEventListener('mousedown', (e) => {
            isPowerActive = true;
            updatePowerFromY(e.clientY);
        });

        document.addEventListener('mousemove', (e) => {
            if (!isPowerActive) return;
            updatePowerFromY(e.clientY);
        });

        document.addEventListener('mouseup', () => { isPowerActive = false; });

        function syncSlidersAndKnobs() {
            const pPct = ((strikePower - 5) / 95) * 100;
            powerFill.style.height = `${pPct}%`;
            powerHandle.style.bottom = `${pPct}%`;
        }

        document.getElementById('start-game-btn').addEventListener('click', () => {
            audioCtx.resume();
            document.getElementById('welcome-overlay').classList.add('hidden');
        });

        document.getElementById('strike-btn').addEventListener('click', triggerStrike);

        document.getElementById('top-quit-btn').addEventListener('click', () => {
            document.getElementById('quit-overlay').classList.remove('hidden');
        });

        document.getElementById('cancel-quit-btn').addEventListener('click', () => {
            document.getElementById('quit-overlay').classList.add('hidden');
        });

        document.getElementById('confirm-quit-btn').addEventListener('click', () => {
            document.getElementById('quit-overlay').classList.add('hidden');
            document.getElementById('gameover-overlay').classList.remove('hidden');
            isGameOver = true;
        });

        document.getElementById('restart-gameover-btn').addEventListener('click', restartGame);
        document.getElementById('victory-restart-btn').addEventListener('click', restartGame);

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        syncSlidersAndKnobs();
        animate();
    </script>
</body>
</html>
"""

# Render the game inside Streamlit with a spacious iframe layout
components.html(game_html, height=850, scrolling=False)