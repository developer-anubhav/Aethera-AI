"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { CompoundDetailed } from "../../types";
import { apiService } from "../../services/api";
import MolecularViewer3D from "../../components/visualization/MolecularViewer3D";
import MolecularViewer2D from "../../components/visualization/MolecularViewer2D";
import {
  Atom, Tag, BookOpen, ShieldAlert, Sparkles, Clipboard, Check,
  ExternalLink, Layers, Scale, Warehouse, Activity, Link2, Dna, ArrowRight
} from "lucide-react";
import Link from "next/link";
import AeraChatPanel from "./AeraChatPanel";

interface CompoundDetailViewProps {
  compound: CompoundDetailed;
}

type TabType = "overview" | "identifiers" | "properties" | "safety" | "references";

export default function CompoundDetailView({ compound }: CompoundDetailViewProps) {
  const [activeTab, setActiveTab] = useState<TabType>("overview");
  const [copiedText, setCopiedText] = useState<string | null>(null);

  const copyToClipboard = (text: string, identifier: string) => {
    navigator.clipboard.writeText(text);
    setCopiedText(identifier);
    setTimeout(() => setCopiedText(null), 2000);
  };

  // Fetch related compounds in the same category for recommendation cards
  const { data: categoryData } = useQuery({
    queryKey: ["related-compounds", compound.category?.slug],
    queryFn: () => compound.category ? apiService.getCategory(compound.category.slug) : null,
    enabled: !!compound.category?.slug,
  });

  const relatedCompounds = categoryData?.compounds
    ?.filter((c) => c.slug !== compound.slug)
    ?.slice(0, 3) || [];

  const tabs: { id: TabType; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
    { id: "overview", label: "Overview & Structure", icon: Activity },
    { id: "identifiers", label: "Chemical Identifiers", icon: Link2 },
    { id: "properties", label: "Physical & Chemical Specs", icon: Scale },
    { id: "safety", label: "Safety (GHS)", icon: ShieldAlert },
    { id: "references", label: "Peer Citations", icon: BookOpen },
  ];

  return (
    <div className="py-8 md:py-12 px-6 md:px-8 bg-white max-w-7xl mx-auto w-full">

      {/* Breadcrumb Navigation */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8 pb-4 border-b border-neutral-200">
        <div className="flex items-center gap-2 text-xs text-neutral-500 font-semibold uppercase tracking-wider">
          <Link href="/" className="hover:text-black transition-colors flex items-center gap-1.5 group">
            <div className="w-5 h-5 rounded-md bg-black flex items-center justify-center">
              <Atom className="h-3 w-3 text-white" />
            </div>
            <span>Aethera</span>
          </Link>
          <span className="text-neutral-300">/</span>
          <Link href="/search" className="hover:text-black transition-colors">
            Index
          </Link>
          {compound.category && (
            <>
              <span className="text-neutral-300">/</span>
              <Link href={`/search?category=${compound.category.slug}`} className="hover:text-black transition-colors">
                {compound.category.name}
              </Link>
            </>
          )}
          <span className="text-neutral-300">/</span>
          <span className="text-black font-bold truncate max-w-50">{compound.name}</span>
        </div>

        {compound.category && (
          <Link
            href={`/search?category=${compound.category.slug}`}
            className="inline-flex items-center gap-2 px-3.5 py-1.5 bg-black text-white text-xs font-bold uppercase tracking-wider rounded-full shadow-xs hover:bg-neutral-800 transition-colors"
          >
            <span className="w-2 h-2 rounded-full bg-accent" />
            <span>{compound.category.name}</span>
          </Link>
        )}
      </div>

      {/* Compound Title Banner */}
      <div className="flex flex-col md:flex-row items-start justify-between gap-6 border-2 border-neutral-200 rounded-3xl p-6 md:p-8 mb-10 bg-white shadow-xs">
        <div>
          <div className="flex flex-wrap items-center gap-3 mb-2">
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-serif font-bold text-black tracking-tight">
              {compound.name}
            </h1>
            <span className="font-mono text-base md:text-lg font-bold bg-neutral-100 text-black border border-neutral-300 px-3 py-1 rounded-xl shadow-2xs">
              {compound.formula}
            </span>
          </div>
          <p className="text-xs text-neutral-500 font-medium flex items-center gap-2">
            <Tag className="h-3.5 w-3.5 text-accent" />
            <span className="font-mono">IUPAC: {compound.iupac_name || "N/A"}</span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          {compound.cas_number && (
            <button
              onClick={() => copyToClipboard(compound.cas_number || "", "cas")}
              className="inline-flex items-center gap-2 px-4 py-2 border-2 border-neutral-200 hover:border-black bg-white hover:bg-neutral-50 rounded-xl text-xs font-bold text-neutral-800 hover:text-black transition-all shadow-2xs group"
              title="Copy CAS registry number"
            >
              <span className="font-mono text-neutral-500 group-hover:text-black">CAS: {compound.cas_number}</span>
              {copiedText === "cas" ? (
                <Check className="h-3.5 w-3.5 text-accent" />
              ) : (
                <Clipboard className="h-3.5 w-3.5 text-neutral-400 group-hover:text-accent transition-colors" />
              )}
            </button>
          )}
        </div>
      </div>

      {/* 2-Column Split Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start pb-16">

        {/* LEFT COLUMN: Sticky 3D WebGL Canvas + 2D Skeletal Sketch */}
        <div className="lg:col-span-5 lg:sticky lg:top-24 flex flex-col gap-6">
          
          {/* 3D WebGL Canvas Container */}
          <div className="rounded-3xl overflow-hidden border-2 border-black shadow-lg bg-white">
            {compound.visualization_metadata && compound.visualization_metadata.three_d_sdf ? (
              <MolecularViewer3D
                data={compound.visualization_metadata.three_d_sdf}
                format={compound.visualization_metadata.three_d_model_type}
                name={compound.name}
              />
            ) : (
              <div className="w-full h-80 flex flex-col items-center justify-center p-6 text-neutral-400 text-sm font-medium gap-2">
                <Atom className="h-8 w-8 text-neutral-300 stroke-[1.5]" />
                <span>3D atomic coordinates not available for this record.</span>
              </div>
            )}
          </div>

          {/* 2D Skeletal Structure & Quick Specs Split */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* 2D Skeletal Sketch */}
            <div className="rounded-2xl border-2 border-neutral-200 overflow-hidden bg-white shadow-xs">
              {compound.visualization_metadata && compound.visualization_metadata.two_d_svg ? (
                <MolecularViewer2D
                  svgMarkup={compound.visualization_metadata.two_d_svg}
                  name={compound.name}
                />
              ) : (
                <div className="w-full h-full min-h-45 p-6 text-center flex items-center justify-center text-neutral-400 text-xs font-medium">
                  2D structural skeleton unavailable.
                </div>
              )}
            </div>

            {/* Quick Specs Card */}
            <div className="bg-black text-white rounded-2xl p-6 border-2 border-black shadow-md flex flex-col justify-between">
              <div>
                <h3 className="text-[10px] font-bold uppercase tracking-widest text-neutral-400 mb-4 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                  Quick Specs
                </h3>
                <div className="flex flex-col gap-3">
                  <div>
                    <span className="text-neutral-400 text-[10px] uppercase tracking-wider block font-semibold">Molecular Weight</span>
                    <span className="font-bold font-mono text-sm text-white">
                      {compound.molecular_weight ? `${compound.molecular_weight} g/mol` : "N/A"}
                    </span>
                  </div>
                  <div>
                    <span className="text-neutral-400 text-[10px] uppercase tracking-wider block font-semibold">Classification</span>
                    <span className="font-semibold text-xs text-white">
                      {compound.biomolecule || compound.protein ? "Macromolecule" : "Small Molecule"}
                    </span>
                  </div>
                  <div className="h-px bg-neutral-800 my-1" />
                  <div>
                    <span className="text-neutral-400 text-[10px] uppercase tracking-wider block font-semibold">Formula</span>
                    <span className="font-mono text-xs font-bold text-accent">
                      {compound.formula}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* RIGHT COLUMN: Tab Panel */}
        <div className="lg:col-span-7 flex flex-col gap-6">

          {/* Tab Navigation Buttons */}
          <div className="flex overflow-x-auto gap-2 pb-2 no-scrollbar border-b border-neutral-200">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider transition-all whitespace-nowrap ${
                    isActive
                      ? "bg-black text-white shadow-sm"
                      : "bg-white text-neutral-600 border border-neutral-200 hover:border-black hover:text-black"
                  }`}
                >
                  <Icon className={`h-3.5 w-3.5 ${isActive ? "text-accent" : "text-neutral-400"}`} />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* Tab Content Wrappers */}
          <div className="min-h-100 min-w-0">

            {/* TAB 1: OVERVIEW & USAGE */}
            {activeTab === "overview" && (
              <div className="flex flex-col gap-6 text-sm animate-in fade-in-50 duration-200">
                {/* Description Card */}
                <div className="bg-white p-6 rounded-2xl border-2 border-neutral-200 shadow-xs">
                  <h3 className="text-xs uppercase font-bold tracking-widest text-neutral-700 mb-3 flex items-center gap-2">
                    <Sparkles className="h-4 w-4 text-accent" />
                    Abstract Description
                  </h3>
                  <p className="text-neutral-700 leading-relaxed font-normal">
                    {compound.description || "No description cataloged for this chemical record."}
                  </p>
                </div>

                {/* Synonyms */}
                {compound.synonyms && compound.synonyms.length > 0 && (
                  <div className="bg-neutral-50 p-5 rounded-2xl border border-neutral-200">
                    <h3 className="text-[10px] uppercase font-bold tracking-widest text-neutral-500 mb-3 flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                      Known Chemical Aliases & Synonyms
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {compound.synonyms.map((s) => (
                        <span
                          key={s.id}
                          className="bg-white border border-neutral-200 text-neutral-700 rounded-lg px-2.5 py-1 text-xs font-medium shadow-2xs"
                        >
                          {s.synonym}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Biological Role */}
                {compound.biological_role && (
                  <div className="p-6 rounded-2xl border-2 border-neutral-200 bg-white">
                    <h3 className="text-xs uppercase font-bold tracking-widest text-black mb-2 flex items-center gap-2">
                      <Activity className="h-4 w-4 text-accent" />
                      Biological Activity
                    </h3>
                    <p className="text-neutral-600 leading-relaxed">
                      {compound.biological_role}
                    </p>
                  </div>
                )}

                {/* Applications & Industrial uses */}
                {(compound.applications || compound.industrial_uses) && (
                  <div className="p-6 rounded-2xl border-2 border-neutral-200 bg-white flex flex-col gap-4">
                    <h3 className="text-xs uppercase font-bold tracking-widest text-black flex items-center gap-2">
                      <Layers className="h-4 w-4 text-accent" />
                      Applications & Industrial Context
                    </h3>
                    {compound.applications && (
                      <div>
                        <span className="text-[10px] uppercase font-bold tracking-widest text-neutral-400 block mb-1">
                          Research & Biological Applications
                        </span>
                        <p className="text-neutral-600 leading-relaxed">{compound.applications}</p>
                      </div>
                    )}
                    {compound.industrial_uses && (
                      <div className="pt-3 border-t border-neutral-100">
                        <span className="text-[10px] uppercase font-bold tracking-widest text-neutral-400 block mb-1">
                          Industrial Synthesis & Production
                        </span>
                        <p className="text-neutral-600 leading-relaxed">{compound.industrial_uses}</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Storage Recommendations */}
                {compound.storage_recommendations && (
                  <div className="p-6 rounded-2xl border-2 border-neutral-200 bg-white">
                    <h3 className="text-xs uppercase font-bold tracking-widest text-black mb-2 flex items-center gap-2">
                      <Warehouse className="h-4 w-4 text-accent" />
                      Storage Protocol
                    </h3>
                    <p className="text-neutral-600 leading-relaxed">{compound.storage_recommendations}</p>
                  </div>
                )}

                {/* Macromolecular Protein Information */}
                {compound.protein && (
                  <div className="border-2 border-black rounded-2xl p-6 bg-white flex flex-col gap-4">
                    <h4 className="font-bold text-sm text-black uppercase tracking-wider flex items-center gap-2">
                      <Dna className="h-4 w-4 text-accent" />
                      Macromolecular Protein Specification
                    </h4>
                    <div className="grid grid-cols-2 gap-4 text-xs">
                      <div className="p-3 bg-neutral-50 rounded-xl border border-neutral-200">
                        <span className="text-neutral-400 text-[10px] uppercase tracking-wider block font-bold mb-1">Gene Symbol</span>
                        <span className="font-bold text-black">{compound.protein.gene_name || "N/A"}</span>
                      </div>
                      <div className="p-3 bg-neutral-50 rounded-xl border border-neutral-200">
                        <span className="text-neutral-400 text-[10px] uppercase tracking-wider block font-bold mb-1">Host Organism</span>
                        <span className="font-bold text-black">{compound.protein.organism || "N/A"}</span>
                      </div>
                      {compound.protein.pdb_id && (
                        <div className="p-3 bg-neutral-50 rounded-xl border border-neutral-200">
                          <span className="text-neutral-400 text-[10px] uppercase tracking-wider block font-bold mb-1">PDB Structural ID</span>
                          <a
                            href={`https://www.rcsb.org/structure/${compound.protein.pdb_id}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="font-mono font-bold text-black hover:text-accent inline-flex items-center gap-1"
                          >
                            <span>{compound.protein.pdb_id}</span>
                            <ExternalLink className="h-3 w-3" />
                          </a>
                        </div>
                      )}
                      {compound.protein.uniprot_id && (
                        <div className="p-3 bg-neutral-50 rounded-xl border border-neutral-200">
                          <span className="text-neutral-400 text-[10px] uppercase tracking-wider block font-bold mb-1">UniProt ID</span>
                          <a
                            href={`https://www.uniprot.org/uniprotkb/${compound.protein.uniprot_id}/entry`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="font-mono font-bold text-black hover:text-accent inline-flex items-center gap-1"
                          >
                            <span>{compound.protein.uniprot_id}</span>
                            <ExternalLink className="h-3 w-3" />
                          </a>
                        </div>
                      )}
                    </div>
                    {compound.protein.enzyme && (
                      <div className="border-t border-neutral-200 pt-4 flex flex-col gap-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-neutral-500 uppercase">Enzyme Classification (EC):</span>
                          <span className="font-mono font-bold text-black bg-neutral-100 border border-neutral-300 px-2.5 py-0.5 rounded-md">
                            {compound.protein.enzyme.ec_number || "N/A"}
                          </span>
                        </div>
                        <p className="text-neutral-600 text-xs mt-1 leading-relaxed">{compound.protein.enzyme.catalytic_activity}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: CHEMICAL IDENTIFIERS */}
            {activeTab === "identifiers" && (
              <div className="flex flex-col gap-5 text-sm animate-in fade-in-50 duration-200">
                {/* SMILES string */}
                <div className="bg-white p-6 rounded-2xl border-2 border-neutral-200 flex flex-col gap-3 shadow-xs">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-lg bg-black flex items-center justify-center">
                        <Link2 className="h-3.5 w-3.5 text-accent" />
                      </div>
                      <span className="text-xs uppercase font-bold tracking-widest text-black">
                        Canonical SMILES Notation
                      </span>
                    </div>
                    <button
                      onClick={() => copyToClipboard(compound.smiles || "N/A", "smiles")}
                      className="text-xs font-bold text-neutral-700 hover:text-black hover:bg-neutral-100 border border-neutral-200 rounded-lg px-2.5 py-1 flex items-center gap-1.5 transition-colors"
                    >
                      {copiedText === "smiles" ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-accent" />
                          <span className="text-accent">Copied</span>
                        </>
                      ) : (
                        <>
                          <Clipboard className="h-3.5 w-3.5" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="text-xs bg-neutral-50 border border-neutral-200 p-4 rounded-xl font-mono text-black overflow-x-auto whitespace-pre-wrap select-all leading-relaxed font-semibold">
                    {compound.smiles || "Not applicable / Biological macromolecule"}
                  </pre>
                </div>

                {/* InChI string */}
                <div className="bg-white p-6 rounded-2xl border-2 border-neutral-200 flex flex-col gap-3 shadow-xs">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-lg bg-black flex items-center justify-center">
                        <Link2 className="h-3.5 w-3.5 text-accent" />
                      </div>
                      <span className="text-xs uppercase font-bold tracking-widest text-black">
                        InChI / InChIKey Identifier
                      </span>
                    </div>
                    <button
                      onClick={() => copyToClipboard(compound.inchi || "N/A", "inchi")}
                      className="text-xs font-bold text-neutral-700 hover:text-black hover:bg-neutral-100 border border-neutral-200 rounded-lg px-2.5 py-1 flex items-center gap-1.5 transition-colors"
                    >
                      {copiedText === "inchi" ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-accent" />
                          <span className="text-accent">Copied</span>
                        </>
                      ) : (
                        <>
                          <Clipboard className="h-3.5 w-3.5" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="text-xs bg-neutral-50 border border-neutral-200 p-4 rounded-xl font-mono text-black overflow-x-auto whitespace-pre-wrap select-all leading-relaxed font-semibold">
                    {compound.inchi || "Not applicable / Biological macromolecule"}
                  </pre>
                </div>

                {/* External Databases */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="border-2 border-neutral-200 rounded-2xl p-5 bg-white flex flex-col justify-between h-32">
                    <div>
                      <span className="text-[10px] uppercase tracking-wider font-bold text-neutral-400 block mb-1">
                        PubChem Database
                      </span>
                      <h4 className="text-xs font-bold text-black">PubChem Compound ID (CID)</h4>
                    </div>
                    {compound.pubchem_cid ? (
                      <a
                        href={`https://pubchem.ncbi.nlm.nih.gov/compound/${compound.pubchem_cid}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs font-bold font-mono text-black hover:text-accent flex items-center gap-1.5 bg-neutral-50 border border-neutral-200 rounded-lg px-3 py-1.5 w-fit hover:border-black transition-colors"
                      >
                        <span>CID: {compound.pubchem_cid}</span>
                        <ExternalLink className="h-3 w-3 text-neutral-400" />
                      </a>
                    ) : (
                      <span className="text-xs text-neutral-400">Not indexed</span>
                    )}
                  </div>

                  <div className="border-2 border-neutral-200 rounded-2xl p-5 bg-white flex flex-col justify-between h-32">
                    <div>
                      <span className="text-[10px] uppercase tracking-wider font-bold text-neutral-400 block mb-1">
                        ChEBI Index
                      </span>
                      <h4 className="text-xs font-bold text-black">ChEBI Chemical Ontology</h4>
                    </div>
                    {compound.chebi_id ? (
                      <a
                        href={`https://www.ebi.ac.uk/chebi/searchId.do?chebiId=${compound.chebi_id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs font-bold font-mono text-black hover:text-accent flex items-center gap-1.5 bg-neutral-50 border border-neutral-200 rounded-lg px-3 py-1.5 w-fit hover:border-black transition-colors"
                      >
                        <span>ID: {compound.chebi_id}</span>
                        <ExternalLink className="h-3 w-3 text-neutral-400" />
                      </a>
                    ) : (
                      <span className="text-xs text-neutral-400">Not indexed</span>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* TAB 3: PHYSICAL & CHEMICAL PROPERTIES */}
            {activeTab === "properties" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm animate-in fade-in-50 duration-200">
                {/* Physical Specifications */}
                <div className="bg-white p-6 rounded-2xl border-2 border-neutral-200 shadow-xs">
                  <div className="flex items-center gap-3 mb-5 border-b border-neutral-200 pb-4">
                    <div className="w-9 h-9 rounded-xl bg-black flex items-center justify-center">
                      <Scale className="h-4 w-4 text-accent" />
                    </div>
                    <div>
                      <h3 className="text-xs uppercase font-bold tracking-widest text-black">Physical Metrics</h3>
                      <p className="text-[10px] text-neutral-400 font-semibold">Macroscopic Observations</p>
                    </div>
                  </div>
                  {compound.physical_properties ? (
                    <div className="flex flex-col gap-3">
                      <div className="flex items-center justify-between border-b border-neutral-100 pb-2.5">
                        <span className="text-xs text-neutral-500 font-medium">Appearance</span>
                        <span className="text-xs font-bold text-black">{compound.physical_properties.appearance || "N/A"}</span>
                      </div>
                      <div className="flex items-center justify-between border-b border-neutral-100 pb-2.5">
                        <span className="text-xs text-neutral-500 font-medium">Melting Point</span>
                        <span className="text-xs font-mono font-bold text-black">{compound.physical_properties.melting_point || "N/A"}</span>
                      </div>
                      <div className="flex items-center justify-between border-b border-neutral-100 pb-2.5">
                        <span className="text-xs text-neutral-500 font-medium">Boiling Point</span>
                        <span className="text-xs font-mono font-bold text-black">{compound.physical_properties.boiling_point || "N/A"}</span>
                      </div>
                      <div className="flex items-center justify-between border-b border-neutral-100 pb-2.5">
                        <span className="text-xs text-neutral-500 font-medium">Density</span>
                        <span className="text-xs font-mono font-bold text-black">{compound.physical_properties.density || "N/A"}</span>
                      </div>
                      <div className="flex items-center justify-between pt-1">
                        <span className="text-xs text-neutral-500 font-medium">Solubility</span>
                        <span className="text-xs font-semibold text-black text-right max-w-45">{compound.physical_properties.solubility || "N/A"}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-xs text-neutral-500">Physical metrics are not cataloged for this record.</p>
                  )}
                </div>

                {/* Chemical Specifications */}
                <div className="bg-white p-6 rounded-2xl border-2 border-neutral-200 shadow-xs">
                  <div className="flex items-center gap-3 mb-5 border-b border-neutral-200 pb-4">
                    <div className="w-9 h-9 rounded-xl bg-black flex items-center justify-center">
                      <Atom className="h-4 w-4 text-accent" />
                    </div>
                    <div>
                      <h3 className="text-xs uppercase font-bold tracking-widest text-black">Chemical Metrics</h3>
                      <p className="text-[10px] text-neutral-400 font-semibold">Bonding & Stability</p>
                    </div>
                  </div>
                  {compound.chemical_properties ? (
                    <div className="flex flex-col gap-3">
                      <div className="flex items-center justify-between border-b border-neutral-100 pb-2.5">
                        <span className="text-xs text-neutral-500 font-medium">Acidity (pKa)</span>
                        <span className="text-xs font-mono font-bold text-black">{compound.chemical_properties.acidity_pka || "N/A"}</span>
                      </div>
                      <div className="flex items-center justify-between border-b border-neutral-100 pb-2.5">
                        <span className="text-xs text-neutral-500 font-medium">Refractive Index</span>
                        <span className="text-xs font-mono font-bold text-black">{compound.chemical_properties.refractive_index || "N/A"}</span>
                      </div>
                      <div className="flex flex-col gap-1 border-b border-neutral-100 pb-2.5">
                        <span className="text-xs text-neutral-500 font-medium">Chemical Stability</span>
                        <span className="text-xs font-semibold text-neutral-800">{compound.chemical_properties.chemical_stability || "N/A"}</span>
                      </div>
                      <div className="flex flex-col gap-1 pt-1">
                        <span className="text-xs text-neutral-500 font-medium">Reactivity</span>
                        <span className="text-xs font-semibold text-neutral-800">{compound.chemical_properties.reactivity || "N/A"}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-xs text-neutral-500">Chemical metrics are not cataloged for this record.</p>
                  )}
                </div>
              </div>
            )}

            {/* TAB 4: SAFETY (GHS) */}
            {activeTab === "safety" && (
              <div className="border-2 border-neutral-200 rounded-2xl bg-white shadow-xs p-6 animate-in fade-in-50 duration-200 text-sm">
                <div className="flex items-center gap-3 mb-6 border-b border-neutral-200 pb-4">
                  <div className="w-10 h-10 rounded-xl bg-black flex items-center justify-center">
                    <ShieldAlert className="h-5 w-5 text-accent" />
                  </div>
                  <div>
                    <h3 className="text-xs uppercase font-bold tracking-widest text-black">
                      Globally Harmonized System (GHS) Hazard Ratings
                    </h3>
                    <p className="text-xs text-neutral-500">Standardized chemical safety classifications</p>
                  </div>
                </div>

                {compound.hazard ? (
                  <div className="flex flex-col gap-5">
                    <div className="bg-neutral-50 p-4 rounded-xl border border-neutral-200">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-neutral-500 block mb-2">GHS Hazard Rating</span>
                      <div className="inline-flex items-center gap-2 bg-black text-white px-3.5 py-1.5 rounded-lg text-xs font-bold">
                        <span className="w-2 h-2 rounded-full bg-accent" />
                        {compound.hazard.ghs_classification || "Not classified as hazardous"}
                      </div>
                    </div>

                    {compound.hazard.hazard_statements && compound.hazard.hazard_statements !== "None" && (
                      <div className="bg-white p-4 rounded-xl border border-neutral-200">
                        <span className="text-xs font-bold text-black uppercase tracking-wider mb-2 flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                          Hazard Statements
                        </span>
                        <p className="text-neutral-700 font-medium leading-relaxed text-xs">{compound.hazard.hazard_statements}</p>
                      </div>
                    )}

                    {compound.hazard.precautionary_statements && compound.hazard.precautionary_statements !== "None" && (
                      <div className="bg-white p-4 rounded-xl border border-neutral-200">
                        <span className="text-xs font-bold text-black uppercase tracking-wider mb-2 flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                          Precautionary Actions
                        </span>
                        <p className="text-neutral-700 font-medium leading-relaxed text-xs">{compound.hazard.precautionary_statements}</p>
                      </div>
                    )}

                    {compound.hazard.safety_equipment && (
                      <div className="border-t border-neutral-200 pt-4">
                        <span className="text-xs font-bold text-black uppercase tracking-wider mb-3 block">
                          Recommended Protective Equipment
                        </span>
                        <div className="flex flex-wrap gap-2">
                          {compound.hazard.safety_equipment.split(',').map((eq, idx) => (
                            <span key={idx} className="px-3 py-1 bg-neutral-100 text-black border border-neutral-300 rounded-lg text-xs font-semibold">
                              {eq.trim()}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <ShieldAlert className="h-10 w-10 text-neutral-300 mx-auto mb-2" />
                    <p className="text-xs text-neutral-500">GHS hazard listings are not cataloged for this chemical record.</p>
                  </div>
                )}
              </div>
            )}

            {/* TAB 5: LITERATURE REFERENCES */}
            {activeTab === "references" && (
              <div className="border-2 border-neutral-200 rounded-2xl bg-white shadow-xs p-6 animate-in fade-in-50 duration-200 text-sm">
                <div className="flex items-center gap-3 mb-6 border-b border-neutral-200 pb-4">
                  <div className="w-10 h-10 rounded-xl bg-black flex items-center justify-center">
                    <BookOpen className="h-5 w-5 text-accent" />
                  </div>
                  <div>
                    <h3 className="text-xs uppercase font-bold tracking-widest text-black">
                      Peer-Reviewed Citations & Literature
                    </h3>
                    <p className="text-xs text-neutral-500">Verified academic references and DOIs</p>
                  </div>
                </div>

                {compound.references && compound.references.length > 0 ? (
                  <ul className="flex flex-col gap-4">
                    {compound.references.map((ref, idx) => (
                      <li
                        key={ref.id}
                        className="p-5 rounded-2xl bg-white border-2 border-neutral-200 hover:border-black transition-all flex flex-col gap-3 group"
                      >
                        <div className="flex items-start gap-3">
                          <span className="w-7 h-7 rounded-lg bg-black text-white text-xs font-mono font-bold flex items-center justify-center shrink-0">
                            {idx + 1}
                          </span>
                          <p className="text-xs font-semibold text-neutral-900 leading-relaxed flex-1">
                            {ref.citation}
                          </p>
                        </div>
                        <div className="flex flex-wrap gap-2 pt-2 border-t border-neutral-100 pl-10">
                          {ref.doi && (
                            <a
                              href={`https://doi.org/${ref.doi}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1.5 px-3 py-1 bg-neutral-100 hover:bg-black hover:text-white text-neutral-800 border border-neutral-200 rounded-lg text-xs font-mono font-semibold transition-colors"
                            >
                              <ExternalLink className="h-3 w-3 text-accent" />
                              <span className="truncate">DOI: {ref.doi}</span>
                            </a>
                          )}
                          {ref.url && (
                            <a
                              href={ref.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1.5 px-3 py-1 bg-black text-white rounded-lg text-xs font-semibold hover:bg-neutral-800 transition-colors"
                            >
                              <BookOpen className="h-3 w-3 text-accent" />
                              <span>Full Publication</span>
                            </a>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-center py-8">
                    <BookOpen className="h-10 w-10 text-neutral-300 mx-auto mb-2 opacity-50" />
                    <p className="text-xs text-neutral-500">No external literature references currently linked to this record.</p>
                  </div>
                )}
              </div>
            )}

          </div>

        </div>

      </div>

      {/* Aera Intelligent Scientific Assistant */}
      <div className="mt-12">
        <AeraChatPanel compound={compound} />
      </div>

      {/* Related Compounds Section */}
      {relatedCompounds.length > 0 && (
        <div className="border-t border-neutral-200 pt-12 mt-16">
          <div className="flex items-center gap-2 mb-6">
            <span className="w-2 h-2 rounded-full bg-accent" />
            <h2 className="text-xl font-serif font-bold text-black">Related Compounds in {compound.category?.name}</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
            {relatedCompounds.map((rel) => (
              <Link
                key={rel.slug}
                href={`/compounds/${rel.slug}`}
                className="group p-5 border-2 border-neutral-200 hover:border-black rounded-2xl bg-white hover:-translate-y-1 hover:shadow-lg transition-all flex flex-col justify-between h-44 shadow-xs"
              >
                <div>
                  <span className="text-[10px] text-neutral-400 uppercase tracking-wider font-bold block mb-1">
                    {rel.subcategory || "Compound"}
                  </span>
                  <h3 className="text-base font-bold text-black group-hover:text-black truncate">
                    {rel.name}
                  </h3>
                  <p className="font-mono text-xs text-neutral-500 mt-1">
                    {rel.formula}
                  </p>
                </div>
                <div className="flex items-center justify-between pt-3 border-t border-neutral-100">
                  <span className="text-[10px] font-mono text-neutral-500">
                    {rel.molecular_weight ? `${rel.molecular_weight} g/mol` : "N/A MW"}
                  </span>
                  <span className="text-xs font-bold text-black group-hover:text-accent transition-colors flex items-center gap-1">
                    View 3D <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
