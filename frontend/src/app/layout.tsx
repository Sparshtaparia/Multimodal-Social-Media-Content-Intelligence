import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { TooltipProvider } from '@/components/ui/tooltip';
import Link from 'next/link';
import { BarChart3, BookOpen, Library, Search } from 'lucide-react';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SocialLens - Content Intelligence',
  description: 'Evidence-grounded multimodal content intelligence for social media.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} text-slate-900 bg-slate-50 min-h-screen flex flex-col`}>
        <TooltipProvider>
          <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
            <div className="container mx-auto px-4 h-14 flex items-center justify-between">
              <div className="flex items-center gap-6">
                <Link href="/" className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5 text-blue-600" />
                  <span className="font-semibold tracking-tight text-slate-900">SocialLens</span>
                </Link>
                <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-600">
                  <Link href="/analyze" className="hover:text-slate-900 transition-colors flex items-center gap-2">
                    <Search className="h-4 w-4" /> Analyze
                  </Link>
                  <Link href="/library" className="hover:text-slate-900 transition-colors flex items-center gap-2">
                    <Library className="h-4 w-4" /> Library
                  </Link>
                  <Link href="/methodology" className="hover:text-slate-900 transition-colors flex items-center gap-2">
                    <BookOpen className="h-4 w-4" /> Methodology
                  </Link>
                </nav>
              </div>
              <div className="flex items-center">
                <Link 
                  href="/analyze" 
                  className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring bg-blue-600 text-white shadow hover:bg-blue-600/90 h-9 px-4 py-2"
                >
                  New Analysis
                </Link>
              </div>
            </div>
          </header>
          <main className="flex-1 flex flex-col">
            {children}
          </main>
        </TooltipProvider>
      </body>
    </html>
  );
}
