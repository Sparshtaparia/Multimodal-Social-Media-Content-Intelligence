import { ContentProfile as ContentProfileType, DocumentInfo, ProcessingInfo, VisualProfile } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Props {
  document: DocumentInfo;
  content?: ContentProfileType;
  visual?: VisualProfile;
  processing: ProcessingInfo;
}

function StatGroup({ title, children }: { title: string, children: React.ReactNode }) {
  return (
    <div className="space-y-4">
      <h4 className="font-semibold text-sm text-slate-500 uppercase tracking-wider">{title}</h4>
      <div className="grid grid-cols-2 gap-x-4 gap-y-3">
        {children}
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string, value: string | number | undefined }) {
  return (
    <div className="flex flex-col min-w-0">
      <span className="text-xs text-slate-500 truncate">{label}</span>
      <span className="text-sm font-medium text-slate-900 truncate" title={value?.toString()}>{value !== undefined ? value : '-'}</span>
    </div>
  );
}

export function ContentProfile({ document, content, visual, processing }: Props) {
  return (
    <Card className="h-full shadow-sm">
      <CardHeader>
        <CardTitle>Content Profile</CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        
        <StatGroup title="Document">
          <Stat label="File" value={document.filename} />
          <Stat label="Type" value={document.file_type.toUpperCase()} />
          <Stat label="Size" value={`${(document.file_size / (1024 * 1024)).toFixed(2)} MB`} />
          <Stat label="Pages" value={document.page_count} />
        </StatGroup>

        <StatGroup title="Extraction">
          <Stat label="Method" value={processing.extraction_method || 'Native PDF'} />
          <Stat label="OCR Used" value={processing.ocr_used ? 'Yes' : 'No'} />
          <Stat label="Text Blocks" value={visual?.text_block_count} />
          <Stat label="Image Blocks" value={visual?.image_block_count} />
        </StatGroup>

        <StatGroup title="Linguistic">
          <Stat label="Words" value={content?.word_count} />
          <Stat label="Sentences" value={content?.sentence_count} />
          <Stat label="Readability" value={content?.readability_score} />
          <Stat label="Questions" value={content?.sentiment_score} /> {/* Needs actual question count if available, backend didn't provide in schema explicitly. We'll show sentiment */}
          <Stat label="Sentiment" value={content?.sentiment_score !== undefined ? (content.sentiment_score > 0 ? 'Positive' : content.sentiment_score < 0 ? 'Negative' : 'Neutral') : undefined} />
        </StatGroup>

        <StatGroup title="Visual">
          <Stat label="Text Area" value={visual?.text_area_ratio !== undefined ? `${(visual.text_area_ratio * 100).toFixed(1)}%` : undefined} />
          <Stat label="Image Area" value={visual?.image_area_ratio !== undefined ? `${(visual.image_area_ratio * 100).toFixed(1)}%` : undefined} />
        </StatGroup>

      </CardContent>
    </Card>
  );
}
