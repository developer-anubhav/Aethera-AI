"use client";

import React from "react";
import { Shield, Compass, BookOpen, Atom, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function AboutView() {
  const missionItems = [
    {
      title: "Reliable Scientific Data",
      description: "All records are cross-checked and integrated from certified chemistry databases and crystallographic repositories, including NCBI PubChem and the Protein Data Bank (RCSB).",
      icon: Shield
    },
    {
      title: "WebGL Atomic Exploration",
      description: "Interactive 3D molecular renders run natively in WebGL, utilizing GPU acceleration to draw bonds, labels, electron surfaces, and ribbons with zero external plugins.",
      icon: Compass
    },
    {
      title: "Open Academic Purpose",
      description: "Designed for researchers, organic chemists, pharmacology students, and biochemistry enthusiasts to look up molecular characteristics and validated properties.",
      icon: BookOpen
    }
  ];

  return (
    <div className="py-16 md:py-20 px-6 md:px-8">
      <div className="mx-auto max-w-4xl">
        
        {/* Title */}
        <div className="max-w-3xl mb-12">
          <div className="inline-flex items-center gap-2 border border-neutral-200 bg-neutral-50 px-3.5 py-1.5 rounded-full text-[11px] font-bold text-black tracking-wide uppercase mb-4 shadow-2xs">
            <span className="w-2 h-2 rounded-full bg-accent" />
            <Atom className="h-3.5 w-3.5 text-black" />
            Platform Core
          </div>
          <h1 className="font-serif text-4xl sm:text-5xl md:text-6xl font-bold text-black tracking-tight mb-4">
            About Aethera AI
          </h1>
          <p className="text-base sm:text-lg text-neutral-600 leading-relaxed font-normal">
            Aethera AI is a precision scientific compound repository engineered to enable frictionless molecular visualization, structured property cataloging, and instant citation lookups.
          </p>
        </div>

        {/* Narrative */}
        <div className="prose prose-neutral max-w-none mb-16 text-sm sm:text-base text-neutral-600 leading-relaxed flex flex-col gap-6">
          <div className="p-8 rounded-3xl border-2 border-neutral-200 bg-neutral-50/50">
            <h2 className="text-xl font-serif font-bold text-black mb-3">Bridging Data & Spatial Reality</h2>
            <p className="text-neutral-700 leading-relaxed">
              Understanding chemical structures requires spatial context. Standard flat lists of physical metrics and 2D skeletal formulas are often insufficient for visualizing complex amino acid chains, enzymes, or aromatic ring conformations. Aethera bridges this gap by merging reliable properties databases with real-time WebGL molecular coordinate rendering.
            </p>
          </div>

          <div className="p-8 rounded-3xl border-2 border-black bg-white shadow-sm">
            <h2 className="text-xl font-serif font-bold text-black mb-3">Minimalist Scientific Interface</h2>
            <p className="text-neutral-700 leading-relaxed">
              The platform is built on an editorial design philosophy: pure White, stark Black, and a high-contrast Electric Atomic Amber spark. Rather than cluttering the screen with unnecessary decorative gradients or bloated controls, Aethera highlights the atomic coordinate files and peer-reviewed scientific citations as the primary interactive medium.
            </p>
          </div>
        </div>

        {/* Pillars Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 border-t border-neutral-200 pt-16">
          {missionItems.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                className="p-6 rounded-2xl border-2 border-neutral-200 hover:border-black bg-white transition-all shadow-xs flex flex-col gap-3 group"
              >
                <div className="w-10 h-10 rounded-xl bg-black flex items-center justify-center">
                  <Icon className="h-5 w-5 text-accent" />
                </div>
                <h3 className="text-xs font-bold text-black uppercase tracking-wider">
                  {item.title}
                </h3>
                <p className="text-xs text-neutral-500 leading-relaxed">
                  {item.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* Action Link */}
        <div className="mt-14 text-center">
          <Link
            href="/search"
            className="inline-flex items-center gap-2 px-6 py-3 bg-black hover:bg-neutral-800 text-white rounded-full text-xs font-bold uppercase tracking-wider shadow-md hover:scale-105 transition-all"
          >
            <span>Explore the Compound Index</span>
            <ArrowRight className="h-4 w-4 text-accent" />
          </Link>
        </div>

      </div>
    </div>
  );
}
