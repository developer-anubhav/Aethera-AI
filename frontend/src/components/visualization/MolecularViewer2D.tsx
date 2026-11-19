"use client";

import React from "react";

interface MolecularViewer2DProps {
  svgMarkup: string;
  name: string;
}

export default function MolecularViewer2D({ svgMarkup, name }: MolecularViewer2DProps) {
  if (!svgMarkup) {
    return (
      <div className="w-full h-full min-h-[220px] flex items-center justify-center border border-neutral-200 bg-white rounded-2xl p-6 text-neutral-400 text-xs font-semibold">
        2D skeletal structure unavailable for {name}.
      </div>
    );
  }

  return (
    <div className="relative w-full h-full min-h-[220px] bg-white border border-neutral-200 rounded-2xl flex flex-col items-center justify-center p-6 shadow-2xs overflow-hidden group">
      {/* 2D Chemical drawing container */}
      <div 
        className="w-full max-w-[190px] aspect-square flex items-center justify-center [&>svg]:w-full [&>svg]:h-full [&>svg_path]:stroke-black [&>svg_line]:stroke-black [&>svg_polygon]:stroke-black [&>svg_polygon]:fill-black [&>svg_text]:fill-black font-mono"
        dangerouslySetInnerHTML={{ __html: svgMarkup }} 
      />

      {/* Info Badge */}
      <div className="absolute top-3.5 left-3.5 bg-white/95 border border-neutral-200 rounded-full px-3 py-1 text-[10px] font-bold tracking-wider text-black uppercase pointer-events-none flex items-center gap-1.5 shadow-2xs">
        <span className="w-1.5 h-1.5 rounded-full bg-accent"></span>
        <span>2D Skeletal</span>
      </div>
    </div>
  );
}
