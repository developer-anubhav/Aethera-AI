"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Search, Menu, X, Compass, Layers, Info, Atom } from "lucide-react";
import { clsx } from "clsx";

export default function Header() {
  const router = useRouter();
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { name: "Explore", href: "/", icon: Compass },
    { name: "Categories", href: "/categories", icon: Layers },
    { name: "About", href: "/about", icon: Info },
  ];

  return (
    <header className="sticky top-0 z-50 w-full glass">
      <div className="mx-auto max-w-7xl px-6 md:px-8">
        <div className="flex h-18 items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="relative w-10 h-10 rounded-xl bg-black flex items-center justify-center shadow-md group-hover:scale-105 transition-transform">
                <Atom className="h-5 w-5 text-white transition-transform group-hover:rotate-12 duration-500" />
                <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-accent ring-2 ring-white" />
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5">
                  <span className="font-serif text-xl font-bold tracking-tight text-black group-hover:text-black">
                    Aethera
                  </span>
                  <span className="px-1.5 py-0.5 rounded-md bg-black text-[10px] font-mono font-bold text-white uppercase tracking-wider group-hover:bg-accent group-hover:text-white transition-colors">
                    AI
                  </span>
                </div>
                <span className="text-[10px] uppercase tracking-widest text-neutral-400 font-semibold -mt-0.5">
                  Molecular Data
                </span>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1 bg-neutral-100/70 p-1.5 rounded-full border border-neutral-200/80">
            {navItems.map((item) => {
              const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={clsx(
                    "px-4 py-1.5 text-xs font-semibold rounded-full transition-all duration-200 flex items-center gap-1.5",
                    isActive
                      ? "bg-black text-white shadow-sm"
                      : "text-neutral-600 hover:text-black hover:bg-white"
                  )}
                >
                  <item.icon className={clsx("h-3.5 w-3.5", isActive ? "text-accent" : "text-neutral-500")} />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* Search Trigger & Mobile Menu Toggle */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                const searchInput = document.getElementById("search-input");
                if (searchInput) {
                  searchInput.focus();
                } else {
                  router.push("/search");
                }
              }}
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-neutral-200 bg-white hover:border-black text-xs font-medium text-neutral-600 hover:text-black transition-all shadow-xs group"
              aria-label="Search compound index"
            >
              <Search className="h-3.5 w-3.5 text-neutral-400 group-hover:text-accent transition-colors" />
              <span className="hidden sm:inline text-neutral-500 group-hover:text-black">Quick Search...</span>
              <kbd className="hidden sm:inline-block bg-neutral-100 border border-neutral-200 text-[10px] font-mono font-semibold text-neutral-500 px-1.5 py-0.5 rounded">
                /
              </kbd>
            </button>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 md:hidden rounded-lg border border-neutral-200 bg-white text-neutral-700 hover:border-black hover:text-black transition-all"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? (
                <X className="h-5 w-5 stroke-[1.8]" />
              ) : (
                <Menu className="h-5 w-5 stroke-[1.8]" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Dropdown */}
      {mobileMenuOpen && (
        <div className="block md:hidden border-t border-neutral-200 bg-white px-6 py-4 shadow-lg animate-in slide-in-from-top-2 duration-200">
          <div className="flex flex-col gap-2">
            {navItems.map((item) => {
              const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={clsx(
                    "flex items-center gap-3 text-sm font-semibold px-4 py-2.5 rounded-xl transition-all",
                    isActive
                      ? "bg-black text-white"
                      : "text-neutral-700 hover:bg-neutral-100 hover:text-black"
                  )}
                >
                  <item.icon className={clsx("h-4 w-4", isActive ? "text-accent" : "text-neutral-400")} />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
}
