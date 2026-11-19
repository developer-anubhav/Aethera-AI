"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "../../../services/api";
import CompoundDetailView from "../../../features/detail/CompoundDetailView";
import Link from "next/link";
import { ArrowLeft, Atom } from "lucide-react";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default function CompoundDetailPage({ params }: PageProps) {
  const { id } = React.use(params);

  const { data: compound, isLoading, error } = useQuery({
    queryKey: ["compound-detail", id],
    queryFn: () => apiService.getCompound(id),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div className="flex min-h-[70vh] flex-col items-center justify-center gap-3 text-center">
        <span className="w-3 h-3 rounded-full bg-accent animate-ping" />
        <p className="text-xs font-bold uppercase tracking-wider text-neutral-400">
          Loading molecular specifications & coordinates...
        </p>
      </div>
    );
  }

  if (error || !compound) {
    return (
      <div className="flex min-h-[70vh] flex-col items-center justify-center gap-6 text-center px-6">
        <div className="w-14 h-14 rounded-2xl bg-neutral-100 border border-neutral-200 flex items-center justify-center">
          <Atom className="h-7 w-7 text-neutral-400 stroke-[1.5]" />
        </div>
        <div className="flex flex-col gap-2">
          <p className="text-2xl font-serif font-bold text-black">Compound Not Found</p>
          <p className="text-xs text-neutral-500 max-w-sm leading-relaxed">
            The requested compound identifier or slug &quot;<span className="text-black font-semibold">{id}</span>&quot; is not registered in the Aethera database index.
          </p>
        </div>
        <Link 
          href="/search"
          className="inline-flex items-center gap-2 border-2 border-black bg-black text-white hover:bg-neutral-800 rounded-xl px-5 py-2.5 text-xs font-bold uppercase tracking-wider transition-all shadow-xs"
        >
          <ArrowLeft className="h-4 w-4 text-accent" />
          <span>Return to Compound Index</span>
        </Link>
      </div>
    );
  }

  return <CompoundDetailView compound={compound} />;
}
