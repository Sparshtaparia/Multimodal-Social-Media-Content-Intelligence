'use client';

import { useEffect, useState } from 'react';
import { getAnalysis } from '@/lib/api';
import { AnalysisResult } from '@/lib/types';
import { ProcessingTimeline } from '@/components/processing/ProcessingTimeline';
import { Dashboard } from '@/components/analysis/Dashboard';
import { AlertCircle, FileX } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function AnalysisPage({ params }: { params: { id: string } }) {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    let isMounted = true;
    // eslint-disable-next-line prefer-const
    let pollInterval: NodeJS.Timeout | undefined;

    const fetchStatus = async () => {
      try {
        const data = await getAnalysis(params.id);
        if (!isMounted) return;
        
        setAnalysis(data);

        // Stop polling if done
        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          clearInterval(pollInterval);
        }
      } catch (err: unknown) {
        if (!isMounted) return;
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('Failed to retrieve analysis');
        }
        clearInterval(pollInterval);
      }
    };

    // Initial fetch
    fetchStatus();

    // Poll every 1.5 seconds
    pollInterval = setInterval(fetchStatus, 1500);

    return () => {
      isMounted = false;
      clearInterval(pollInterval);
    };
  }, [params.id]);

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] p-4 text-center">
        <FileX className="w-12 h-12 text-slate-400 mb-4" />
        <h2 className="text-xl font-semibold mb-2">Analysis not found</h2>
        <p className="text-slate-500 mb-6 max-w-sm">{error}</p>
        <Link href="/">
          <Button>New Analysis</Button>
        </Link>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] p-4">
        <div className="animate-pulse flex flex-col items-center">
          <div className="h-12 w-12 bg-slate-200 rounded-full mb-4"></div>
          <div className="h-6 w-48 bg-slate-200 rounded mb-2"></div>
          <div className="h-4 w-32 bg-slate-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (analysis.status === 'FAILED') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] p-4 text-center">
        <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
        <h2 className="text-xl font-semibold mb-2">Analysis could not be completed</h2>
        <p className="text-slate-500 mb-6 max-w-sm">Unable to process the uploaded document.</p>
        <Link href="/">
          <Button>Try Again</Button>
        </Link>
      </div>
    );
  }

  if (analysis.status !== 'COMPLETED') {
    return (
      <div className="container mx-auto p-4 max-w-xl mt-12">
        <ProcessingTimeline status={analysis.status} />
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-[1400px]">
      <Dashboard analysis={analysis} />
    </div>
  );
}
