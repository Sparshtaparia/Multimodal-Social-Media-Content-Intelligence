import { AnalysisResult } from '@/lib/types';
import { ExecutiveSummary } from './ExecutiveSummary';
import { ScoreHero } from './ScoreHero';
import { ScoreBreakdown } from './ScoreBreakdown';
import { OriginalContent } from './OriginalContent';
import { ContentProfile } from './ContentProfile';
import { RecommendationList } from './RecommendationList';
import { AIStrategist } from './AIStrategist';
import { TechnicalDetails } from './TechnicalDetails';

export function Dashboard({ analysis }: { analysis: AnalysisResult }) {
  const { engagement, recommendations, content_profile, visual_profile, document, processing } = analysis;

  return (
    <div className="space-y-10 pb-16">
      {/* Header Info */}
      <div className="flex items-center justify-between border-b pb-6">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 truncate max-w-2xl" title={document.filename}>
            {document.filename}
          </h1>
          <p className="text-sm text-slate-500 mt-1 uppercase tracking-wide">
            {document.file_type} • {(document.file_size / 1024).toFixed(1)} KB • {document.page_count} Pages
          </p>
        </div>
      </div>

      {/* Section 1: Executive Intelligence */}
      <section className="bg-white rounded-xl shadow-sm border p-8">
        <h2 className="text-xl font-bold text-slate-900 mb-6">Executive Intelligence</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 items-center">
          <div className="md:col-span-1 flex justify-center">
            {engagement && <ScoreHero score={engagement.overall_score} />}
          </div>
          <div className="md:col-span-3">
            <ExecutiveSummary analysis={analysis} />
          </div>
        </div>
      </section>

      {/* Section 2: Two-column layout */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-slate-900">Original Content</h2>
          <div className="bg-white rounded-xl shadow-sm border p-6 min-h-[400px]">
            <OriginalContent document={document} processing={processing} blocks={analysis.extracted_blocks} />
          </div>
        </div>
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-slate-900">Content Profile</h2>
          <div className="bg-white rounded-xl shadow-sm border p-6 min-h-[400px]">
            <ContentProfile document={document} content={content_profile} visual={visual_profile} processing={processing} />
          </div>
        </div>
      </section>

      {/* Section 3: Score Breakdown */}
      {engagement && (
        <section className="space-y-4">
          <h2 className="text-xl font-bold text-slate-900">Score Breakdown & Evidence</h2>
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <ScoreBreakdown engagement={engagement} />
          </div>
        </section>
      )}

      {/* Section 4: Prioritized Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-xl font-bold text-slate-900">Actionable Recommendations</h2>
          <RecommendationList recommendations={recommendations} />
        </section>
      )}

      {/* Section 5: AI Strategist */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900">AI Strategist</h2>
        {recommendations && recommendations.some(r => r.source === 'gemini' || r.source === 'hybrid') ? (
          <div className="bg-amber-50 rounded-xl border border-amber-200 p-6">
            <AIStrategist recommendations={recommendations} />
          </div>
        ) : (
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-6 text-slate-500 text-center">
            AI enhancement unavailable.
          </div>
        )}
      </section>

      {/* Section 6: Technical Details */}
      <section className="space-y-4">
        <TechnicalDetails analysis={analysis} />
      </section>
    </div>
  );
}
