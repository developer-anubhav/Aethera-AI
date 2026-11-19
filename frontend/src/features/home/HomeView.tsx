"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import SearchBar from "../../components/ui/SearchBar";
import {
  Compass, Dna, FileText, Layers, ArrowRight,
  Activity, FlaskConical, Building2, TrendingUp, ShieldCheck
} from "lucide-react";

export default function HomeView() {
  const searchParams = useSearchParams();

  // Focus search input if routed with focus query
  useEffect(() => {
    if (searchParams.get("focus") === "true") {
      const searchInput = document.getElementById("search-input");
      if (searchInput) {
        searchInput.focus();
      }
    }
  }, [searchParams]);

  const featuredMolecules = [
    { name: "Tetrahydropyran", formula: "C5H10O", weight: 86.13, slug: "tetrahydropyran", category: "Cyclic Ether" },
    { name: "Caffeine", formula: "C8H10N4O2", weight: 194.19, slug: "caffeine", category: "Purine Alkaloid" },
    { name: "ATP", formula: "C10H16N5O13P3", weight: 507.18, slug: "atp", category: "Ribonucleotide" },
    { name: "Human Lysozyme", formula: "C688H1053N209O193S10", weight: 14700.2, slug: "lysozyme", category: "Globular Hydrolase" },
    { name: "Aspirin", formula: "C9H8O4", weight: 180.16, slug: "aspirin", category: "Salicylate Drug" },
    { name: "Buckyball C60", formula: "C60", weight: 720.64, slug: "buckminsterfullerene", category: "Fullerene Nanomaterial" }
  ];

  const categoryShortcuts = [
    { name: "Organic Chemistry", slug: "organic-chemistry", count: "45,000+" },
    { name: "Inorganic Chemistry", slug: "inorganic-chemistry", count: "25,000+" },
    { name: "Proteins & Enzymes", slug: "proteins", count: "12,000+" },
    { name: "DNA & RNA", slug: "dna", count: "5,000+" },
    { name: "Drugs & Pharmacophores", slug: "drugs", count: "8,000+" },
    { name: "Nanomaterials", slug: "nanomaterials", count: "2,000+" }
  ];

  const recentDiscoveries = [
    { title: "Tetrahydropyran Synthesis Route", date: "Aug 2026", desc: "Added detailed 3D conformational rings showing the standard chair conformation of Oxane (C5H10O)." },
    { title: "Human Lysozyme Enzyme", date: "Jul 2026", desc: "Indexed the 1A8M peptide chain with active residue annotations for Muramidase (EC 3.2.1.17)." },
    { title: "Buckyball Fullerene Cage", date: "Jun 2026", desc: "Mapped the icosahedral symmetry geodesic coordinates of Buckminsterfullerene (C60 allotrope)." }
  ];

  return (
    <div className="flex flex-col min-h-[calc(100vh-16rem)] py-12 md:py-16 px-6 md:px-8 max-w-7xl mx-auto w-full bg-white">

      {/* Hero Section */}
      <div className="text-center mb-16">
        {/* Core Tagline Badge */}
        <div className="inline-flex items-center gap-2 border border-neutral-300 bg-neutral-50 px-4 py-1.5 rounded-full text-[11px] font-bold text-black tracking-wider uppercase mb-8 shadow-xs hover:border-black transition-colors">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-accent"></span>
          </span>
          <span className="font-semibold text-neutral-800">Precision Scientific Molecular Engine</span>
        </div>

        {/* Hero Header */}
        <div className="mb-6 max-w-4xl mx-auto">
          <h1 className="font-serif text-5xl sm:text-7xl md:text-8xl font-bold tracking-tight text-black mb-4">
            Aethera <span className="inline-block text-accent">AI</span>
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-neutral-600 max-w-2xl mx-auto leading-relaxed font-normal">
            Explore 100,000+ verified chemical compounds, biomolecular sequences, and crystal coordinates with real-time WebGL 3D visualizations.
          </p>
        </div>

        {/* Search Box */}
        <div className="mb-8">
          <SearchBar />
        </div>
      </div>

      {/* Database Statistics Panel (Unified Black, White & Contrast Accent) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-5 py-8 mb-20">
        {/* Stat 1: Compounds */}
        <div className="bg-black text-white p-6 rounded-2xl border-2 border-black shadow-md flex flex-col justify-between group hover:-translate-y-1 transition-all duration-200">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 rounded-xl bg-neutral-900 border border-neutral-800 flex items-center justify-center">
              <FlaskConical className="h-5 w-5 text-accent" />
            </div>
            <span className="text-[10px] font-mono uppercase tracking-widest text-neutral-400 font-bold">Catalog</span>
          </div>
          <div>
            <div className="text-3xl sm:text-4xl font-serif font-bold tracking-tight text-white">100,000+</div>
            <div className="text-[11px] uppercase tracking-wider font-semibold text-neutral-400 mt-1">Compounds Indexed</div>
          </div>
        </div>

        {/* Stat 2: Categories */}
        <div className="bg-white text-black p-6 rounded-2xl border-2 border-neutral-200 hover:border-black shadow-sm flex flex-col justify-between group hover:-translate-y-1 transition-all duration-200">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 rounded-xl bg-neutral-100 border border-neutral-200 flex items-center justify-center group-hover:bg-black group-hover:border-black transition-colors">
              <Layers className="h-5 w-5 text-black group-hover:text-accent transition-colors" />
            </div>
            <span className="text-[10px] font-mono uppercase tracking-widest text-neutral-400 font-bold">Hierarchy</span>
          </div>
          <div>
            <div className="text-3xl sm:text-4xl font-serif font-bold tracking-tight text-black flex items-center gap-1.5">
              50+
              <span className="w-2 h-2 rounded-full bg-accent" />
            </div>
            <div className="text-[11px] uppercase tracking-wider font-semibold text-neutral-500 mt-1">Scientific Categories</div>
          </div>
        </div>

        {/* Stat 3: Accuracy */}
        <div className="bg-white text-black p-6 rounded-2xl border-2 border-neutral-200 hover:border-black shadow-sm flex flex-col justify-between group hover:-translate-y-1 transition-all duration-200">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 rounded-xl bg-neutral-100 border border-neutral-200 flex items-center justify-center group-hover:bg-black group-hover:border-black transition-colors">
              <ShieldCheck className="h-5 w-5 text-black group-hover:text-accent transition-colors" />
            </div>
            <span className="text-[10px] font-mono uppercase tracking-widest text-neutral-400 font-bold">Citations</span>
          </div>
          <div>
            <div className="text-3xl sm:text-4xl font-serif font-bold tracking-tight text-black flex items-center gap-1.5">
              100%
              <span className="w-2 h-2 rounded-full bg-accent" />
            </div>
            <div className="text-[11px] uppercase tracking-wider font-semibold text-neutral-500 mt-1">Verified Reference Data</div>
          </div>
        </div>

        {/* Stat 4: Visualizations */}
        <div className="bg-black text-white p-6 rounded-2xl border-2 border-black shadow-md flex flex-col justify-between group hover:-translate-y-1 transition-all duration-200">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 rounded-xl bg-neutral-900 border border-neutral-800 flex items-center justify-center">
              <Activity className="h-5 w-5 text-accent" />
            </div>
            <span className="text-[10px] font-mono uppercase tracking-widest text-neutral-400 font-bold">WebGL</span>
          </div>
          <div>
            <div className="text-3xl sm:text-4xl font-serif font-bold tracking-tight text-white">Interactive</div>
            <div className="text-[11px] uppercase tracking-wider font-semibold text-neutral-400 mt-1">3D Coordinate Engine</div>
          </div>
        </div>
      </div>

      {/* Featured Compounds Grid */}
      <div className="mb-20">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8 pb-4 border-b border-neutral-200 gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="w-2 h-2 rounded-full bg-accent" />
              <span className="text-xs uppercase font-bold tracking-wider text-neutral-500">Curated Records</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-serif font-bold text-black tracking-tight">
              Featured Compounds
            </h2>
          </div>
          <Link
            href="/search"
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-black hover:text-accent transition-colors group"
          >
            <span>Browse Complete Index</span>
            <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredMolecules.map((mol) => (
            <Link
              key={mol.slug}
              href={`/compounds/${mol.slug}`}
              className="group relative p-6 border-2 border-neutral-200 hover:border-black rounded-2xl bg-white hover:-translate-y-1 shadow-xs hover:shadow-xl transition-all duration-200 flex flex-col justify-between min-h-50"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[10px] uppercase tracking-wider font-bold bg-neutral-100 text-neutral-700 rounded-md border border-neutral-200 group-hover:bg-neutral-50 group-hover:border-black transition-colors">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                    {mol.category}
                  </span>
                  <span className="font-mono text-xs font-bold text-neutral-500 bg-neutral-50 border border-neutral-200 px-2 py-0.5 rounded">
                    {mol.weight} g/mol
                  </span>
                </div>
                <h3 className="text-lg font-bold text-black mb-1 group-hover:text-black transition-colors">
                  {mol.name}
                </h3>
                <p className="font-mono text-xs text-neutral-500">
                  {mol.formula}
                </p>
              </div>

              <div className="flex items-center justify-between pt-4 mt-4 border-t border-neutral-100">
                <span className="text-[11px] font-semibold text-neutral-400 group-hover:text-neutral-700 transition-colors">
                  Structural Model
                </span>
                <span className="text-xs font-bold text-black group-hover:text-accent transition-colors flex items-center gap-1">
                  View 3D <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-0.5 transition-transform" />
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Explore by Category */}
      <div className="mb-20">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8 pb-4 border-b border-neutral-200 gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="w-2 h-2 rounded-full bg-accent" />
              <span className="text-xs uppercase font-bold tracking-wider text-neutral-500">Taxonomy</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-serif font-bold text-black tracking-tight">
              Explore by Classification
            </h2>
          </div>
          <Link
            href="/categories"
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-black hover:text-accent transition-colors group"
          >
            <span>All Categories</span>
            <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-5">
          {categoryShortcuts.map((cat) => (
            <Link
              key={cat.slug}
              href={`/search?category=${cat.slug}`}
              className="group p-6 border-2 border-neutral-200 hover:border-black rounded-2xl bg-white hover:-translate-y-1 hover:shadow-lg transition-all duration-200 flex flex-col justify-between"
            >
              <div>
                <div className="w-11 h-11 mb-4 rounded-xl bg-neutral-100 border border-neutral-200 flex items-center justify-center group-hover:bg-black group-hover:border-black transition-colors">
                  <Compass className="h-5 w-5 text-neutral-700 group-hover:text-accent transition-colors" />
                </div>
                <h3 className="text-base font-bold text-black mb-1">
                  {cat.name}
                </h3>
              </div>

              <div className="mt-4 pt-3 border-t border-neutral-100 flex items-center justify-between">
                <span className="inline-block px-2.5 py-0.5 text-[11px] bg-neutral-100 text-neutral-700 font-bold uppercase tracking-wider rounded-md group-hover:bg-black group-hover:text-white transition-colors">
                  {cat.count}
                </span>
                <ArrowRight className="h-4 w-4 text-neutral-300 group-hover:text-accent group-hover:translate-x-1 transition-all" />
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Two-Column Features Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 border-t border-neutral-200 pt-16">
        {/* Column 1: Capabilities */}
        <div>
          <div className="flex items-center gap-3 mb-8">
            <div className="w-12 h-12 rounded-2xl bg-black border border-black flex items-center justify-center shadow-md">
              <Building2 className="h-6 w-6 text-accent" />
            </div>
            <div>
              <h2 className="text-2xl sm:text-3xl font-serif font-bold text-black">Platform Capabilities</h2>
              <span className="text-[11px] uppercase tracking-wider text-neutral-400 font-semibold">Engineered for Research</span>
            </div>
          </div>

          <div className="flex flex-col gap-4">
            <div className="group p-6 border-2 border-neutral-200 hover:border-black bg-white rounded-2xl transition-all duration-200 hover:shadow-md">
              <div className="flex gap-4">
                <div className="shrink-0 w-11 h-11 rounded-xl bg-neutral-100 border border-neutral-200 flex items-center justify-center group-hover:bg-black group-hover:border-black transition-colors">
                  <Compass className="h-5 w-5 text-black group-hover:text-accent transition-colors" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-black mb-1 flex items-center gap-2">
                    Interactive 3D WebGL Coordinates
                  </h3>
                  <p className="text-sm text-neutral-600 leading-relaxed">
                    Rotate, zoom, toggle Space-Filling vs Stick representations, calculate interatomic distances in Ångströms, and generate crystal captures.
                  </p>
                </div>
              </div>
            </div>

            <div className="group p-6 border-2 border-neutral-200 hover:border-black bg-white rounded-2xl transition-all duration-200 hover:shadow-md">
              <div className="flex gap-4">
                <div className="shrink-0 w-11 h-11 rounded-xl bg-neutral-100 border border-neutral-200 flex items-center justify-center group-hover:bg-black group-hover:border-black transition-colors">
                  <Dna className="h-5 w-5 text-black group-hover:text-accent transition-colors" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-black mb-1 flex items-center gap-2">
                    Macromolecular & Peptide Sequences
                  </h3>
                  <p className="text-sm text-neutral-600 leading-relaxed">
                    Explore protein chains, PDB crystal structures, EC catalytic enzyme actions, and nucleic acid assemblies with verified biological taxonomies.
                  </p>
                </div>
              </div>
            </div>

            <div className="group p-6 border-2 border-neutral-200 hover:border-black bg-white rounded-2xl transition-all duration-200 hover:shadow-md">
              <div className="flex gap-4">
                <div className="shrink-0 w-11 h-11 rounded-xl bg-neutral-100 border border-neutral-200 flex items-center justify-center group-hover:bg-black group-hover:border-black transition-colors">
                  <FileText className="h-5 w-5 text-black group-hover:text-accent transition-colors" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-black mb-1 flex items-center gap-2">
                    Verified Citations & DOI References
                  </h3>
                  <p className="text-sm text-neutral-600 leading-relaxed">
                    Cross-referenced with NCBI PubChem, RCSB Protein Data Bank, and international chemical safety databases with direct DOI links.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Column 2: Recent Index Additions */}
        <div>
          <div className="flex items-center gap-3 mb-8">
            <div className="w-12 h-12 rounded-2xl bg-black border border-black flex items-center justify-center shadow-md">
              <TrendingUp className="h-6 w-6 text-accent" />
            </div>
            <div>
              <h2 className="text-2xl sm:text-3xl font-serif font-bold text-black">Recent Discoveries</h2>
              <span className="text-[11px] uppercase tracking-wider text-neutral-400 font-semibold">Live Database Updates</span>
            </div>
          </div>

          <div className="flex flex-col gap-4">
            {recentDiscoveries.map((disco, idx) => (
              <div
                key={idx}
                className="group p-6 border-2 border-neutral-200 hover:border-black bg-white rounded-2xl transition-all duration-200 hover:shadow-md"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-accent" />
                    <span className="text-xs font-mono font-bold text-neutral-500 uppercase tracking-wider">
                      Index Update
                    </span>
                  </div>
                  <span className="text-[11px] px-2.5 py-0.5 bg-black text-white font-mono font-bold uppercase tracking-wider rounded-md">
                    {disco.date}
                  </span>
                </div>
                <h3 className="text-base font-bold text-black mb-2 group-hover:text-black">
                  {disco.title}
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed">
                  {disco.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>
  );
}
