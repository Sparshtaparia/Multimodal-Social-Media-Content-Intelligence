import { AnalysisResult } from '@/lib/types';
import { ExecutiveSummary } from './ExecutiveSummary';
import { ScoreHero } from './ScoreHero';
import { ScoreBreakdown } from './ScoreBreakdown';
import { OriginalContent } from './OriginalContent';
import { ContentProfile } from './ContentProfile';
import { RecommendationList } from './RecommendationList';
import { AIStrategist } from './AIStrategist';
import { TechnicalDetails } from './TechnicalDetails';
import { Separator } from '@/components/ui/separator';

export function Dashboard({ analysis }: { analysis: AnalysisResult }) {
  const { engagement, recommendations, content_profile, visual_profile, document, processing } = analysis;

  return (
    <div className="space-y-12 pb-16">
      {/* 1. Executive Summary */}
      <section>
        <ExecutiveSummary analysis={analysis} />
      </section>

      <Separator />

      {/* 2. Score Hero & Profile */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          {engagement && <ScoreHero score={engagement.overall_score} />}
        </div>
        <div className="md:col-span-2">
          <ContentProfile document={document} content={content_profile} visual={visual_profile} processing={processing} />
        </div>
      </section>
      
      <Separator />

      {/* 4. Original / Extracted Content */}
      <section>
        <OriginalContent document={document} processing={processing} blocks={analysis.extracted_blocks} />
      </section>

      <Separator />

      {/* 3 & 5. Score Breakdown & Why */}
      {engagement && (
        <section>
          <ScoreBreakdown engagement={engagement} />
        </section>
      )}

      <Separator />

      {/* 6. Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold mb-6">Recommended Improvements</h2>
          <RecommendationList recommendations={recommendations} />
        </section>
      )}

      {/* 7. AI Strategist (if available, e.g. from overall summaries or rewrites) */}
      {recommendations && recommendations.some(r => r.source === 'gemini' || r.source === 'hybrid') ? (
         <>
          <Separator />
          <section>
            <AIStrategist recommendations={recommendations} />
          </section>
         </>
      ) : (
        <div className="mt-8 p-4 bg-amber-50 text-amber-800 text-sm border border-amber-200 rounded-lg">
          <strong>AI enhancement unavailable.</strong> Your deterministic content analysis and rule-based recommendations are still available.
        </div>
      )}

      <Separator />

      {/* 8. Technical Details */}
      <section>
        <TechnicalDetails analysis={analysis} />
      </section>
    </div>
  );
}
