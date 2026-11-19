import React from "react";
import Link from "next/link";
import { Atom, ArrowUpRight, GraduationCap, ShieldCheck } from "lucide-react";

export default function Footer() {
  return (
    <footer className="w-full border-t border-neutral-200 bg-neutral-50/60 py-16">
      <div className="mx-auto max-w-7xl px-6 md:px-8">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12">
          {/* Logo & Slogan */}
          <div className="md:col-span-5 flex flex-col gap-4">
            <div className="flex items-center gap-3">
              <div className="relative w-11 h-11 rounded-xl bg-black flex items-center justify-center shadow-md">
                <Atom className="h-6 w-6 text-white" />
                <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-accent ring-2 ring-white" />
              </div>
              <div>
                <span className="font-serif text-2xl font-bold tracking-tight text-black">Aethera AI</span>
                <span className="block text-[10px] uppercase tracking-widest text-neutral-400 font-semibold">
                  Precision Molecular Knowledge Platform
                </span>
              </div>
            </div>
            <p className="text-sm text-neutral-600 leading-relaxed max-w-sm mt-1">
              Explore 100,000+ chemical compounds, biomolecular structures, and enzymes with verified scientific records and interactive 3D WebGL visualizations.
            </p>
            <div className="flex items-center gap-2 mt-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white border border-neutral-200 text-[11px] font-semibold text-neutral-800 shadow-xs">
                <span className="w-2 h-2 rounded-full bg-accent animate-pulse-subtle" />
                Live Scientific Index
              </span>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="md:col-span-3 flex flex-col gap-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-black border-b border-neutral-200 pb-2 flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-accent rounded-full" />
              Navigation
            </h3>
            <ul className="flex flex-col gap-2.5">
              <li>
                <Link
                  href="/"
                  className="text-sm text-neutral-600 hover:text-black font-medium transition-colors inline-flex items-center gap-1.5 group"
                >
                  <ArrowUpRight className="h-3.5 w-3.5 text-neutral-400 group-hover:text-accent group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" />
                  Molecular Exploration
                </Link>
              </li>
              <li>
                <Link
                  href="/categories"
                  className="text-sm text-neutral-600 hover:text-black font-medium transition-colors inline-flex items-center gap-1.5 group"
                >
                  <ArrowUpRight className="h-3.5 w-3.5 text-neutral-400 group-hover:text-accent group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" />
                  Chemical Categories
                </Link>
              </li>
              <li>
                <Link
                  href="/search"
                  className="text-sm text-neutral-600 hover:text-black font-medium transition-colors inline-flex items-center gap-1.5 group"
                >
                  <ArrowUpRight className="h-3.5 w-3.5 text-neutral-400 group-hover:text-accent group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" />
                  Compound Index Search
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-sm text-neutral-600 hover:text-black font-medium transition-colors inline-flex items-center gap-1.5 group"
                >
                  <ArrowUpRight className="h-3.5 w-3.5 text-neutral-400 group-hover:text-accent group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" />
                  About Platform
                </Link>
              </li>
            </ul>
          </div>

          {/* Scientific Sources */}
          <div className="md:col-span-4 flex flex-col gap-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-black border-b border-neutral-200 pb-2 flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-accent rounded-full" />
              Scientific Reference Catalogs
            </h3>
            <p className="text-xs text-neutral-600 leading-relaxed">
              Curated and synchronized with peer-reviewed open scientific repositories:
            </p>
            <div className="flex flex-wrap gap-2 mt-1">
              <div className="px-3 py-1.5 rounded-lg bg-white border border-neutral-200 hover:border-black transition-colors flex items-center gap-2 shadow-2xs">
                <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                <span className="text-[11px] font-mono font-bold text-black uppercase tracking-wider">NCBI PubChem</span>
              </div>
              <div className="px-3 py-1.5 rounded-lg bg-white border border-neutral-200 hover:border-black transition-colors flex items-center gap-2 shadow-2xs">
                <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                <span className="text-[11px] font-mono font-bold text-black uppercase tracking-wider">RCSB PDB</span>
              </div>
              <div className="px-3 py-1.5 rounded-lg bg-white border border-neutral-200 hover:border-black transition-colors flex items-center gap-2 shadow-2xs">
                <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                <span className="text-[11px] font-mono font-bold text-black uppercase tracking-wider">CRC Handbook</span>
              </div>
            </div>
            <p className="text-[11px] text-neutral-400 mt-1">
              Coordinates rendered via GPU-accelerated WebGL molecular engines.
            </p>
          </div>
        </div>

        {/* Divider & Copyright */}
        <div className="mt-14 border-t border-neutral-200 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-neutral-500 font-medium">
            &copy; {new Date().getFullYear()} Aethera AI. All scientific database rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <span className="text-[11px] uppercase tracking-wider font-semibold text-neutral-500 flex items-center gap-1.5">
              <ShieldCheck className="h-3.5 w-3.5 text-accent" /> Open Science Standard
            </span>
            <span className="text-[11px] uppercase tracking-wider font-semibold text-neutral-500 flex items-center gap-1.5">
              <GraduationCap className="h-3.5 w-3.5 text-neutral-500" /> Academic & Research
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
