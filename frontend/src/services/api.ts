import axios from "axios";
import { Category, CategoryDetailed, Compound, CompoundDetailed, Reference, AeraChatMetadata } from "../types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const apiService = {
  getCompounds: async (categoryId?: number): Promise<Compound[]> => {
    const params = categoryId ? { category_id: categoryId } : {};
    const response = await apiClient.get<Compound[]>("/compounds", { params });
    return response.data;
  },

  getCompound: async (idOrSlug: string): Promise<CompoundDetailed> => {
    const response = await apiClient.get<CompoundDetailed>(`/compounds/${idOrSlug}`);
    return response.data;
  },

  getCategories: async (): Promise<Category[]> => {
    const response = await apiClient.get<Category[]>("/categories");
    return response.data;
  },

  getCategory: async (idOrSlug: string): Promise<CategoryDetailed> => {
    const response = await apiClient.get<CategoryDetailed>(`/categories/${idOrSlug}`);
    return response.data;
  },

  searchCompounds: async (query: string): Promise<Compound[]> => {
    if (!query.trim()) return [];
    // Kept for backward compatibility if needed by simple components
    const response = await apiClient.get<{ results: Compound[] }>("/search", {
      params: { q: query, page_size: 50 },
    });
    return response.data.results;
  },

  searchCompoundsAdvanced: async (
    query?: string,
    category?: string,
    subcategory?: string,
    sortBy: string = "name",
    sortOrder: string = "asc",
    page: number = 1,
    pageSize: number = 25
  ): Promise<{
    total_count: number;
    page: number;
    page_size: number;
    total_pages: number;
    results: Compound[];
  }> => {
    const response = await apiClient.get<{
      total_count: number;
      page: number;
      page_size: number;
      total_pages: number;
      results: Compound[];
    }>("/search", {
      params: {
        q: query || undefined,
        category: category || undefined,
        subcategory: subcategory || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
        page,
        page_size: pageSize
      }
    });
    return response.data;
  },

  getSearchSuggestions: async (query: string): Promise<Array<{
    text: string;
    type: string;
    slug: string;
    formula?: string;
    cas?: string;
  }>> => {
    if (!query.trim()) return [];
    const response = await apiClient.get<Array<{
      text: string;
      type: string;
      slug: string;
      formula?: string;
      cas?: string;
    }>>("/search/suggestions", {
      params: { q: query }
    });
    return response.data;
  },

  getReferences: async (): Promise<Reference[]> => {
    const response = await apiClient.get<Reference[]>("/references");
    return response.data;
  },

  streamAeraChat: async (
    payload: {
      compound_slug: string;
      compare_with_slug?: string;
      question: string;
      messages: Array<{ role: string; content: string }>;
      level: string;
      mode: string;
    },
    onChunk: (text: string) => void,
    onMetadata: (metadata: AeraChatMetadata) => void,
    onError: (err: Error) => void
  ): Promise<void> => {
    try {
      const response = await fetch(`${API_URL}/aera/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      if (!response.body) {
        throw new Error("ReadableStream not supported by browser response.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const cleanLine = line.trim();
          if (cleanLine.startsWith("data: ")) {
            const dataStr = cleanLine.substring(6).trim();
            if (!dataStr) continue;
            try {
              const parsed = JSON.parse(dataStr);
              if (parsed.type === "content") {
                onChunk(parsed.delta);
              } else if (parsed.type === "metadata") {
                onMetadata(parsed);
              } else if (parsed.type === "error") {
                onError(new Error(parsed.message));
              }
            } catch (e) {
              console.error("SSE JSON parsing error:", e, dataStr);
            }
          }
        }
      }
    } catch (err) {
      onError(err instanceof Error ? err : new Error(String(err)));
    }
  }
};
export default apiService;
