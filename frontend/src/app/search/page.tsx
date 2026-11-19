"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "../../services/api";
import { Search, SlidersHorizontal, ChevronLeft, ChevronRight, CornerDownRight, Layers } from "lucide-react";

function SearchContent() {
  const searchParams = useSearchParams();

  // Get initial values from URL query string
  const initialQuery = searchParams.get("q") || "";
  const initialCategory = searchParams.get("category") || "";

  // State
  const [q, setQ] = useState(initialQuery);
  const [category, setCategory] = useState(initialCategory);
  const [subcategory, setSubcategory] = useState("");
  const [sortBy, setSortBy] = useState("name");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");
  const [page, setPage] = useState(1);
  const pageSize = 12;

  // Sync URL search params
  useEffect(() => {
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (category) params.set("category", category);
    window.history.replaceState(
      {},
      "",
      `/search?${params.toString()}`
    );
  }, [q, category]);

  // Fetch Categories for Sidebar
  const { data: categories } = useQuery({
    queryKey: ["categories-list"],
    queryFn: () => apiService.getCategories(),
  });

  // Fetch Search Results
  const { data: searchData, isLoading, isError } = useQuery({
    queryKey: ["search-results", q, category, subcategory, sortBy, sortOrder, page],
    queryFn: () =>
      apiService.searchCompoundsAdvanced(
        q,
        category,
        subcategory,
        sortBy,
        sortOrder,
        page,
        pageSize
      ),
    placeholderData: (previousData) => previousData,
  });

  const handleClearFilters = () => {
    setQ("");
    setCategory("");
    setSubcategory("");
    setSortBy("name");
    setSortOrder("asc");
    setPage(1);
  };

  const handleQChange = (val: string) => {
    setQ(val);
    setPage(1);
  };

  const handleCategoryChange = (val: string) => {
    setCategory(val);
    setPage(1);
  };

  const handleSubcategoryChange = (val: string) => {
    setSubcategory(val);
    setPage(1);
  };

  const handleSortByChange = (val: string) => {
    setSortBy(val);
    setPage(1);
  };

  const handleSortOrderChange = (val: "asc" | "desc") => {
    setSortOrder(val);
    setPage(1);
  };

  return (
    <div className="py-8 md:py-12 px-6 md:px-8 max-w-7xl mx-auto w-full">
      
      {/* Page Title */}
      <div className="border-b border-neutral-200 pb-6 mb-8">
        <div className="flex items-center gap-2 mb-2">
          <span className="w-2 h-2 rounded-full bg-accent" />
          <span className="text-xs uppercase font-bold tracking-wider text-neutral-500">Database Search</span>
        </div>
        <h1 className="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-black">Compound Index Explorer</h1>
        <p className="text-xs sm:text-sm text-neutral-500 mt-1 leading-relaxed">
          Filter chemical entities, compare physical attributes, and inspect 3D molecular conformations.
        </p>
      </div>

      {/* 2-Column Search Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        {/* Sidebar Filters */}
        <div className="lg:col-span-1 flex flex-col gap-6">
          
          {/* Filter Header */}
          <div className="flex items-center justify-between pb-2 border-b border-neutral-200">
            <span className="text-xs uppercase font-bold tracking-widest text-black flex items-center gap-2">
              <SlidersHorizontal className="h-3.5 w-3.5 text-accent" />
              Filter Controls
            </span>
            {(q || category || subcategory || sortBy !== "name" || sortOrder !== "asc") && (
              <button
                onClick={handleClearFilters}
                className="text-[10px] font-bold uppercase tracking-wider text-neutral-400 hover:text-accent transition-colors underline"
              >
                Clear All
              </button>
            )}
          </div>

          {/* Search Term Input */}
          <div className="flex flex-col gap-2">
            <label className="text-[10px] uppercase font-bold tracking-widest text-neutral-500">Search Query</label>
            <div className="relative">
              <input
                type="text"
                value={q}
                onChange={(e) => handleQChange(e.target.value)}
                placeholder="Formula, CAS, name..."
                className="w-full bg-white border-2 border-neutral-200 focus:border-black rounded-xl py-2 pl-9 pr-3 text-xs font-medium focus:outline-none transition-colors"
              />
              <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-neutral-400" />
            </div>
          </div>

          {/* Category Selection */}
          <div className="flex flex-col gap-2">
            <label className="text-[10px] uppercase font-bold tracking-widest text-neutral-500">Classification</label>
            <div className="flex flex-col gap-1 max-h-56 overflow-y-auto pr-1">
              <button
                onClick={() => handleCategoryChange("")}
                className={`text-left text-xs px-3 py-2 rounded-xl border transition-all font-semibold flex items-center justify-between ${
                  !category
                    ? "border-black bg-black text-white shadow-xs"
                    : "border-transparent bg-white text-neutral-600 hover:bg-neutral-100 hover:text-black"
                }`}
              >
                <span>All Classifications</span>
                {!category && <span className="w-1.5 h-1.5 rounded-full bg-accent" />}
              </button>
              {categories?.map((cat) => (
                <button
                  key={cat.slug}
                  onClick={() => handleCategoryChange(cat.slug)}
                  className={`text-left text-xs px-3 py-2 rounded-xl border transition-all font-semibold flex items-center justify-between ${
                    category === cat.slug
                      ? "border-black bg-black text-white shadow-xs"
                      : "border-transparent bg-white text-neutral-600 hover:bg-neutral-100 hover:text-black"
                  }`}
                >
                  <span className="truncate">{cat.name}</span>
                  {category === cat.slug && <span className="w-1.5 h-1.5 rounded-full bg-accent" />}
                </button>
              ))}
            </div>
          </div>

          {/* Subcategory selection */}
          <div className="flex flex-col gap-2">
            <label className="text-[10px] uppercase font-bold tracking-widest text-neutral-500">Subcategory</label>
            <input
              type="text"
              value={subcategory}
              onChange={(e) => handleSubcategoryChange(e.target.value)}
              placeholder="e.g. Alcohols, Purines..."
              className="w-full bg-white border-2 border-neutral-200 focus:border-black rounded-xl py-2 px-3 text-xs font-medium focus:outline-none transition-colors"
            />
          </div>

          {/* Sort By */}
          <div className="flex flex-col gap-2">
            <label className="text-[10px] uppercase font-bold tracking-widest text-neutral-500">Sort Field</label>
            <select
              value={sortBy}
              onChange={(e) => handleSortByChange(e.target.value)}
              className="w-full bg-white border-2 border-neutral-200 focus:border-black rounded-xl py-2 px-3 text-xs font-semibold focus:outline-none transition-colors cursor-pointer"
            >
              <option value="name">Alphabetical (Name)</option>
              <option value="molecular_weight">Molecular Weight</option>
              <option value="created_at">Recently Added</option>
              <option value="category">Category Classification</option>
            </select>
          </div>

          {/* Sort Direction */}
          <div className="flex flex-col gap-2">
            <label className="text-[10px] uppercase font-bold tracking-widest text-neutral-500">Direction</label>
            <div className="flex border-2 border-neutral-200 rounded-xl overflow-hidden p-0.5 bg-neutral-50">
              <button
                onClick={() => handleSortOrderChange("asc")}
                className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition-all ${
                  sortOrder === "asc" ? "bg-black text-white shadow-xs" : "text-neutral-600 hover:text-black"
                }`}
              >
                Ascending
              </button>
              <button
                onClick={() => handleSortOrderChange("desc")}
                className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition-all ${
                  sortOrder === "desc" ? "bg-black text-white shadow-xs" : "text-neutral-600 hover:text-black"
                }`}
              >
                Descending
              </button>
            </div>
          </div>

        </div>

        {/* Results Main Panel */}
        <div className="lg:col-span-3 flex flex-col gap-6">
          
          {/* Header count indicator */}
          <div className="flex items-center justify-between py-2 border-b border-neutral-200 text-xs font-semibold text-neutral-500">
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-accent" />
              {isLoading ? "Querying molecular index..." : `Found ${searchData?.total_count || 0} matching compounds`}
            </span>
            {category && categories && (
              <span className="bg-neutral-100 border border-neutral-200 text-black px-2.5 py-1 rounded-md font-bold text-[10px] uppercase tracking-wider">
                Category: {categories.find((c) => c.slug === category)?.name}
              </span>
            )}
          </div>

          {/* Loading Indicator */}
          {isLoading && (
            <div className="py-24 text-center text-xs font-bold text-neutral-400 flex items-center justify-center gap-2">
              <span className="w-2 h-2 rounded-full bg-accent animate-ping" />
              Searching molecular index database...
            </div>
          )}

          {/* Error Indicator */}
          {isError && (
            <div className="py-24 text-center text-xs font-bold text-neutral-600 border-2 border-neutral-200 rounded-3xl p-8 bg-neutral-50">
              Database connection error. Please verify backend status and retry.
            </div>
          )}

          {/* Empty state */}
          {!isLoading && !isError && searchData?.results.length === 0 && (
            <div className="py-24 border-2 border-dashed border-neutral-200 rounded-3xl flex flex-col items-center justify-center text-center p-8 bg-white">
              <div className="w-12 h-12 rounded-2xl bg-neutral-100 border border-neutral-200 flex items-center justify-center mb-4">
                <Layers className="h-6 w-6 text-neutral-400 stroke-[1.5]" />
              </div>
              <h3 className="text-sm font-bold text-black uppercase tracking-wider mb-1">No Matching Compounds</h3>
              <p className="text-xs text-neutral-500 max-w-sm leading-relaxed mb-6">
                No chemical records matched your specified query parameters. Try loosening filters or searching by partial formula.
              </p>
              <button
                onClick={handleClearFilters}
                className="px-5 py-2.5 bg-black hover:bg-neutral-800 text-white rounded-xl text-xs font-bold uppercase tracking-wider transition-all shadow-xs"
              >
                Clear All Filters
              </button>
            </div>
          )}

          {/* Results Grid */}
          {!isLoading && !isError && searchData && searchData.results.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
              {searchData.results.map((comp) => (
                <Link
                  key={comp.slug}
                  href={`/compounds/${comp.slug}`}
                  className="p-6 border-2 border-neutral-200 hover:border-black rounded-3xl bg-white hover:-translate-y-1 hover:shadow-xl transition-all duration-200 flex flex-col justify-between min-h-48 group shadow-xs"
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] uppercase tracking-wider font-bold text-neutral-400">
                        {comp.subcategory || "Compound"}
                      </span>
                      <span className="font-mono text-[10px] font-bold text-black bg-neutral-100 border border-neutral-200 px-2 py-0.5 rounded">
                        {comp.formula}
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-black group-hover:text-black truncate">
                      {comp.name}
                    </h3>
                    {comp.iupac_name && (
                      <p className="text-[11px] text-neutral-400 mt-1 truncate font-mono" title={comp.iupac_name}>
                        {comp.iupac_name}
                      </p>
                    )}
                    {comp.cas_number && (
                      <p className="text-[10px] font-mono font-semibold text-neutral-500 mt-1">
                        CAS: {comp.cas_number}
                      </p>
                    )}
                  </div>

                  <div className="border-t border-neutral-100 pt-3 mt-4 flex items-center justify-between">
                    <span className="text-[10px] font-mono text-neutral-400">
                      {comp.molecular_weight ? `${comp.molecular_weight} g/mol` : "N/A MW"}
                    </span>
                    <span className="text-xs font-bold text-black group-hover:text-accent transition-colors flex items-center gap-1">
                      Details <CornerDownRight className="h-3.5 w-3.5 group-hover:translate-x-0.5 transition-transform" />
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          )}

          {/* Pagination Controls */}
          {!isLoading && !isError && searchData && searchData.total_pages > 1 && (
            <div className="flex items-center justify-between border-t border-neutral-200 pt-6 mt-6">
              <button
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="flex items-center gap-1.5 border-2 border-neutral-200 hover:border-black disabled:border-neutral-100 disabled:opacity-40 rounded-xl px-4 py-2 text-xs font-bold uppercase tracking-wider transition-all bg-white disabled:hover:border-neutral-100"
              >
                <ChevronLeft className="h-3.5 w-3.5" />
                <span>Previous</span>
              </button>

              <span className="text-xs text-neutral-500 font-semibold font-mono">
                Page {page} of {searchData.total_pages}
              </span>

              <button
                disabled={page >= searchData.total_pages}
                onClick={() => setPage((p) => Math.min(searchData.total_pages, p + 1))}
                className="flex items-center gap-1.5 border-2 border-neutral-200 hover:border-black disabled:border-neutral-100 disabled:opacity-40 rounded-xl px-4 py-2 text-xs font-bold uppercase tracking-wider transition-all bg-white disabled:hover:border-neutral-100"
              >
                <span>Next</span>
                <ChevronRight className="h-3.5 w-3.5 text-accent" />
              </button>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-bg p-8 flex items-center justify-center font-mono text-sm text-neutral-500">Loading search interface...</div>}>
      <SearchContent />
    </Suspense>
  );
}
