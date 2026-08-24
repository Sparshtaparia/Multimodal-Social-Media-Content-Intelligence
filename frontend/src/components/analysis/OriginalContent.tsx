import { AnalysisResult } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText } from 'lucide-react';

export function OriginalContent({ document, processing, blocks }: { document: AnalysisResult['document'], processing: AnalysisResult['processing'], blocks: AnalysisResult['extracted_blocks'] }) {
  // Group blocks by page
  const pageGroups = (blocks || []).reduce((acc, block) => {
    const page = block.page_number || 1;
    if (!acc[page]) acc[page] = [];
    acc[page].push(block);
    return acc;
  }, {} as Record<number, typeof blocks>);

  const sortedPages = Object.keys(pageGroups).map(Number).sort((a, b) => a - b);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      
      {/* Left: Document Preview */}
      <Card className="shadow-sm border-slate-200 bg-slate-50">
        <CardHeader>
          <CardTitle>Original Content</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col items-center justify-center min-h-[300px] text-center text-slate-500 p-8">
          <FileText className="w-12 h-12 mb-4 text-slate-300" />
          <p className="font-medium text-slate-900 mb-1">{document.filename}</p>
          <p className="text-sm mb-4">{document.page_count} pages</p>
          <p className="text-sm text-slate-400 max-w-[250px]">
            The original file is not currently available for post-processing preview.
          </p>
        </CardContent>
      </Card>

      {/* Right: Extracted Content */}
      <Card className="shadow-sm flex flex-col h-[500px]">
        <CardHeader className="flex-shrink-0">
          <div className="flex justify-between items-center">
            <CardTitle>Extracted Information</CardTitle>
            <span className="text-xs font-medium text-slate-500 bg-slate-100 px-2 py-1 rounded">
              {processing.extraction_method === 'ocr' ? 'OCR' : 'Native PDF'}
            </span>
          </div>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
          {!blocks || blocks.length === 0 ? (
            <div className="flex items-center justify-center h-full text-sm text-slate-500">
              No text blocks extracted.
            </div>
          ) : (
            <div className="space-y-8">
              {sortedPages.map((pageNum) => (
                <div key={pageNum} className="space-y-3">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider sticky top-0 bg-white/90 py-1">Page {pageNum}</h4>
                  <div className="space-y-3">
                    {pageGroups[pageNum]?.map((block, idx) => (
                      <div key={block.id} className="p-3 bg-slate-50 rounded-md border text-sm text-slate-700 leading-relaxed group hover:bg-slate-100 transition-colors">
                        <div className="flex justify-between items-start mb-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <span className="text-[10px] text-slate-400 font-mono">Block {idx + 1}</span>
                        </div>
                        {block.text}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

    </div>
  );
}
