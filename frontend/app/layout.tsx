import type { Metadata } from 'next';
import { Inter, Outfit } from 'next/font/google';
import './globals.css';
import AppProviders from '@/components/providers/AppProviders';
import Sidebar from '@/components/layout/Sidebar';
import Header from '@/components/layout/Header';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const outfit = Outfit({
  subsets: ['latin'],
  variable: '--font-outfit',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'TeeDesign AI — Autonomous Merchandise Illustration Command Center',
  description: 'AI-driven apparel illustration platform for TeePublic merchandise creation, quality control, and SEO automation.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`dark ${inter.variable} ${outfit.variable}`}>
      <body className="min-h-screen bg-background text-slate-100 antialiased selection:bg-purple-500/30 selection:text-purple-200">
        <AppProviders>
          <div className="flex min-h-screen">
            {/* Sidebar navigation */}
            <Sidebar />

            {/* Main content container */}
            <div className="flex-1 flex flex-col min-w-0 pl-20 lg:pl-64 transition-all duration-300">
              <Header />
              <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto animate-fade-in">
                {children}
              </main>
            </div>
          </div>
        </AppProviders>
      </body>
    </html>
  );
}
