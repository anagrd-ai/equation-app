// Import Three.js from CDN
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.132.2/examples/jsm/controls/OrbitControls.js';

// Set up the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Create a black hole
const blackHoleGeometry = new THREE.SphereGeometry(5, 32, 32);
const blackHoleMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
const blackHole = new THREE.Mesh(blackHoleGeometry, blackHoleMaterial);
scene.add(blackHole);

// Create an accretion disk
const diskGeometry = new THREE.RingGeometry(6, 12, 64);
const diskMaterial = new THREE.MeshBasicMaterial({ 
  color: 0xffff00, 
  side: THREE.DoubleSide,
  transparent: true,
  opacity: 0.7
});
const accretionDisk = new THREE.Mesh(diskGeometry, diskMaterial);
accretionDisk.rotation.x = Math.PI / 2;
scene.add(accretionDisk);

// Add a starfield background
const starGeometry = new THREE.BufferGeometry();
const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.1 });

const starVertices = [];
for (let i = 0; i < 10000; i++) {
  const x = (Math.random() - 0.5) * 2000;
  const y = (Math.random() - 0.5) * 2000;
  const z = (Math.random() - 0.5) * 2000;
  starVertices.push(x, y, z);
}

starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
const stars = new THREE.Points(starGeometry, starMaterial);
scene.add(stars);

// Set up camera position
camera.position.z = 30;

// Add OrbitControls for mouse interaction
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Handle window resizing
window.addEventListener('resize', () => {
  const newWidth = window.innerWidth;
  const newHeight = window.innerHeight;
  camera.aspect = newWidth / newHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(newWidth, newHeight);
});

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

animate();

// Keyboard controls for zooming and panning
document.addEventListener('keydown', (event) => {
  const moveSpeed = 1;
  const zoomSpeed = 1;

  switch (event.key) {
    case 'ArrowUp':
      camera.position.y += moveSpeed;
      break;
    case 'ArrowDown':
      camera.position.y -= moveSpeed;
      break;
    case 'ArrowLeft':
      camera.position.x -= moveSpeed;
      break;
    case 'ArrowRight':
      camera.position.x += moveSpeed;
      break;
    case '+':
    case '=':
      camera.position.z -= zoomSpeed;
      break;
    case '-':
    case '_':
      camera.position.z += zoomSpeed;
      break;
  }
});
