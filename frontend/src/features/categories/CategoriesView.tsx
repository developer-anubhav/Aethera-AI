"use client";

import React from "react";
import Link from "next/link";
import { Category } from "../../types";
import { Layers, Atom, ArrowRight } from "lucide-react";

interface CategoriesViewProps {
  categories: Category[];
}

export default function CategoriesView({ categories }: CategoriesViewProps) {
  return (
    <div className="py-12 md:py-16 px-6 md:px-8">
      <div className="mx-auto max-w-7xl">
        
        {/* Page Title & Description */}
        <div className="max-w-2xl mb-12">
          <div className="inline-flex items-center gap-2 border border-neutral-200 bg-neutral-50 px-3.5 py-1.5 rounded-full text-[11px] font-bold text-black tracking-wide uppercase mb-4 shadow-2xs">
            <span className="w-2 h-2 rounded-full bg-accent" />
            <Layers className="h-3.5 w-3.5 text-black" />
            Molecular Hierarchy
          </div>
          <h1 className="font-serif text-4xl sm:text-5xl font-bold text-black tracking-tight mb-4">
            Scientific Categories
          </h1>
          <p className="text-sm sm:text-base text-neutral-600 leading-relaxed font-normal">
            Browse through classified groupings of chemical structures, organic chains, alkaloids, biomolecules, proteins, enzymes, and genetic nucleic acids.
          </p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((cat) => (
            <Link
              key={cat.id}
              href={`/categories/${cat.slug}`}
              className="border-2 border-neutral-200 hover:border-black rounded-3xl p-7 bg-white hover:-translate-y-1 shadow-xs hover:shadow-xl transition-all duration-200 flex flex-col justify-between group min-h-60"
            >
              <div>
                <div className="w-11 h-11 rounded-2xl bg-neutral-100 border border-neutral-200 flex items-center justify-center mb-5 group-hover:bg-black group-hover:border-black transition-colors">
                  <Atom className="h-5 w-5 text-black group-hover:text-accent transition-colors" />
                </div>
                <h2 className="text-lg font-bold text-black mb-2 flex items-center gap-1.5 group-hover:text-black">
                  {cat.name}
                </h2>
                <p className="text-xs text-neutral-500 leading-relaxed line-clamp-3">
                  {cat.description || "Browse molecular records compiled and indexed under this classification catalog."}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-neutral-100 flex items-center justify-between text-xs font-bold uppercase tracking-wider text-neutral-500 group-hover:text-black transition-colors">
                <span>View Compounds</span>
                <ArrowRight className="h-4 w-4 text-neutral-300 group-hover:text-accent group-hover:translate-x-1 transition-all" />
              </div>
            </Link>
          ))}
        </div>

      </div>
    </div>
  );
}
