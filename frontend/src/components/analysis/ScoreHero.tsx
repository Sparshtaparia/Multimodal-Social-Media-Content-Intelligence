import { Info } from 'lucide-react';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"

export function ScoreHero({ score }: { score: number }) {
  let label = "Weak";
  let colorClass = "text-red-500";
  
  if (score >= 80) {
    label = "Strong";
    colorClass = "text-green-600";
  } else if (score >= 60) {
    label = "Good";
    colorClass = "text-blue-600";
  } else if (score >= 40) {
    label = "Needs Improvement";
    colorClass = "text-amber-500";
  }

  return (
    <div className="bg-white border rounded-xl p-8 flex flex-col items-center justify-center h-full shadow-sm relative">
      <div className="absolute top-4 right-4">
        <Tooltip>
          <TooltipTrigger>
            <Info className="w-5 h-5 text-slate-400 hover:text-slate-600" />
          </TooltipTrigger>
          <TooltipContent className="max-w-xs">
            <p>Heuristic score based on extracted content characteristics. It is not a prediction of actual engagement.</p>
          </TooltipContent>
        </Tooltip>
      </div>

      <h3 className="text-lg font-medium text-slate-600 mb-6">Engagement Potential</h3>
      
      <div className="flex items-baseline gap-2 mb-4">
        <span className={`text-6xl font-bold tracking-tighter ${colorClass}`}>
          {score}
        </span>
        <span className="text-2xl font-medium text-slate-400">/100</span>
      </div>
      
      <div className={`px-4 py-1.5 rounded-full text-sm font-semibold bg-slate-50 border ${colorClass.replace('text-', 'border-').replace('600', '200').replace('500', '200')}`}>
        <span className={colorClass}>{label}</span>
      </div>
    </div>
  );
}
