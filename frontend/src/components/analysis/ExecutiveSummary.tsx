import { AnalysisResult } from '@/lib/types';

export function ExecutiveSummary({ analysis }: { analysis: AnalysisResult }) {
  const score = analysis.engagement?.overall_score || 0;
  
  let judgement = "Content shows standard engagement indicators.";
  if (score >= 80) judgement = "Strong content with excellent engagement potential.";
  else if (score >= 60) judgement = "Good content with some opportunities to improve interaction.";
  else if (score >= 40) judgement = "Content needs improvement. Consider strengthening the CTA or hook.";
  else judgement = "Weak content. Significant improvements recommended across hook, clarity, and specific claims.";

  return (
    <div className="bg-slate-900 text-white rounded-xl p-8 shadow-sm">
      <div className="max-w-3xl">
        <h2 className="text-sm font-medium text-slate-400 mb-2 uppercase tracking-wider">Content Intelligence</h2>
        <h3 className="text-3xl font-bold mb-4">{analysis.document.filename}</h3>
        <p className="text-lg text-slate-300 leading-relaxed">
          {judgement}
        </p>
      </div>
    </div>
  );
}
