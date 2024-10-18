// pages/index.js
import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import * as THREE from 'three';

// Plasma Effect using Three.js
const PlasmaBackground = () => {
  useEffect(() => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const geometry = new THREE.SphereGeometry(15, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    camera.position.z = 50;

    const animate = function () {
      requestAnimationFrame(animate);
      sphere.rotation.x += 0.01;
      sphere.rotation.y += 0.01;
      renderer.render(scene, camera);
    };

    animate();
    return () => {
      document.body.removeChild(renderer.domElement);
    };
  }, []);

  return null;
};

// Typing Effect for Changing Words
const TypingEffect = () => {
  const words = ["Strategy", "Insight", "Innovation", "Creativity", "Precision"];
  const [wordIndex, setWordIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setWordIndex((prevIndex) => (prevIndex + 1) % words.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <h2>
      Join our team and amplify <span style={{ color: '#7c3aed' }}>{words[wordIndex]}</span> at ZSI.ai
    </h2>
  );
};

const Home = () => {
  return (
    <>
      <Head>
        <title>ZSI Careers</title>
      </Head>
      <PlasmaBackground />
      <header style={styles.header}>
        <img src="/zsi-logo.png" alt="ZSI Logo" style={styles.logo} />
        <nav>
          <a href="#whatwedo">What we do</a>
          <a href="#careers">Careers</a>
          <a href="#contactus">Contact Us</a>
        </nav>
      </header>
      <main style={styles.mainContent}>
        <TypingEffect />
        <section>
          <h1>There’s never been a more exciting time to join us</h1>
          <p>It’s a time of incredible progress at ZSI, a time of momentum. We’re creating essential innovations for the future and working together to invent a better now.</p>
        </section>
      </main>
    </>
  );
};

const styles = {
  header: {
    background: 'black',
    color: 'white',
    display: 'flex',
    justifyContent: 'space-between',
    padding: '20px',
    alignItems: 'center',
  },
  logo: {
    height: '50px',
  },
  mainContent: {
    maxWidth: '1200px',
    margin: '0 auto',
    textAlign: 'center',
    padding: '100px 20px',
  }
};

export default Home;
