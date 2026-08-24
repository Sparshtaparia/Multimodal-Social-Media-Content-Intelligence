import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { TooltipProvider } from '@/components/ui/tooltip';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SocialLens - Content Intelligence',
  description: 'Multimodal Social Media Content Analyzer',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <TooltipProvider>
          <div className="min-h-screen bg-slate-50 flex flex-col">
            <header className="border-b bg-white">
              <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                <div>
                  <h1 className="text-lg font-semibold tracking-tight">SocialLens</h1>
                  <p className="text-xs text-muted-foreground">Content Intelligence</p>
                </div>
                <nav>
                  <Link href="/" className="text-sm font-medium text-primary hover:underline">
                    + New Analysis
                  </Link>
                </nav>
              </div>
            </header>
            <main className="flex-1">{children}</main>
          </div>
        </TooltipProvider>
      </body>
    </html>
  );
}
