'use client';

import { useRef, useEffect, useState } from 'react';
import { TextLine } from '@/lib/types';

interface CanvasOverlayProps {
  imageFile: File;
  lines: TextLine[];
  showTranslation: boolean;
  canvasWidth: number;
  canvasHeight: number;
}

export function CanvasOverlay({
  imageFile,
  lines,
  showTranslation,
  canvasWidth,
  canvasHeight,
}: CanvasOverlayProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [imageSrc, setImageSrc] = useState<string>('');

  // Load image from file
  useEffect(() => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setImageSrc(e.target?.result as string);
    };
    reader.readAsDataURL(imageFile);
  }, [imageFile]);

  // Draw overlay
  useEffect(() => {
    if (!canvasRef.current || !imageSrc) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const img = new Image();
    img.onload = () => {
      // Draw original image
      ctx.drawImage(img, 0, 0, canvasWidth, canvasHeight);

      // Draw text overlays
      ctx.font = '16px sans-serif';
      ctx.fillStyle = 'rgba(255, 0, 0, 0.8)';
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
      ctx.lineWidth = 1;

      lines.forEach((line) => {
        const [x1, y1, x2, y2] = line.bbox;
        const textToShow = showTranslation ? line.translation : line.text;

        // Draw bounding box
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        // Draw text (centered in box, with background)
        const textWidth = ctx.measureText(textToShow).width;
        const textX = x1 + (x2 - x1 - textWidth) / 2;
        const textY = y1 + (y2 - y1) / 2 + 6;

        // Draw semi-transparent background
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.fillRect(
          textX - 4,
          textY - 14,
          textWidth + 8,
          18
        );

        // Draw text
        ctx.fillStyle = 'rgba(0, 0, 0, 1)';
        ctx.fillText(textToShow, textX, textY);
      });
    };
    img.src = imageSrc;
  }, [imageSrc, lines, showTranslation, canvasWidth, canvasHeight]);

  return (
    <canvas
      ref={canvasRef}
      width={canvasWidth}
      height={canvasHeight}
      className="w-full border border-gray-300 shadow-lg rounded-lg"
    />
  );
}
