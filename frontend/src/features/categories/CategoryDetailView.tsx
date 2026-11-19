"use client";

import React from "react";
import Link from "next/link";
import { CategoryDetailed } from "../../types";
import { ChevronLeft, ArrowRight } from "lucide-react";

interface CategoryDetailViewProps {
  category: CategoryDetailed;
}

export default function CategoryDetailView({ category }: CategoryDetailViewProps) {
  return (
    <div className="py-12 md:py-16 px-6 md:px-8">
      <div className="mx-auto max-w-7xl">
        
        {/* Back Link */}
        <Link 
          href="/categories" 
          className="inline-flex items-center gap-1.5 text-xs text-neutral-500 hover:text-black font-bold uppercase tracking-wider mb-8 transition-colors group"
        >
          <ChevronLeft className="h-4 w-4 text-neutral-400 group-hover:text-accent group-hover:-translate-x-0.5 transition-all" />
          Back to Categories
        </Link>

        {/* Category Header */}
        <div className="max-w-3xl border-b border-neutral-200 pb-8 mb-10">
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2 h-2 rounded-full bg-accent" />
            <span className="text-xs uppercase font-bold tracking-wider text-neutral-500">Classification Catalog</span>
          </div>
          <h1 className="font-serif text-4xl sm:text-5xl font-bold text-black tracking-tight mb-3">
            {category.name}
          </h1>
          <p className="text-sm sm:text-base text-neutral-600 leading-relaxed font-normal">
            {category.description || "Collection of chemical compounds, organic functional groups, and biomolecules cataloged under this index."}
          </p>
        </div>

        {/* Compound Card Grid */}
        {category.compounds.length === 0 ? (
          <div className="border-2 border-dashed border-neutral-200 rounded-3xl p-16 text-center text-sm font-semibold text-neutral-400 bg-neutral-50">
            No compounds registered under {category.name} yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {category.compounds.map((comp) => (
              <Link
                key={comp.id}
                href={`/compounds/${comp.slug}`}
                className="border-2 border-neutral-200 hover:border-black rounded-3xl p-7 bg-white hover:-translate-y-1 shadow-xs hover:shadow-xl transition-all duration-200 flex flex-col justify-between group min-h-60"
              >
                <div>
                  <div className="flex items-center justify-between gap-4 mb-4">
                    <span className="font-mono text-xs font-bold text-black bg-neutral-100 px-2.5 py-1 rounded-lg border border-neutral-200">
                      {comp.formula}
                    </span>
                    {comp.molecular_weight && (
                      <span className="font-mono text-xs font-bold text-neutral-400">
                        {comp.molecular_weight} g/mol
                      </span>
                    )}
                  </div>

                  <h2 className="text-lg font-bold text-black mb-2 group-hover:text-black">
                    {comp.name}
                  </h2>
                  <p className="text-xs text-neutral-500 leading-relaxed line-clamp-3 mb-4">
                    {comp.description || "Explore physical and chemical specifications for this molecular record."}
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-neutral-100 flex items-center justify-between text-xs font-bold uppercase tracking-wider text-neutral-500 group-hover:text-black transition-colors">
                  <span>Explore Structure</span>
                  <ArrowRight className="h-4 w-4 text-neutral-300 group-hover:text-accent group-hover:translate-x-1 transition-all" />
                </div>
              </Link>
            ))}
          </div>
        )}

      </div>
    </div>
  );
}
