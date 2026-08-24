import { AnalysisResult } from '@/lib/types';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"

export function TechnicalDetails({ analysis }: { analysis: AnalysisResult }) {
  const { document, processing, engagement, visual_profile } = analysis;

  return (
    <Accordion className="w-full bg-white rounded-xl shadow-sm border px-6">
      <AccordionItem value="technical-details" className="border-0">
        <AccordionTrigger className="text-slate-600 hover:text-slate-900 font-medium py-6 hover:no-underline">
          Technical Details & Metadata
        </AccordionTrigger>
        <AccordionContent className="pb-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-sm">
            <div>
              <p className="text-slate-500 mb-1">Analysis ID</p>
              <p className="font-mono text-slate-700 text-xs truncate" title={analysis.analysis_id}>{analysis.analysis_id}</p>
            </div>
            <div>
              <p className="text-slate-500 mb-1">Extraction Method</p>
              <p className="text-slate-900">{processing.extraction_method || 'Native'}</p>
            </div>
            <div>
              <p className="text-slate-500 mb-1">OCR Used</p>
              <p className="text-slate-900">{processing.ocr_used ? 'Yes' : 'No'}</p>
            </div>
            <div>
              <p className="text-slate-500 mb-1">Processing Time</p>
              <p className="text-slate-900">{processing.processing_time_ms ? `${(processing.processing_time_ms / 1000).toFixed(2)}s` : 'Unknown'}</p>
            </div>
            <div>
              <p className="text-slate-500 mb-1">Scoring Version</p>
              <p className="font-mono text-slate-700 text-xs">{engagement?.scoring_version || 'v1.0'}</p>
            </div>
            <div>
              <p className="text-slate-500 mb-1">Pages Processed</p>
              <p className="text-slate-900">{document.page_count || 1}</p>
            </div>
            <div>
              <p className="text-slate-500 mb-1">Text Blocks</p>
              <p className="text-slate-900">{visual_profile?.text_block_count || 0}</p>
            </div>
            <div>
              <p className="text-slate-500 mb-1">Image Blocks</p>
              <p className="text-slate-900">{visual_profile?.image_block_count || 0}</p>
            </div>
          </div>
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );
}
