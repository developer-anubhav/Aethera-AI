import type { Metadata } from "next";
import { Inter, Playfair_Display } from "next/font/google";
import "./globals.css";
import Providers from "../components/providers";
import Header from "../components/layout/Header";
import Footer from "../components/layout/Footer";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const playfair = Playfair_Display({
  variable: "--font-playfair",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Aethera AI | Molecular Database & Interactive 3D Visualization",
  description: "A premier molecular database platform exploring chemical compounds, biomolecules, proteins, and crystal coordinates with interactive 3D WebGL visualizations.",
  keywords: "chemical compound, biochemistry, 3D molecule, protein structure, molecular viewer, IUPAC, PubChem, Aethera AI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${playfair.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col font-sans bg-white text-black selection:bg-black selection:text-white antialiased">
        <Providers>
          <Header />
          <main className="flex-1 w-full bg-white">
            <div className="mx-auto max-w-7xl">
              {children}
            </div>
          </main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
