"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { formatDistanceToNow } from "date-fns";
import { Search, Filter, FileText, Image as ImageIcon, ChevronRight } from "lucide-react";
import { fetchAnalyses, LibraryAnalysis } from "@/lib/api";

export default function LibraryPage() {
  const [analyses, setAnalyses] = useState<LibraryAnalysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchAnalyses();
        setAnalyses(data.analyses || []);
      } catch {
        setError("Failed to load analyses");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="flex flex-col gap-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Content Library</h1>
          <p className="text-slate-500 mt-1">Review previously analyzed content.</p>
        </div>

        {/* Toolbar */}
        <div className="flex items-center justify-between gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input 
              type="text"
              placeholder="Search filename..." 
              className="w-full h-10 pl-9 pr-4 rounded-md border border-slate-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled
            />
          </div>
          <button className="inline-flex items-center justify-center h-10 px-4 py-2 border border-slate-200 bg-white rounded-md text-sm font-medium hover:bg-slate-50 transition-colors" disabled>
            <Filter className="h-4 w-4 mr-2" /> Filter
          </button>
        </div>

        {/* Content */}
        {loading ? (
          <div className="text-center py-24 text-slate-500">Loading library...</div>
        ) : error ? (
          <div className="text-center py-24 text-red-500">{error}</div>
        ) : analyses.length === 0 ? (
          <div className="text-center py-24 bg-white border border-slate-200 border-dashed rounded-lg">
            <h3 className="text-lg font-semibold text-slate-900">No analyses yet</h3>
            <p className="text-slate-500 mt-1">Upload your first piece of content to begin.</p>
            <Link href="/analyze" className="inline-flex mt-6 bg-blue-600 text-white px-4 py-2 rounded-md font-medium text-sm hover:bg-blue-700">
              New Analysis
            </Link>
          </div>
        ) : (
          <div className="bg-white border rounded-lg overflow-hidden shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left text-slate-600">
                <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-b">
                  <tr>
                    <th scope="col" className="px-6 py-3 font-medium">Content</th>
                    <th scope="col" className="px-6 py-3 font-medium">Type</th>
                    <th scope="col" className="px-6 py-3 font-medium text-center">Score</th>
                    <th scope="col" className="px-6 py-3 font-medium">Status</th>
                    <th scope="col" className="px-6 py-3 font-medium">Analyzed</th>
                    <th scope="col" className="px-6 py-3 font-medium">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {analyses.map((doc) => (
                    <tr key={doc.id} className="border-b last:border-0 hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 font-medium text-slate-900 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          {doc.file_type === 'pdf' ? <FileText className="h-4 w-4 text-blue-500" /> : <ImageIcon className="h-4 w-4 text-emerald-500" />}
                          <span className="truncate max-w-[200px]" title={doc.filename}>{doc.filename}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 uppercase text-xs font-semibold">{doc.file_type}</td>
                      <td className="px-6 py-4 text-center font-bold text-slate-900">
                        {doc.overall_score !== null ? doc.overall_score : '-'}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize
                          ${doc.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' : 
                            doc.status === 'FAILED' ? 'bg-red-100 text-red-800' : 
                            'bg-blue-100 text-blue-800'}`}>
                          {doc.status.toLowerCase()}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-slate-500 whitespace-nowrap">
                        {doc.created_at ? formatDistanceToNow(new Date(doc.created_at), { addSuffix: true }) : '-'}
                      </td>
                      <td className="px-6 py-4">
                        <Link href={`/analysis/${doc.id}`} className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium hover:underline">
                          View <ChevronRight className="h-4 w-4 ml-1" />
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
