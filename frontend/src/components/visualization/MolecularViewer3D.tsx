/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
import { RotateCw, ZoomIn, ZoomOut, Maximize2, Minimize2, RefreshCw, Layers, Tag, Camera, Ruler } from "lucide-react";

interface MolecularViewer3DProps {
  data: string;
  format: "sdf" | "pdb" | "xyz";
  name: string;
}

type ViewerStyle = "ballAndStick" | "stick" | "sphere" | "wireframe" | "cartoon";
type ColorTheme = "jmol" | "monochrome";

export default function MolecularViewer3D({ data, format, name }: MolecularViewer3DProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<any>(null);
  const [scriptLoaded, setScriptLoaded] = useState(() => {
    return typeof window !== "undefined" && Boolean((window as any).$3Dmol);
  });
  const [viewerStyle, setViewerStyle] = useState<ViewerStyle>(
    format === "pdb" ? "cartoon" : "ballAndStick"
  );
  const [colorTheme, setColorTheme] = useState<ColorTheme>("jmol");
  const [spinActive, setSpinActive] = useState(false);
  const [labelsActive, setLabelsActive] = useState(false);
  const [showSurface, setShowSurface] = useState(false);
  const [transparency, setTransparency] = useState(0.5);
  const [measurementMode, setMeasurementMode] = useState(false);
  const [clickedAtoms, setClickedAtoms] = useState<any[]>([]);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Apply representation style & colorscheme
  const applyStyle = useCallback((viewer: any, style: string, theme: string, surface: boolean, opacity: number) => {
    viewer.setStyle({}, {});
    
    const scheme = theme === "monochrome" ? "whiteCarbon" : "Jmol";
    
    if (style === "stick") {
      viewer.setStyle({}, { stick: { radius: 0.20, colorscheme: scheme } });
    } else if (style === "sphere") {
      viewer.setStyle({}, { sphere: { colorscheme: scheme } });
    } else if (style === "wireframe") {
      viewer.setStyle({}, { line: { colorscheme: scheme } });
    } else if (style === "ballAndStick") {
      viewer.setStyle({}, { 
        stick: { radius: 0.12, colorscheme: scheme }, 
        sphere: { scale: 0.25, colorscheme: scheme } 
      });
    } else if (style === "cartoon") {
      viewer.setStyle({ helical: true }, { cartoon: { color: theme === "monochrome" ? "#000000" : "#ff5a1f", thickness: 0.2 } });
      viewer.setStyle({ sheet: true }, { cartoon: { color: theme === "monochrome" ? "#525252" : "#27272a", thickness: 0.2 } });
      viewer.setStyle({ coil: true }, { cartoon: { color: theme === "monochrome" ? "#d4d4d4" : "#a1a1aa", thickness: 0.15 } });
      viewer.setStyle({ hetatom: true }, { stick: { radius: 0.2, colorscheme: "Jmol" } });
    }

    if (surface) {
      const $3Dmol = (window as any).$3Dmol;
      viewer.addSurface($3Dmol.SurfaceType.VDW, {
        opacity: opacity,
        color: theme === "monochrome" ? "#e5e5e5" : "spectrum"
      });
    }
  }, []);

  const addLabels = useCallback((viewer: any) => {
    viewer.removeAllLabels();
    if (format === "pdb") {
      viewer.addResLabels({ hetatom: true }, { fontColor: "black", fontSize: 10, backgroundAlpha: 0.8 });
    } else {
      viewer.addPropertyLabels("symbol", { not: { elem: "H" } }, {
        fontColor: "#000000",
        font: "monospace",
        fontSize: 10,
        showBackground: true,
        backgroundAlpha: 0.8,
        backgroundColor: "white",
        alignment: "center",
      });
    }
  }, [format]);

  // 1. Load 3Dmol.js script locally (offline-resilient)
  useEffect(() => {
    if (typeof window === "undefined") return;

    if ((window as any).$3Dmol) {
      if (!scriptLoaded) {
        queueMicrotask(() => setScriptLoaded(true));
      }
      return;
    }

    const scriptId = "aethera-3dmol-cdn";
    let script = document.getElementById(scriptId) as HTMLScriptElement;

    if (!script) {
      script = document.createElement("script");
      script.id = scriptId;
      script.src = "/js/3Dmol-min.js";
      script.async = true;
      script.onload = () => setScriptLoaded(true);
      script.onerror = (e) => console.error("Failed to load 3Dmol locally:", e);
      document.body.appendChild(script);
    } else {
      const handleLoad = () => setScriptLoaded(true);
      script.addEventListener("load", handleLoad);
      return () => script.removeEventListener("load", handleLoad);
    }
  }, [scriptLoaded]);

  // 2. Initialize viewer instance ONCE
  useEffect(() => {
    if (!scriptLoaded || !containerRef.current) return;

    const $3Dmol = (window as any).$3Dmol;
    if (!$3Dmol) return;

    if (!viewerRef.current) {
      try {
        const element = $3Dmol.$ ? $3Dmol.$(containerRef.current) : containerRef.current;
        const viewer = $3Dmol.createViewer(element, {
          backgroundColor: "#ffffff",
        });
        viewerRef.current = viewer;
        viewer.resize();
        viewer.render();
      } catch (e) {
        console.error("Failed to initialize WebGL 3Dmol viewer:", e);
      }
    }

    return () => {
      if (viewerRef.current) {
        viewerRef.current.spin(false);
      }
    };
  }, [scriptLoaded]);

  // 3. React to molecule coordinate data, styles, surfaces, transparency, and labels
  useEffect(() => {
    const viewer = viewerRef.current;
    if (!viewer || !data) return;

    const $3Dmol = (window as any).$3Dmol;
    if (!$3Dmol) return;

    try {
      viewer.clear();
      viewer.removeAllSurfaces();
      viewer.removeAllShapes();

      // Inject coordinates
      viewer.addModel(data, format);
      
      // Apply style & theme colors
      applyStyle(viewer, viewerStyle, colorTheme, showSurface, transparency);

      // Apply labels
      if (labelsActive) {
        addLabels(viewer);
      } else {
        viewer.removeAllLabels();
      }

      // Configure Measurement Mode callbacks
      if (measurementMode) {
        viewer.setClickable({}, true, (atom: any, viewerInstance: any) => {
          setClickedAtoms((prev) => {
            const next = [...prev, atom];
            if (next.length === 2) {
              const a1 = next[0];
              const a2 = next[1];
              
              // Calculate spatial distance (Å)
              const dx = a1.x - a2.x;
              const dy = a1.y - a2.y;
              const dz = a1.z - a2.z;
              const dist = Math.sqrt(dx * dx + dy * dy + dz * dz).toFixed(2);
              
              // Draw measurement line cylinder
              viewerInstance.addCylinder({
                start: { x: a1.x, y: a1.y, z: a1.z },
                end: { x: a2.x, y: a2.y, z: a2.z },
                radius: 0.05,
                color: "#ff5a1f",
                fromCap: 1,
                toCap: 1
              });
              
              // Draw label box
              viewerInstance.addLabel(`${dist} Å`, {
                position: {
                  x: (a1.x + a2.x) / 2,
                  y: (a1.y + a2.y) / 2,
                  z: (a1.z + a2.z) / 2
                },
                backgroundColor: "#000000",
                fontColor: "#ffffff",
                fontSize: 10,
                font: "sans-serif",
                backgroundAlpha: 0.9,
                showBackground: true
              });
              
              viewerInstance.render();
              return [];
            }
            return next;
          });
        });
      } else {
        viewer.setClickable({}, false, () => {});
      }

      // Orientation & Redraw
      viewer.zoomTo();
      viewer.render();
      viewer.spin(spinActive);

      setTimeout(() => {
        if (viewerRef.current) {
          viewerRef.current.resize();
          viewerRef.current.render();
        }
      }, 60);

    } catch (error) {
      console.error("Error updating WebGL 3D molecule state:", error);
    }
  }, [data, format, viewerStyle, colorTheme, showSurface, transparency, labelsActive, measurementMode, spinActive, applyStyle, addLabels]);

  const handleZoom = (factor: number) => {
    if (!viewerRef.current) return;
    viewerRef.current.zoom(factor);
    viewerRef.current.render();
  };

  const handleReset = () => {
    if (!viewerRef.current) return;
    setSpinActive(false);
    viewerRef.current.spin(false);
    viewerRef.current.zoomTo(250);
    viewerRef.current.render();
  };

  const handleScreenshot = () => {
    if (!viewerRef.current) return;
    try {
      const pngData = viewerRef.current.pngURI();
      const link = document.createElement("a");
      link.href = pngData;
      link.download = `${name.toLowerCase()}_3d_structure.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (e) {
      console.error("Failed to capture WebGL screenshot:", e);
    }
  };

  const toggleFullscreen = () => {
    const element = containerRef.current?.parentElement;
    if (!element) return;

    if (!isFullscreen) {
      if (element.requestFullscreen) element.requestFullscreen();
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  };

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
      setTimeout(() => {
        if (viewerRef.current) {
          viewerRef.current.resize();
          viewerRef.current.render();
        }
      }, 100);
    };

    document.addEventListener("fullscreenchange", handleFullscreenChange);
    return () => document.removeEventListener("fullscreenchange", handleFullscreenChange);
  }, []);

  return (
    <div className="relative w-full h-full bg-white flex flex-col group overflow-hidden">
      
      {/* 3D WebGL Canvas Area */}
      <div 
        ref={containerRef} 
        style={{ height: "450px", width: "100%", position: "relative" }}
        className="cursor-grab active:cursor-grabbing bg-white"
      >
        {!scriptLoaded && (
          <div className="absolute inset-0 flex items-center justify-center text-xs font-semibold text-neutral-400 gap-2">
            <span className="w-2 h-2 rounded-full bg-accent animate-ping" />
            Initializing atomic coordinates visualizer...
          </div>
        )}
      </div>

      {/* Control Overlay Bar */}
      <div className="border-t border-neutral-200 p-4 bg-white flex flex-col gap-3.5 z-10 text-xs">
        
        {/* Style and Theme Selector Row */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-1">
            <span className="text-[10px] uppercase tracking-widest text-neutral-400 font-bold mr-1.5">
              Style:
            </span>
            {(format === "pdb" ? ["cartoon", "stick", "sphere", "wireframe"] : ["ballAndStick", "stick", "sphere", "wireframe"]).map((style) => (
              <button
                key={style}
                onClick={() => setViewerStyle(style as ViewerStyle)}
                className={`px-2.5 py-1 text-[11px] rounded-lg border transition-all font-semibold capitalize ${
                  viewerStyle === style
                    ? "border-black bg-black text-white"
                    : "border-neutral-200 bg-white hover:border-black text-neutral-700 hover:text-black"
                }`}
              >
                {style === "ballAndStick" ? "Ball & Stick" : style === "sphere" ? "Space Filling" : style}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-1">
            <span className="text-[10px] uppercase tracking-widest text-neutral-400 font-bold mr-1.5">
              Theme:
            </span>
            {["jmol", "monochrome"].map((theme) => (
              <button
                key={theme}
                onClick={() => setColorTheme(theme as ColorTheme)}
                className={`px-2.5 py-1 text-[11px] rounded-lg border transition-all font-semibold capitalize ${
                  colorTheme === theme
                    ? "border-black bg-black text-white"
                    : "border-neutral-200 bg-white hover:border-black text-neutral-700 hover:text-black"
                }`}
              >
                {theme === "jmol" ? "Jmol Elements" : "Monochrome"}
              </button>
            ))}
          </div>
        </div>

        {/* Surfaces & Opacity controls */}
        <div className="flex flex-wrap items-center justify-between gap-3 py-2 border-y border-neutral-100">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowSurface(!showSurface)}
              className={`px-3 py-1.5 rounded-lg border font-semibold transition-all flex items-center gap-1.5 ${
                showSurface
                  ? "border-black bg-black text-white"
                  : "border-neutral-200 text-neutral-700 hover:border-black hover:text-black bg-white"
              }`}
            >
              <Layers className="h-3.5 w-3.5" />
              <span>Molecular Surface</span>
            </button>
            {showSurface && (
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-neutral-400 uppercase font-bold">Opacity:</span>
                <input
                  type="range"
                  min="0.1"
                  max="1.0"
                  step="0.05"
                  value={transparency}
                  onChange={(e) => setTransparency(parseFloat(e.target.value))}
                  className="w-20 accent-[#ff5a1f] cursor-pointer"
                />
                <span className="text-[10px] font-mono font-bold text-neutral-800">{Math.round(transparency * 100)}%</span>
              </div>
            )}
          </div>

          <button
            onClick={() => {
              setMeasurementMode(!measurementMode);
              setClickedAtoms([]);
            }}
            className={`px-3 py-1.5 rounded-lg border font-semibold transition-all flex items-center gap-1.5 ${
              measurementMode
                ? "border-black bg-black text-white font-bold"
                : "border-neutral-200 text-neutral-700 hover:border-black hover:text-black bg-white"
            }`}
            title="Measure interatomic distance (Å)"
          >
            <Ruler className={`h-3.5 w-3.5 ${measurementMode ? "text-accent" : ""}`} />
            <span>Measure Distance</span>
          </button>
        </div>

        {/* Bottom Actions Row */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setSpinActive(!spinActive)}
              className={`viewer-control-btn ${spinActive ? "border-black bg-black text-white" : ""}`}
              title="Auto-rotate molecule"
            >
              <RotateCw className={`h-3.5 w-3.5 ${spinActive ? "animate-spin text-accent" : ""}`} />
              <span>Spin</span>
            </button>

            <button
              onClick={() => setLabelsActive(!labelsActive)}
              className={`viewer-control-btn ${labelsActive ? "border-black bg-black text-white" : ""}`}
              title="Toggle atom labels"
            >
              <Tag className={`h-3.5 w-3.5 ${labelsActive ? "text-accent" : ""}`} />
              <span>Labels</span>
            </button>

            <button
              onClick={handleScreenshot}
              className="viewer-control-btn"
              title="Save PNG image capture"
            >
              <Camera className="h-3.5 w-3.5" />
              <span>Capture</span>
            </button>
          </div>

          <div className="flex items-center gap-1.5">
            <div className="flex border border-neutral-200 rounded-lg overflow-hidden">
              <button
                onClick={() => handleZoom(1.1)}
                className="p-2 bg-white hover:bg-neutral-50 text-neutral-600 hover:text-black border-r border-neutral-200 transition-colors"
                title="Zoom In"
              >
                <ZoomIn className="h-3.5 w-3.5" />
              </button>
              <button
                onClick={() => handleZoom(0.9)}
                className="p-2 bg-white hover:bg-neutral-50 text-neutral-600 hover:text-black transition-colors"
                title="Zoom Out"
              >
                <ZoomOut className="h-3.5 w-3.5" />
              </button>
            </div>

            <button
              onClick={handleReset}
              className="viewer-control-btn"
              title="Reset camera focus"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Reset</span>
            </button>

            <button
              onClick={toggleFullscreen}
              className="viewer-control-btn"
              title="Toggle fullscreen mode"
            >
              {isFullscreen ? (
                <Minimize2 className="h-3.5 w-3.5" />
              ) : (
                <Maximize2 className="h-3.5 w-3.5" />
              )}
            </button>
          </div>
        </div>

        {/* Measurement HUD banner */}
        {measurementMode && (
          <div className="bg-neutral-100 border border-neutral-200 rounded-xl p-2.5 flex items-center justify-between">
            <span className="text-[11px] text-neutral-700 font-medium flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-accent" />
              {clickedAtoms.length === 0 && "Select first atom to measure distance..."}
              {clickedAtoms.length === 1 && `First atom: ${clickedAtoms[0].elem} (${clickedAtoms[0].serial}). Select second atom...`}
            </span>
            <button 
              onClick={() => setClickedAtoms([])}
              className="text-[10px] text-neutral-500 hover:text-black font-bold uppercase tracking-wider"
            >
              Clear
            </button>
          </div>
        )}
      </div>
      
      {/* 3D Visualizer Active Badge */}
      <div className="absolute top-4 left-4 bg-white/95 border border-neutral-200 rounded-full px-3 py-1 text-[10px] font-bold tracking-wider text-black uppercase pointer-events-none shadow-xs flex items-center gap-1.5">
        <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse"></span>
        <span>WebGL 3D: {format}</span>
      </div>
    </div>
  );
}
