import { Engagement, Evidence } from '@/lib/types';
import { useState } from 'react';
import { Progress } from '@/components/ui/progress';
import { ChevronRight, ChevronDown } from 'lucide-react';

function EvidenceItem({ evidence }: { evidence: Evidence }) {
  return (
    <div className="bg-slate-50 p-4 rounded-md border text-sm mt-3 animate-in slide-in-from-top-2 duration-200">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <span className="text-slate-500 block text-xs uppercase tracking-wider mb-1">Signal</span>
          <span className="font-medium text-slate-900">{evidence.signal.replace(/_/g, ' ')}</span>
        </div>
        {evidence.source && evidence.page && (
          <div>
            <span className="text-slate-500 block text-xs uppercase tracking-wider mb-1">Source</span>
            <span className="text-slate-700">Page {evidence.page} {evidence.block_id && `· Block ${evidence.block_id.split('-')[0]}`}</span>
          </div>
        )}
      </div>
      
      {evidence.value && (
        <div className="mt-3">
          <span className="text-slate-500 block text-xs uppercase tracking-wider mb-1">Evidence</span>
          <p className="text-slate-700 italic border-l-2 border-slate-300 pl-3 py-1">&quot;{evidence.value}&quot;</p>
        </div>
      )}
    </div>
  );
}

export function ScoreBreakdown({ engagement }: { engagement: Engagement }) {
  const [expandedRow, setExpandedRow] = useState<string | null>(null);

  const components = [
    { key: 'hook_score', label: 'Hook' },
    { key: 'clarity_score', label: 'Clarity' },
    { key: 'specificity_score', label: 'Specificity' },
    { key: 'cta_score', label: 'CTA' },
    { key: 'emotion_score', label: 'Emotion' },
    { key: 'interaction_score', label: 'Interaction' },
    { key: 'readability_score', label: 'Readability' },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border p-6 md:p-8">
      <h3 className="text-xl font-semibold mb-6">Score Breakdown</h3>
      
      <div className="space-y-1">
        {components.map(({ key, label }) => {
          const score = (engagement.components as unknown as Record<string, number>)[key] || 0;
          const isExpanded = expandedRow === key;
          
          // Find evidence for this component
          // Since our backend doesn't strongly link evidence to the exact component string in the JSON, 
          // we match by signal name heuristic.
          const componentEvidence = engagement.evidence.filter(e => {
            const s = e.signal.toLowerCase();
            if (key === 'cta_score') return s.includes('cta');
            if (key === 'hook_score') return s.includes('hook') || s.includes('opening') || s.includes('headline');
            if (key === 'specificity_score') return s.includes('specific') || s.includes('measur');
            if (key === 'emotion_score') return s.includes('emotion') || s.includes('exclamation') || s.includes('sentiment');
            if (key === 'interaction_score') return s.includes('question') || s.includes('audience');
            if (key === 'clarity_score' || key === 'readability_score') return s.includes('readability') || s.includes('density');
            return false;
          });

          return (
            <div key={key} className="border-b last:border-0 border-slate-100 py-3">
              <button 
                onClick={() => setExpandedRow(isExpanded ? null : key)}
                className="w-full flex items-center gap-4 hover:bg-slate-50 p-2 rounded-lg transition-colors text-left"
              >
                <div className="w-32 font-medium text-slate-700 flex items-center justify-between">
                  {label}
                  {componentEvidence.length > 0 && (
                    isExpanded ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />
                  )}
                </div>
                
                <div className="flex-1 flex items-center gap-4">
                  <Progress value={score} className="h-2.5 flex-1" indicatorColor={score > 70 ? 'bg-green-500' : score > 40 ? 'bg-blue-500' : 'bg-amber-500'} />
                  <span className="w-8 text-right font-semibold text-slate-700">{score}</span>
                </div>
              </button>
              
              {isExpanded && componentEvidence.length > 0 && (
                <div className="pl-36 pr-12 pb-2">
                  <p className="text-sm font-medium text-slate-900 mt-2 mb-2">Why?</p>
                  {componentEvidence.map((ev, i) => (
                    <EvidenceItem key={i} evidence={ev} />
                  ))}
                </div>
              )}
              {isExpanded && componentEvidence.length === 0 && (
                <div className="pl-36 pr-12 pb-2 mt-2">
                  <p className="text-sm text-slate-500">No specific textual evidence available for this score.</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
