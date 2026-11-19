"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "../../../services/api";
import CategoryDetailView from "../../../features/categories/CategoryDetailView";
import { Layers, RefreshCw } from "lucide-react";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default function CategoryDetailPage({ params }: PageProps) {
  const { id } = React.use(params);

  const { data: category, isLoading, error } = useQuery({
    queryKey: ["category-detail", id],
    queryFn: () => apiService.getCategory(id),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-3 text-center">
        <span className="w-3 h-3 rounded-full bg-accent animate-ping" />
        <p className="text-xs font-bold uppercase tracking-wider text-neutral-400">
          Loading category records...
        </p>
      </div>
    );
  }

  if (error || !category) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-5 text-center px-6">
        <div className="w-12 h-12 rounded-2xl bg-neutral-100 border border-neutral-200 flex items-center justify-center">
          <Layers className="h-6 w-6 text-neutral-400" />
        </div>
        <div>
          <p className="text-base font-serif font-bold text-black">Category Not Found</p>
          <p className="text-xs text-neutral-400 max-w-sm mt-1">
            The requested category classification could not be loaded from the database index.
          </p>
        </div>
        <button 
          onClick={() => window.location.reload()}
          className="inline-flex items-center gap-2 text-xs border-2 border-black bg-black text-white hover:bg-neutral-800 rounded-xl px-5 py-2.5 font-bold uppercase tracking-wider transition-all shadow-xs"
        >
          <RefreshCw className="h-3.5 w-3.5 text-accent" />
          <span>Retry Connection</span>
        </button>
      </div>
    );
  }

  return <CategoryDetailView category={category} />;
}
