import { UploadZone } from '@/components/upload/UploadZone';
import { Search } from 'lucide-react';

export default function AnalyzePage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <div className="bg-white border rounded-xl shadow-sm overflow-hidden">
        <div className="border-b bg-slate-50 px-6 py-8 text-center space-y-2">
          <div className="h-12 w-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <Search className="h-6 w-6" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">
            New Content Analysis
          </h2>
          <p className="text-slate-500 max-w-lg mx-auto">
            Upload a social-media creative to extract its structure, evaluate engagement signals, and identify improvement opportunities.
          </p>
        </div>
        
        <div className="p-8">
          <UploadZone />
        </div>
      </div>
    </div>
  );
}
