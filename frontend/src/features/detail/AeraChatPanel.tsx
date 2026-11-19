"use client";

import React, { useState, useEffect, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "../../services/api";
import { CompoundDetailed, Compound, AeraChatMetadata } from "../../types";
import { Sparkles, Send, RefreshCw, Brain, Copy, Check, Maximize2, Minimize2, FlaskConical } from "lucide-react";
import AeraMarkdownRenderer from "./AeraMarkdownRenderer";

type ExplanationLevel = "school" | "high_school" | "university" | "research" | "professional";
type StudyMode = "explain" | "compare" | "summarize" | "teach";

interface AeraChatPanelProps {
  compound: CompoundDetailed;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  metadata?: AeraChatMetadata;
}

export default function AeraChatPanel({ compound }: AeraChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [level, setLevel] = useState<ExplanationLevel>("university");
  const [mode, setMode] = useState<StudyMode>("explain");
  const [compareWithSlug, setCompareWithSlug] = useState<string>("");
  const [isExpandedView, setIsExpandedView] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch other compounds for comparison select box
  const { data: compoundsList } = useQuery<Compound[]>({
    queryKey: ["compounds-list-for-compare"],
    queryFn: () => apiService.getCompounds(),
  });

  const otherCompounds = compoundsList?.filter((c) => c.slug !== compound.slug) || [];

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const executeSend = async (questionText: string) => {
    if (!questionText.trim() || isStreaming) return;

    // Create user message
    const userMessage: ChatMessage = { role: "user", content: questionText };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setIsStreaming(true);

    // Prepare container for assistant streaming message
    const assistantMessageIndex = updatedMessages.length;
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    let streamedText = "";

    await apiService.streamAeraChat(
      {
        compound_slug: compound.slug,
        compare_with_slug: mode === "compare" && compareWithSlug ? compareWithSlug : undefined,
        question: questionText,
        messages: updatedMessages.map((m) => ({ role: m.role, content: m.content })),
        level,
        mode,
      },
      // Callback 1: chunk updates
      (chunk) => {
        streamedText += chunk;
        setMessages((prev) => {
          const next = [...prev];
          next[assistantMessageIndex] = {
            role: "assistant",
            content: streamedText,
          };
          return next;
        });
      },
      // Callback 2: final metadata package
      (metadata) => {
        setIsStreaming(false);
        setMessages((prev) => {
          const next = [...prev];
          next[assistantMessageIndex] = {
            ...next[assistantMessageIndex],
            metadata: {
              request_id: metadata.request_id,
              prompt_tokens: metadata.prompt_tokens,
              completion_tokens: metadata.completion_tokens,
              total_time_ms: metadata.total_time_ms,
              citations: metadata.citations,
            },
          };
          return next;
        });
      },
      // Callback 3: handle exception errors
      (err) => {
        setIsStreaming(false);
        console.error("Aera Streaming Error:", err);
        setMessages((prev) => {
          const next = [...prev];
          next[assistantMessageIndex] = {
            role: "assistant",
            content: `Failed to retrieve scientific data: ${err.message || "Connection timed out."}`,
          };
          return next;
        });
      }
    );
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    const text = inputValue;
    setInputValue("");
    await executeSend(text);
  };

  const handlePromptChipClick = async (chipPrompt: string, chipMode?: StudyMode) => {
    if (chipMode) setMode(chipMode);
    await executeSend(chipPrompt);
  };

  const handleClearHistory = () => {
    setMessages([]);
  };

  return (
    <div className="border-2 border-black rounded-3xl bg-white p-5 sm:p-7 md:p-8 shadow-md flex flex-col gap-6 text-sm">
      
      {/* Title & Status Header */}
      <div className="flex flex-wrap items-center justify-between border-b border-neutral-200 pb-5 gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-black flex items-center justify-center shadow-xs">
            <Brain className="h-5 w-5 text-accent" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-serif text-lg font-bold text-black tracking-tight">
                Aera Scientific AI
              </h3>
              <span className="px-2 py-0.5 rounded-full bg-neutral-100 border border-neutral-200 text-[10px] font-mono font-bold text-neutral-800">
                Grounded Engine
              </span>
            </div>
            <p className="text-[10px] text-neutral-400 font-semibold uppercase tracking-wider mt-0.5">
              Trained on IUPAC, PubChem & Crystallographic References
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          {/* Reading View Height Expander */}
          <button
            onClick={() => setIsExpandedView(!isExpandedView)}
            className="flex items-center gap-1.5 px-2.5 py-1 text-[11px] font-semibold text-neutral-600 hover:text-black rounded-lg border border-neutral-200 hover:border-black bg-white transition-all shadow-2xs"
            title={isExpandedView ? "Switch to standard height" : "Expand to larger reading canvas"}
          >
            {isExpandedView ? (
              <>
                <Minimize2 className="h-3 w-3 text-neutral-500" />
                <span>Compact View</span>
              </>
            ) : (
              <>
                <Maximize2 className="h-3 w-3 text-neutral-500" />
                <span>Reading Mode</span>
              </>
            )}
          </button>

          {messages.length > 0 && (
            <button
              onClick={handleClearHistory}
              className="text-[11px] uppercase tracking-wider font-bold text-neutral-400 hover:text-black transition-colors underline"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Interactive Controls & Filters */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 border-b border-neutral-200 pb-6">
        
        {/* Toggle Mode */}
        <div className="md:col-span-4 flex flex-col gap-1.5">
          <span className="text-[10px] uppercase font-bold tracking-widest text-neutral-500">Analysis Mode</span>
          <div className="grid grid-cols-4 gap-1 border border-neutral-200 rounded-xl p-1 bg-neutral-50">
            {[
              { id: "explain", label: "Explain" },
              { id: "compare", label: "Compare" },
              { id: "summarize", label: "Summary" },
              { id: "teach", label: "Teach" },
            ].map((m) => (
              <button
                key={m.id}
                onClick={() => setMode(m.id as StudyMode)}
                className={`py-1.5 text-[10px] font-bold rounded-lg transition-all uppercase tracking-wider ${
                  mode === m.id
                    ? "bg-black text-white shadow-xs"
                    : "text-neutral-600 hover:text-black hover:bg-white"
                }`}
              >
                {m.label}
              </button>
            ))}
          </div>
        </div>

        {/* Toggle Level */}
        <div className="md:col-span-4 flex flex-col gap-1.5">
          <span className="text-[10px] uppercase font-bold tracking-widest text-neutral-500">Academic Depth</span>
          <div className="grid grid-cols-5 gap-1 border border-neutral-200 rounded-xl p-1 bg-neutral-50">
            {[
              { id: "school", label: "School" },
              { id: "high_school", label: "H.S." },
              { id: "university", label: "Univ" },
              { id: "research", label: "Res" },
              { id: "professional", label: "Prof" },
            ].map((lvl) => (
              <button
                key={lvl.id}
                onClick={() => setLevel(lvl.id as ExplanationLevel)}
                className={`py-1.5 text-[9px] font-bold rounded-lg transition-all uppercase ${
                  level === lvl.id
                    ? "bg-black text-white shadow-xs"
                    : "text-neutral-600 hover:text-black hover:bg-white"
                }`}
                title={`Level: ${lvl.id}`}
              >
                {lvl.label}
              </button>
            ))}
          </div>
        </div>

        {/* Comparison Dropdown (If active) */}
        <div className={`md:col-span-4 flex flex-col gap-1.5 transition-all ${mode === "compare" ? "opacity-100 pointer-events-auto" : "opacity-40 pointer-events-none"}`}>
          <span className="text-[10px] uppercase font-bold tracking-widest text-neutral-500">Comparison Molecule</span>
          <select
            disabled={mode !== "compare"}
            value={compareWithSlug}
            onChange={(e) => setCompareWithSlug(e.target.value)}
            className="w-full bg-white border border-neutral-200 rounded-xl p-2 text-xs focus:outline-none focus:border-black cursor-pointer font-medium"
          >
            <option value="">-- Select Compound to Compare --</option>
            {otherCompounds.map((c) => (
              <option key={c.slug} value={c.slug}>
                {c.name} ({c.formula})
              </option>
            ))}
          </select>
        </div>

      </div>

      {/* Message Chat Logs Area with dynamic reading height */}
      <div
        className={`overflow-y-auto pr-2 flex flex-col gap-5 border border-neutral-200/90 bg-neutral-50/50 rounded-2xl p-4 sm:p-5 transition-all duration-300 ${
          isExpandedView ? "min-h-[520px] max-h-[820px]" : "min-h-[380px] max-h-[580px]"
        }`}
      >
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-6 sm:p-8 text-neutral-400 gap-4">
            <div className="w-14 h-14 rounded-2xl bg-white border border-neutral-200 flex items-center justify-center shadow-xs">
              <Sparkles className="h-7 w-7 text-accent" />
            </div>
            <div>
              <span className="text-sm font-bold uppercase tracking-wider text-black block mb-1">
                Aera Scientific Consultation
              </span>
              <p className="text-xs max-w-md text-neutral-500 leading-relaxed">
                Consult on <strong className="text-black">{compound.name}</strong> ({compound.formula}). Get comparative tables, reaction mechanisms, binding kinetics, safety profiles, or synthesis pathways.
              </p>
            </div>

            {/* Quick Suggestion Chips */}
            <div className="w-full max-w-lg mt-2 flex flex-wrap gap-2 justify-center">
              <button
                type="button"
                onClick={() =>
                  handlePromptChipClick(
                    `Provide a detailed overview of ${compound.name} with key physical, chemical, and biological properties.`,
                    "explain"
                  )
                }
                className="px-3 py-1.5 rounded-xl border border-neutral-200 bg-white hover:border-black hover:bg-neutral-50 text-neutral-700 text-[11px] font-medium transition-all shadow-2xs flex items-center gap-1.5"
              >
                <FlaskConical className="h-3 w-3 text-accent" />
                <span>Overview & Properties</span>
              </button>

              {otherCompounds.length > 0 && (
                <button
                  type="button"
                  onClick={() => {
                    const target = otherCompounds[0];
                    setCompareWithSlug(target.slug);
                    handlePromptChipClick(
                      `Generate a comparative matrix comparing ${compound.name} and ${target.name} side-by-side with differences and similarities.`,
                      "compare"
                    );
                  }}
                  className="px-3 py-1.5 rounded-xl border border-neutral-200 bg-white hover:border-black hover:bg-neutral-50 text-neutral-700 text-[11px] font-medium transition-all shadow-2xs flex items-center gap-1.5"
                >
                  <Sparkles className="h-3 w-3 text-accent" />
                  <span>Compare with {otherCompounds[0]?.name || "another molecule"}</span>
                </button>
              )}

              <button
                type="button"
                onClick={() =>
                  handlePromptChipClick(
                    `What are the typical reaction mechanisms, stability risks, and hazards for ${compound.name}?`,
                    "explain"
                  )
                }
                className="px-3 py-1.5 rounded-xl border border-neutral-200 bg-white hover:border-black hover:bg-neutral-50 text-neutral-700 text-[11px] font-medium transition-all shadow-2xs flex items-center gap-1.5"
              >
                <span>Reactivity & Safety Hazards</span>
              </button>
            </div>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`flex flex-col ${
                msg.role === "user"
                  ? "self-end items-end max-w-[85%] sm:max-w-[75%]"
                  : "w-full self-start items-start"
              }`}
            >
              {/* User Message Bubble */}
              {msg.role === "user" ? (
                <div className="p-3.5 sm:p-4 rounded-2xl border text-xs sm:text-[13px] leading-relaxed font-medium shadow-xs bg-black border-black text-white rounded-tr-none">
                  <div className="wrap-break-word whitespace-pre-wrap">{msg.content}</div>
                </div>
              ) : (
                /* Assistant Scientific Response Card (Full Width for Tables & Dense Data) */
                <div className="w-full bg-white border border-neutral-200/90 rounded-2xl rounded-tl-none p-4 sm:p-6 shadow-xs flex flex-col gap-3">
                  {/* Assistant Card Header */}
                  <div className="flex items-center justify-between pb-3 border-b border-neutral-100 gap-3">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-lg bg-black flex items-center justify-center shrink-0">
                        <Brain className="h-3.5 w-3.5 text-accent" />
                      </div>
                      <span className="font-serif font-bold text-xs text-neutral-900 tracking-tight">
                        Aera Scientific Intelligence
                      </span>
                      <span className="text-[9px] uppercase font-mono px-1.5 py-0.5 rounded bg-neutral-100 text-neutral-600 border border-neutral-200 font-semibold">
                        {level.replace("_", " ")}
                      </span>
                    </div>

                    {/* Copy Response Action */}
                    <CopyMessageButton content={msg.content} />
                  </div>

                  {/* Rendered Scientific Markdown (Tables, Headings, Formatting) */}
                  <div className="w-full overflow-hidden">
                    <AeraMarkdownRenderer
                      content={msg.content}
                      isStreaming={isStreaming && index === messages.length - 1}
                    />
                  </div>
                </div>
              )}

              {/* Message Latency & Citations Metadata */}
              {msg.role === "assistant" && msg.metadata && (
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-[9px] text-neutral-500 font-mono mt-1.5 px-2 uppercase tracking-wider font-semibold">
                  <span>Req: {msg.metadata.request_id?.slice(0, 8)}</span>
                  <span>•</span>
                  <span>Tokens: {msg.metadata.prompt_tokens || 0} In / {msg.metadata.completion_tokens || 0} Out</span>
                  <span>•</span>
                  <span>Latency: {((msg.metadata.total_time_ms || 0) / 1000).toFixed(2)}s</span>
                  
                  {msg.metadata.citations && msg.metadata.citations.length > 0 && (
                    <>
                      <span>•</span>
                      <span className="text-black font-bold flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                        {msg.metadata.citations.filter((c) => c.verified).length} verified references
                      </span>
                    </>
                  )}
                </div>
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input Form */}
      <form onSubmit={handleSend} className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          disabled={isStreaming}
          placeholder={
            mode === "compare"
              ? `Ask to compare ${compound.name} with selected molecule...`
              : `Ask Aera about ${compound.name}'s structure, toxicity, or mechanisms...`
          }
          className="flex-1 bg-white border-2 border-neutral-200 focus:border-black rounded-2xl px-5 py-3.5 text-xs sm:text-[13px] font-medium focus:outline-none transition-colors disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isStreaming}
          className="bg-black hover:bg-neutral-800 disabled:opacity-40 disabled:hover:bg-black text-white px-5 sm:px-6 rounded-2xl flex items-center justify-center gap-2 text-xs font-bold uppercase tracking-wider transition-all shadow-sm shrink-0 cursor-pointer"
        >
          {isStreaming ? (
            <RefreshCw className="h-4 w-4 animate-spin text-accent" />
          ) : (
            <Send className="h-4 w-4 text-accent" />
          )}
          <span>Ask</span>
        </button>
      </form>

    </div>
  );
}

function CopyMessageButton({ content }: { content: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy message:", err);
    }
  };

  return (
    <button
      onClick={handleCopy}
      type="button"
      className="flex items-center gap-1.5 px-2 py-1 rounded-lg text-[10px] font-semibold text-neutral-500 hover:text-black hover:bg-neutral-100 transition-colors border border-transparent hover:border-neutral-200 cursor-pointer"
      title="Copy markdown text"
    >
      {copied ? (
        <>
          <Check className="h-3 w-3 text-emerald-600" />
          <span className="text-emerald-600">Copied</span>
        </>
      ) : (
        <>
          <Copy className="h-3 w-3 text-neutral-400" />
          <span>Copy Output</span>
        </>
      )}
    </button>
  );
}
