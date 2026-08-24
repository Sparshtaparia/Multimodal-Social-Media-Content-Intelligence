import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

const STATUS_ORDER = [
  { key: 'UPLOADING', label: 'Uploading file' },
  { key: 'VALIDATING', label: 'Validating your file' },
  { key: 'EXTRACTING', label: 'Extracting content' },
  { key: 'PROFILING', label: 'Profiling content' },
  { key: 'SCORING', label: 'Evaluating engagement signals' },
  { key: 'GENERATING_RECOMMENDATIONS', label: 'Generating improvement recommendations' },
  { key: 'FINALIZING', label: 'Preparing your report' },
];

export function ProcessingTimeline({ status }: { status: string }) {
  const currentIndex = STATUS_ORDER.findIndex(s => s.key === status);
  const activeIndex = currentIndex === -1 ? 0 : currentIndex;

  return (
    <div className="bg-white p-8 rounded-lg shadow-sm border border-slate-200">
      <h2 className="text-2xl font-bold mb-8 text-center text-slate-800">Analyzing Content</h2>
      
      <div className="space-y-6 max-w-sm mx-auto">
        {STATUS_ORDER.map((stage, idx) => {
          const isCompleted = idx < activeIndex;
          const isActive = idx === activeIndex;

          return (
            <div key={stage.key} className="flex items-center gap-4">
              {isCompleted ? (
                <CheckCircle2 className="w-6 h-6 text-green-500 flex-shrink-0" />
              ) : isActive ? (
                <Loader2 className="w-6 h-6 text-primary animate-spin flex-shrink-0" />
              ) : (
                <Circle className="w-6 h-6 text-slate-200 flex-shrink-0" />
              )}
              
              <span className={`text-base font-medium ${
                isActive ? 'text-slate-900' : 
                isCompleted ? 'text-slate-600' : 
                'text-slate-400'
              }`}>
                {stage.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
