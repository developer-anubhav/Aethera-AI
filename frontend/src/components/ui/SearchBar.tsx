"use client";

import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { Search, X, History, Atom, ArrowRight } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "../../services/api";
import { useSearchStore } from "../../store/useSearchStore";
import { useDebounce } from "../../hooks/useDebounce";

interface SearchBarProps {
  className?: string;
}

export default function SearchBar({ className = "" }: SearchBarProps) {
  const router = useRouter();
  const [inputValue, setInputValue] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const debouncedSearch = useDebounce(inputValue, 200);
  const { recentSearches, addRecentSearch, clearRecentSearches } = useSearchStore();

  // Fetch search recommendations from suggestions API
  const { data: suggestions, isLoading } = useQuery({
    queryKey: ["search-suggestions", debouncedSearch],
    queryFn: () => apiService.getSearchSuggestions(debouncedSearch),
    enabled: debouncedSearch.trim().length >= 1,
  });

  // Handle clicking outside suggestions container to collapse it
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsFocused(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleSelectCompound = (slug: string, name: string) => {
    addRecentSearch(name);
    setIsFocused(false);
    setInputValue("");
    router.push(`/compounds/${slug}`);
  };

  const handleClear = () => {
    setInputValue("");
  };

  return (
    <div ref={dropdownRef} className={`relative w-full max-w-2xl mx-auto z-40 ${className}`}>
      {/* Search Input Box */}
      <div
        className={`flex items-center gap-3 bg-white border-2 rounded-2xl px-5 py-4 transition-all duration-200 ${
          isFocused
            ? "border-black ring-4 ring-accent/15 shadow-lg"
            : "border-neutral-200 hover:border-neutral-400 shadow-sm"
        }`}
      >
        <div className="shrink-0 flex items-center justify-center">
          <Search className={`h-5 w-5 transition-colors stroke-[2] ${isFocused ? "text-accent" : "text-neutral-400"}`} />
        </div>
        <input
          id="search-input"
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && inputValue.trim()) {
              addRecentSearch(inputValue);
              setIsFocused(false);
              router.push(`/search?q=${encodeURIComponent(inputValue)}`);
            }
          }}
          placeholder="Search by name, chemical formula (e.g. C8H10N4O2), CAS, or category..."
          className="flex-1 text-sm bg-transparent text-black placeholder-neutral-400 focus:outline-none font-medium"
          autoComplete="off"
        />
        {inputValue && (
          <button
            onClick={handleClear}
            className="shrink-0 text-neutral-400 hover:text-black hover:bg-neutral-100 rounded-lg p-1.5 transition-colors"
            type="button"
            aria-label="Clear search query"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Autocomplete Dropdown List */}
      {isFocused && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white border-2 border-black rounded-2xl shadow-xl overflow-hidden divide-y divide-neutral-100 z-50 animate-in fade-in-50 zoom-in-95 duration-150">
          
          {/* Case 1: Empty Input - Show Recent Searches */}
          {!inputValue && (
            <div className="p-4">
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] uppercase tracking-wider text-neutral-500 font-bold flex items-center gap-1.5">
                  <History className="h-3 w-3 text-accent" />
                  Recent Searches
                </span>
                {recentSearches.length > 0 && (
                  <button
                    onClick={clearRecentSearches}
                    className="text-[10px] uppercase font-bold text-neutral-400 hover:text-accent transition-colors"
                  >
                    Clear History
                  </button>
                )}
              </div>
              {recentSearches.length === 0 ? (
                <p className="text-xs text-neutral-400 py-2">
                  No recent searches. Enter a formula or compound name to explore molecular structures.
                </p>
              ) : (
                <div className="flex flex-col gap-1">
                  {recentSearches.map((term, index) => (
                    <button
                      key={index}
                      onClick={() => setInputValue(term)}
                      className="flex items-center justify-between text-xs text-neutral-700 hover:text-black py-2 px-3 rounded-lg hover:bg-neutral-50 transition-colors text-left group"
                    >
                      <div className="flex items-center gap-2.5">
                        <History className="h-3.5 w-3.5 text-neutral-300 group-hover:text-accent transition-colors" />
                        <span className="font-medium">{term}</span>
                      </div>
                      <ArrowRight className="h-3.5 w-3.5 text-neutral-300 opacity-0 group-hover:opacity-100 group-hover:text-black transition-all" />
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Case 2: Query Active - Show suggestions */}
          {inputValue && (
            <div className="p-2 max-h-80 overflow-y-auto">
              {isLoading && (
                <div className="p-5 text-center text-xs text-neutral-500 font-medium flex items-center justify-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
                  Searching molecular index...
                </div>
              )}

              {!isLoading && suggestions && suggestions.length === 0 && (
                <div className="p-6 text-center text-xs text-neutral-400 font-medium">
                  No molecules matched &quot;<span className="text-black font-semibold">{inputValue}</span>&quot;. Press Enter to perform an advanced database search.
                </div>
              )}

              {!isLoading && suggestions && suggestions.map((sug, index) => (
                <button
                  key={index}
                  onClick={() => handleSelectCompound(sug.slug, sug.text)}
                  className="w-full flex items-center justify-between text-left py-2.5 px-3.5 rounded-xl hover:bg-neutral-50 hover:border-black transition-all group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-neutral-100 border border-neutral-200 flex items-center justify-center group-hover:bg-black group-hover:border-black transition-all">
                      <Atom className="h-4 w-4 text-neutral-700 group-hover:text-accent transition-colors" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-black group-hover:text-black">{sug.text}</div>
                      <div className="text-[10px] text-neutral-400 mt-0.5 capitalize flex items-center gap-1.5">
                        <span className="w-1 h-1 rounded-full bg-accent" />
                        Matched by {sug.type}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {sug.formula && (
                      <span className="font-mono text-[10px] font-semibold text-neutral-700 bg-neutral-100 px-2 py-0.5 rounded border border-neutral-200">
                        {sug.formula}
                      </span>
                    )}
                    <ArrowRight className="h-4 w-4 text-neutral-300 group-hover:text-accent group-hover:translate-x-0.5 transition-all" />
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
