'use client';
import { useState } from 'react';

export default function Gallery({ images, alt }) {
  const [i, setI] = useState(0);
  return (
    <div className="gallery">
      <div className="g-main">
        <img src={images[i]} alt={alt} width="800" height="800" fetchPriority="high" />
      </div>
      {images.length > 1 && (
        <div className="g-thumbs" role="tablist" aria-label="Product images">
          {images.map((src, n) => (
            <button key={src} role="tab" aria-selected={n === i} className={n === i ? 'on' : ''} onClick={() => setI(n)} aria-label={`Image ${n + 1}`}>
              <img src={src} alt="" width="96" height="96" loading="lazy" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
