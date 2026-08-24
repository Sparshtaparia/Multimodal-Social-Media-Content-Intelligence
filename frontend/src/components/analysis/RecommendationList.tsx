import { Recommendation } from '@/lib/types';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ChevronRight, AlertTriangle, Lightbulb } from 'lucide-react';

function RecommendationCard({ rec }: { rec: Recommendation }) {
  const isHigh = rec.priority === 'HIGH';
  const isMed = rec.priority === 'MEDIUM';

  return (
    <Card className={`border-l-4 ${isHigh ? 'border-l-red-500' : isMed ? 'border-l-amber-500' : 'border-l-blue-500'} shadow-sm hover:shadow transition-shadow`}>
      <CardContent className="p-6">
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center gap-2 mb-2">
            <Badge variant={isHigh ? "destructive" : isMed ? "default" : "secondary"} className={isMed ? 'bg-amber-500 hover:bg-amber-600' : ''}>
              {rec.priority}
            </Badge>
            <span className="text-sm font-medium text-slate-500 uppercase tracking-wider">{rec.category}</span>
          </div>
          
          <Badge variant="outline" className="text-xs text-slate-500 bg-slate-50">
            {rec.source === 'gemini' || rec.source === 'hybrid' ? 'Rule + AI' : 'Rule'}
          </Badge>
        </div>

        <h4 className="text-lg font-semibold text-slate-900 mb-3">{rec.problem}</h4>
        
        {rec.evidence && rec.evidence.length > 0 && (
          <div className="bg-slate-50 p-4 rounded-md mb-4 text-sm text-slate-700 border">
            <p className="font-medium text-slate-900 mb-1 text-xs uppercase tracking-wider flex items-center gap-1"><AlertTriangle className="w-3 h-3" /> Evidence</p>
            {rec.evidence.map((ev, i) => (
              <div key={i} className="mb-2 last:mb-0">
                <span className="italic border-l-2 border-slate-300 pl-2">&quot;{ev.value}&quot;</span>
                {(ev.page || ev.block_id) && (
                  <span className="text-slate-400 text-xs ml-2">
                    (Page {ev.page || '?'} {ev.block_id && `· Block ${ev.block_id.split('-')[0]}`})
                  </span>
                )}
              </div>
            ))}
          </div>
        )}

        <div className="flex gap-3 items-start mt-4">
          <Lightbulb className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
          <p className="text-slate-800 font-medium">{rec.recommendation}</p>
        </div>

        {rec.rewrite && (
          <div className="mt-4 bg-blue-50/50 p-4 rounded-md border border-blue-100">
             <p className="font-medium text-blue-900 mb-2 text-xs uppercase tracking-wider">Suggested Rewrite</p>
             <div className="flex gap-2">
                <ChevronRight className="w-4 h-4 text-blue-400 flex-shrink-0 mt-1" />
                <p className="text-blue-900 font-medium italic">&quot;{rec.rewrite}&quot;</p>
             </div>
             {rec.supported === false && (
                <p className="text-xs text-red-500 mt-2 bg-red-50 p-2 rounded">
                  ⚠️ AI generation contains unsupported numerical claims not found in the original text.
                </p>
             )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function RecommendationList({ recommendations }: { recommendations: Recommendation[] }) {
  // Sort HIGH -> MEDIUM -> LOW
  const sorted = [...recommendations].sort((a, b) => {
    const p = { 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
    return (p[b.priority as keyof typeof p] || 0) - (p[a.priority as keyof typeof p] || 0);
  });

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {sorted.map((rec, i) => (
        <RecommendationCard key={i} rec={rec} />
      ))}
    </div>
  );
}
