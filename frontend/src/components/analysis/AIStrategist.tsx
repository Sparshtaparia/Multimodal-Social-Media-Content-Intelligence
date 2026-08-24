import { Recommendation } from '@/lib/types';
import { Card, CardContent } from '@/components/ui/card';
import { Sparkles, MessageSquare } from 'lucide-react';

export function AIStrategist({ recommendations }: { recommendations: Recommendation[] }) {
  const aiRecs = recommendations.filter(r => r.source === 'gemini' || r.source === 'hybrid');

  if (aiRecs.length === 0) return null;

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-8 border border-indigo-100 shadow-sm">
      <div className="flex items-center gap-3 mb-6">
        <div className="bg-indigo-100 p-2 rounded-lg">
          <Sparkles className="w-6 h-6 text-indigo-600" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-indigo-900">AI Content Strategist</h3>
          <p className="text-sm text-indigo-700/80">AI-generated qualitative analysis</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {aiRecs.map((rec, i) => (
          <Card key={i} className="border-indigo-100/50 bg-white/80 backdrop-blur-sm shadow-sm">
            <CardContent className="p-6">
              <div className="flex items-start gap-3">
                <MessageSquare className="w-5 h-5 text-indigo-400 mt-1 flex-shrink-0" />
                <div>
                  <h4 className="font-semibold text-slate-800 mb-2">{rec.problem}</h4>
                  <p className="text-slate-600 text-sm mb-4 leading-relaxed">{rec.recommendation}</p>
                  
                  {rec.rewrite && (
                    <div className="bg-indigo-50/50 p-3 rounded-lg border border-indigo-100/50">
                      <p className="text-xs uppercase tracking-wider text-indigo-400 font-medium mb-1">AI Suggestion</p>
                      <p className="text-indigo-900 font-medium italic text-sm">&quot;{rec.rewrite}&quot;</p>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      
      <p className="text-xs text-indigo-400/80 mt-6 text-center max-w-2xl mx-auto">
        AI recommendations are generated based on deterministic signals. Always verify AI suggestions against your brand voice.
      </p>
    </div>
  );
}
