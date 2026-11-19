"use client";

import React, { useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Check, Copy, Table as TableIcon } from "lucide-react";

interface AeraMarkdownRendererProps {
  content: string;
  isStreaming?: boolean;
}

export default function AeraMarkdownRenderer({ content, isStreaming }: AeraMarkdownRendererProps) {
  return (
    <div className="aera-markdown-content text-xs sm:text-sm text-neutral-800 leading-relaxed w-full">
      <Markdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Styled headings with visual hierarchy and accent markers
          h1: ({ children, ...props }) => (
            <h1
              className="text-base sm:text-lg font-serif font-bold text-neutral-950 mt-5 mb-2.5 pb-2 border-b border-neutral-200 flex items-center gap-2"
              {...props}
            >
              <span className="w-1.5 h-4.5 rounded-full bg-accent shrink-0" />
              <span>{children}</span>
            </h1>
          ),
          h2: ({ children, ...props }) => (
            <h2
              className="text-sm sm:text-base font-serif font-bold text-neutral-900 mt-4 mb-2 pb-1.5 border-b border-neutral-200/70 flex items-center gap-2"
              {...props}
            >
              <span className="w-1.5 h-4 rounded-full bg-accent shrink-0" />
              <span>{children}</span>
            </h2>
          ),
          h3: ({ children, ...props }) => (
            <h3
              className="text-xs sm:text-sm font-bold text-neutral-900 mt-3.5 mb-1.5 flex items-center gap-2"
              {...props}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-accent shrink-0" />
              <span>{children}</span>
            </h3>
          ),
          h4: ({ children, ...props }) => (
            <h4
              className="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-neutral-500 mt-3 mb-1"
              {...props}
            >
              {children}
            </h4>
          ),

          // Paragraphs
          p: ({ children, ...props }) => (
            <p className="my-2 text-xs sm:text-[13px] text-neutral-700 leading-relaxed font-normal" {...props}>
              {children}
            </p>
          ),

          // Lists
          ul: ({ children, ...props }) => (
            <ul
              className="my-2.5 space-y-1.5 pl-5 list-disc text-xs sm:text-[13px] text-neutral-700 leading-relaxed marker:text-accent"
              {...props}
            >
              {children}
            </ul>
          ),
          ol: ({ children, ...props }) => (
            <ol
              className="my-2.5 space-y-1.5 pl-5 list-decimal text-xs sm:text-[13px] text-neutral-700 leading-relaxed marker:font-bold marker:text-neutral-900"
              {...props}
            >
              {children}
            </ol>
          ),
          li: ({ children, ...props }) => (
            <li className="leading-relaxed pl-1" {...props}>
              {children}
            </li>
          ),

          // Bold & Italic
          strong: ({ children, ...props }) => (
            <strong className="font-semibold text-neutral-950" {...props}>
              {children}
            </strong>
          ),
          em: ({ children, ...props }) => (
            <em className="italic text-neutral-800" {...props}>
              {children}
            </em>
          ),

          // Beautiful Responsive Comparison & Scientific Tables
          table: ({ children, ...props }) => (
            <div className="my-4 w-full overflow-hidden rounded-xl border border-neutral-200/90 bg-white shadow-xs">
              <div className="flex items-center justify-between px-3.5 py-2 bg-neutral-100/70 border-b border-neutral-200/80 text-[10px] font-mono font-bold uppercase tracking-wider text-neutral-600">
                <span className="flex items-center gap-1.5">
                  <TableIcon className="h-3.5 w-3.5 text-accent" />
                  <span>Comparative Matrix / Data Table</span>
                </span>
                <span className="text-[9px] text-neutral-400 normal-case hidden sm:inline">
                  Scroll horizontally if truncated
                </span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[520px] text-left text-xs border-collapse divide-y divide-neutral-200" {...props}>
                  {children}
                </table>
              </div>
            </div>
          ),
          thead: ({ children, ...props }) => (
            <thead className="bg-neutral-50/90 text-neutral-900 border-b border-neutral-200" {...props}>
              {children}
            </thead>
          ),
          tbody: ({ children, ...props }) => (
            <tbody className="divide-y divide-neutral-100 bg-white" {...props}>
              {children}
            </tbody>
          ),
          tr: ({ children, ...props }) => (
            <tr className="hover:bg-amber-50/20 transition-colors even:bg-neutral-50/35" {...props}>
              {children}
            </tr>
          ),
          th: ({ children, ...props }) => (
            <th
              className="px-4 py-3 text-[11px] font-bold text-neutral-900 uppercase tracking-wider whitespace-nowrap bg-neutral-100/50"
              {...props}
            >
              {children}
            </th>
          ),
          td: ({ children, ...props }) => (
            <td
              className="px-4 py-2.5 text-xs text-neutral-700 leading-relaxed align-top first:font-semibold first:text-neutral-950 first:bg-neutral-50/60 first:whitespace-nowrap first:border-r first:border-neutral-100/80 break-words"
              {...props}
            >
              {children}
            </td>
          ),

          // Code blocks & Inline Code (Identifiers, Formulas, SMILES, InChI)
          code: ({ className, children, ...props }: React.HTMLAttributes<HTMLElement> & { inline?: boolean }) => {
            const match = /language-(\w+)/.exec(className || "");
            const isBlock = match || String(children).includes("\n");

            if (isBlock) {
              return (
                <div className="my-3 rounded-xl border border-neutral-800 bg-neutral-950 text-neutral-100 overflow-hidden shadow-xs">
                  <div className="flex items-center justify-between px-3.5 py-1.5 bg-neutral-900 border-b border-neutral-800 text-[10px] text-neutral-400 font-mono">
                    <span>{match ? match[1].toUpperCase() : "IDENTIFIER / CODE"}</span>
                    <CopyCodeButton text={String(children).replace(/\n$/, "")} />
                  </div>
                  <pre className="p-3.5 text-xs font-mono overflow-x-auto leading-relaxed text-neutral-200">
                    <code className={className} {...props}>
                      {children}
                    </code>
                  </pre>
                </div>
              );
            }

            return (
              <code
                className="px-1.5 py-0.5 mx-0.5 rounded-md bg-neutral-100 border border-neutral-200/80 text-neutral-900 font-mono text-[11px] font-medium break-all"
                {...props}
              >
                {children}
              </code>
            );
          },

          // Quotes & Callouts
          blockquote: ({ children, ...props }) => (
            <blockquote
              className="my-3 border-l-3 border-accent bg-accent/5 rounded-r-xl px-4 py-2.5 text-xs sm:text-[13px] text-neutral-800 italic"
              {...props}
            >
              {children}
            </blockquote>
          ),

          // Divider
          hr: ({ ...props }) => <hr className="my-4 border-t border-neutral-200/80" {...props} />,

          // Links
          a: ({ children, href, ...props }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent hover:text-accent-dark underline underline-offset-2 font-medium transition-colors"
              {...props}
            >
              {children}
            </a>
          ),
        }}
      >
        {content}
      </Markdown>

      {/* Streaming cursor */}
      {isStreaming && (
        <span className="inline-flex items-center ml-1 text-accent animate-pulse font-bold text-sm">
          ●
        </span>
      )}
    </div>
  );
}

function CopyCodeButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  return (
    <button
      onClick={handleCopy}
      type="button"
      className="flex items-center gap-1 text-[10px] text-neutral-400 hover:text-white transition-colors cursor-pointer"
      title="Copy to clipboard"
    >
      {copied ? (
        <>
          <Check className="h-3 w-3 text-emerald-400" />
          <span className="text-emerald-400">Copied</span>
        </>
      ) : (
        <>
          <Copy className="h-3 w-3" />
          <span>Copy</span>
        </>
      )}
    </button>
  );
}
