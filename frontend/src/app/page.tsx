import React, { Suspense } from "react";
import HomeView from "../features/home/HomeView";

export default function Home() {
  return (
    <Suspense fallback={
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-3 text-center">
        <span className="w-3 h-3 rounded-full bg-accent animate-ping" />
        <p className="text-xs font-bold uppercase tracking-wider text-neutral-400">
          Loading molecular exploration...
        </p>
      </div>
    }>
      <HomeView />
    </Suspense>
  );
}
