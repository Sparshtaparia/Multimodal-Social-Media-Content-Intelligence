import { ShieldCheck, Sparkles, BarChart3, ScanText, FileText, ArrowDown } from "lucide-react";

export default function MethodologyPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="space-y-12">
        <div className="space-y-4">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">How SocialLens evaluates content</h1>
          <p className="text-lg text-slate-600 leading-relaxed">
            SocialLens combines deterministic heuristic analysis with AI-driven insights to evaluate social media content. Our philosophy is simple: <strong className="text-slate-900">Deterministic analysis is the source of truth; AI provides interpretation.</strong>
          </p>
        </div>

        {/* Pipeline Diagram */}
        <section className="bg-white rounded-xl border p-8 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900 mb-8 text-center">The Intelligence Pipeline</h2>
          
          <div className="max-w-md mx-auto space-y-2">
            {[
              { label: "DOCUMENT", icon: <FileText className="h-4 w-4" />, color: "bg-slate-100 text-slate-700" },
              { label: "EXTRACTION", icon: <ScanText className="h-4 w-4" />, color: "bg-blue-100 text-blue-700" },
              { label: "CONTENT PROFILING", icon: <BarChart3 className="h-4 w-4" />, color: "bg-emerald-100 text-emerald-700" },
              { label: "VISUAL ANALYSIS", icon: <BarChart3 className="h-4 w-4" />, color: "bg-emerald-100 text-emerald-700" },
              { label: "ENGAGEMENT SCORING", icon: <ShieldCheck className="h-4 w-4" />, color: "bg-indigo-100 text-indigo-700" },
              { label: "EVIDENCE COLLECTION", icon: <ShieldCheck className="h-4 w-4" />, color: "bg-indigo-100 text-indigo-700" },
              { label: "AI ENRICHMENT & VALIDATION", icon: <Sparkles className="h-4 w-4" />, color: "bg-amber-100 text-amber-700" },
              { label: "FINAL RECOMMENDATIONS", icon: <Sparkles className="h-4 w-4" />, color: "bg-slate-900 text-white" }
            ].map((step, i, arr) => (
              <div key={step.label} className="flex flex-col items-center text-center">
                <div className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold text-sm w-full justify-center tracking-wide shadow-sm ${step.color}`}>
                  {step.icon} {step.label}
                </div>
                {i < arr.length - 1 && <ArrowDown className="h-5 w-5 text-slate-300 my-2" />}
              </div>
            ))}
          </div>
        </section>

        {/* Scoring Dimensions */}
        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-900">Scoring Dimensions</h2>
          <p className="text-slate-600">The overall Engagement Potential Score is an aggregation of 6 core heuristics, normalized to 0-100.</p>
          
          <div className="bg-white rounded-lg border overflow-hidden shadow-sm">
            <table className="w-full text-sm text-left">
              <thead className="bg-slate-50 border-b text-slate-700">
                <tr>
                  <th className="px-6 py-4 font-semibold">Dimension</th>
                  <th className="px-6 py-4 font-semibold">What it evaluates</th>
                  <th className="px-6 py-4 font-semibold">Signals Analyzed</th>
                </tr>
              </thead>
              <tbody className="divide-y text-slate-600">
                <tr>
                  <td className="px-6 py-4 font-medium text-slate-900">Hook</td>
                  <td className="px-6 py-4">Opening strength and ability to grab attention instantly.</td>
                  <td className="px-6 py-4">Questions, opening sentence length, presence of clear headlines.</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-slate-900">Clarity</td>
                  <td className="px-6 py-4">Ease of understanding and cognitive load.</td>
                  <td className="px-6 py-4">Readability metrics (Flesch), text density, paragraph length.</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-slate-900">Specificity</td>
                  <td className="px-6 py-4">Concrete information vs generic claims.</td>
                  <td className="px-6 py-4">Numbers, percentages, measurable claims, currency symbols.</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-slate-900">Emotion</td>
                  <td className="px-6 py-4">Emotional activation potential.</td>
                  <td className="px-6 py-4">Sentiment polarity, expressive emphasis, exclamation frequency.</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-slate-900">Interaction</td>
                  <td className="px-6 py-4">Direct audience engagement.</td>
                  <td className="px-6 py-4">Questions asked, second-person direct address (&quot;you&quot;, &quot;your&quot;).</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-slate-900">Call-to-Action</td>
                  <td className="px-6 py-4">Clarity of the desired user action.</td>
                  <td className="px-6 py-4">Action-oriented keyword detection, distinct UI blocks.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Evidence Model */}
        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-900">The Evidence Model</h2>
          <div className="bg-slate-50 p-6 rounded-xl border border-slate-200">
            <p className="text-slate-700 leading-relaxed mb-6">
              Scores are not black-box outputs. Supporting signals are retained with exact block and page provenance wherever possible. This ensures that every analytical conclusion can be traced back to the actual creative.
            </p>
            <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm font-medium bg-white p-6 rounded-lg border shadow-sm">
              <div className="flex flex-col items-center">
                <span className="text-slate-500 text-xs mb-1 uppercase tracking-wider">Metric</span>
                <span className="text-indigo-600 bg-indigo-50 px-3 py-1 rounded">Score</span>
              </div>
              <ArrowDown className="md:-rotate-90 h-4 w-4 text-slate-300" />
              <div className="flex flex-col items-center">
                <span className="text-slate-500 text-xs mb-1 uppercase tracking-wider">Detection</span>
                <span className="text-emerald-600 bg-emerald-50 px-3 py-1 rounded">Signal</span>
              </div>
              <ArrowDown className="md:-rotate-90 h-4 w-4 text-slate-300" />
              <div className="flex flex-col items-center">
                <span className="text-slate-500 text-xs mb-1 uppercase tracking-wider">Extracted Text</span>
                <span className="text-blue-600 bg-blue-50 px-3 py-1 rounded">Evidence</span>
              </div>
              <ArrowDown className="md:-rotate-90 h-4 w-4 text-slate-300" />
              <div className="flex flex-col items-center">
                <span className="text-slate-500 text-xs mb-1 uppercase tracking-wider">Geometry</span>
                <span className="text-amber-600 bg-amber-50 px-3 py-1 rounded">Block / BBox</span>
              </div>
              <ArrowDown className="md:-rotate-90 h-4 w-4 text-slate-300" />
              <div className="flex flex-col items-center">
                <span className="text-slate-500 text-xs mb-1 uppercase tracking-wider">Location</span>
                <span className="text-rose-600 bg-rose-50 px-3 py-1 rounded">Page</span>
              </div>
            </div>
          </div>
        </section>

        {/* AI Architecture */}
        <section className="space-y-4 pb-12">
          <div className="flex items-center gap-3">
            <Sparkles className="h-6 w-6 text-amber-500" />
            <h2 className="text-2xl font-bold text-slate-900">AI Strategist Architecture</h2>
          </div>
          <p className="text-slate-600 leading-relaxed">
            The AI Strategist layer acts as a consultant analyzing the deterministic profile. It generates qualitative rewrites and strategic insights.
          </p>
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
            <h4 className="font-semibold text-amber-900 mb-2">Core Principle</h4>
            <p className="text-amber-800">
              <strong>Gemini does not override deterministic scores.</strong> Recommendations from AI are strictly validated through a Critic framework that grounds claims against the original document text. Unsupported claims are flagged, and AI insights are layered on top of the deterministic rule engine as &quot;Hybrid&quot; recommendations rather than replacing them.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
