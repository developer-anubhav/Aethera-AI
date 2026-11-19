import { create } from "zustand";

interface SearchState {
  searchQuery: string;
  recentSearches: string[];
  setSearchQuery: (query: string) => void;
  addRecentSearch: (term: string) => void;
  clearRecentSearches: () => void;
}

export const useSearchStore = create<SearchState>((set) => ({
  searchQuery: "",
  recentSearches: [],
  setSearchQuery: (query) => set({ searchQuery: query }),
  addRecentSearch: (term) =>
    set((state) => {
      const cleanTerm = term.trim();
      if (!cleanTerm) return state;
      
      // Filter out existing and keep only the last 6 unique entries
      const filtered = state.recentSearches.filter((t) => t.toLowerCase() !== cleanTerm.toLowerCase());
      return {
        recentSearches: [cleanTerm, ...filtered].slice(0, 6),
      };
    }),
  clearRecentSearches: () => set({ recentSearches: [] }),
}));
