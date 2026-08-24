import Link from "next/link";
import { ArrowRight, BarChart3, ScanText, ShieldCheck, Sparkles } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex flex-col flex-1">
      {/* Hero */}
      <section className="bg-white border-b overflow-hidden">
        <div className="container mx-auto px-4 py-24 sm:py-32 flex flex-col items-center text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl max-w-4xl">
            Understand what makes your content perform.
          </h1>
          <p className="mt-6 text-xl text-slate-600 max-w-2xl leading-relaxed">
            SocialLens analyzes social-media creatives using multimodal extraction, linguistic signals, visual structure, deterministic scoring, and evidence-grounded AI recommendations.
          </p>
          <div className="mt-10 flex items-center gap-4">
            <Link
              href="/analyze"
              className="inline-flex h-12 items-center justify-center rounded-md bg-blue-600 px-8 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700"
            >
              Analyze Content
            </Link>
            <Link
              href="/methodology"
              className="inline-flex h-12 items-center justify-center rounded-md border border-slate-200 bg-white px-8 text-sm font-medium text-slate-900 shadow-sm transition-colors hover:bg-slate-100 hover:text-slate-900"
            >
              Explore Methodology
            </Link>
          </div>
          
          {/* Design preview illustration */}
          <div className="mt-16 w-full max-w-5xl rounded-xl border bg-slate-50/50 p-4 shadow-xl ring-1 ring-slate-900/5 relative overflow-hidden">
            <div className="absolute top-2 right-4 z-10 text-xs font-semibold text-slate-400 uppercase tracking-widest bg-white/80 px-2 py-1 rounded">Product Preview</div>
            <div className="bg-white rounded-lg border shadow-sm p-6 grid grid-cols-1 md:grid-cols-3 gap-6 opacity-90 grayscale-[0.2]">
              <div className="col-span-1 space-y-4">
                <div className="h-48 bg-slate-100 rounded-md border flex items-center justify-center text-slate-400">Creative Thumbnail</div>
                <div className="space-y-2">
                  <div className="h-4 bg-slate-100 rounded w-1/2"></div>
                  <div className="h-4 bg-slate-100 rounded w-3/4"></div>
                </div>
              </div>
              <div className="col-span-2 space-y-6">
                <div className="flex items-center gap-4">
                  <div className="h-16 w-16 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-2xl font-bold">85</div>
                  <div>
                    <h3 className="text-lg font-semibold text-slate-900">Strong Engagement Potential</h3>
                    <p className="text-sm text-slate-500">Based on 6 deterministic heuristics.</p>
                  </div>
                </div>
                <div className="space-y-3">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center gap-4">
                      <div className="h-2 flex-1 bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full bg-blue-500 w-[80%]"></div>
                      </div>
                      <span className="text-xs text-slate-500 w-12 text-right">80 / 100</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Capabilities */}
      <section className="py-24 bg-slate-50">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-white p-6 rounded-xl border shadow-sm space-y-4">
              <div className="h-12 w-12 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center">
                <ScanText className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900">Multimodal Extraction</h3>
              <p className="text-slate-600 text-sm">Automatically extract text and layout from native PDFs, scanned documents, and images using PyMuPDF and Tesseract OCR.</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl border shadow-sm space-y-4">
              <div className="h-12 w-12 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center">
                <BarChart3 className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900">Explainable Scoring</h3>
              <p className="text-slate-600 text-sm">Evaluate content deterministically across 6 dimensions: Hook, Clarity, Specificity, Emotion, Interaction, and Call-to-Action.</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl border shadow-sm space-y-4">
              <div className="h-12 w-12 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center">
                <ShieldCheck className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900">Evidence & Provenance</h3>
              <p className="text-slate-600 text-sm">Every important signal can be traced back to exact extracted content blocks, ensuring complete transparency.</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl border shadow-sm space-y-4">
              <div className="h-12 w-12 rounded-lg bg-indigo-100 text-indigo-600 flex items-center justify-center">
                <Sparkles className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900">AI Strategy</h3>
              <p className="text-slate-600 text-sm">Gemini adds qualitative recommendations and rewrites while the deterministic analysis remains the ground truth.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-24 bg-white border-t">
        <div className="container mx-auto px-4 max-w-4xl text-center">
          <h2 className="text-3xl font-bold text-slate-900">How it works</h2>
          <p className="mt-4 text-slate-600">Deterministic analysis first. AI second.</p>
          
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 relative">
            <div className="hidden md:block absolute top-6 left-[12.5%] right-[12.5%] h-0.5 bg-slate-100 -z-10"></div>
            
            <div className="flex flex-col items-center">
              <div className="h-12 w-12 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-lg mb-4 shadow-md">1</div>
              <h4 className="font-semibold text-slate-900">Upload</h4>
              <p className="text-sm text-slate-500 mt-2">Submit your creative</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="h-12 w-12 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-lg mb-4 shadow-md">2</div>
              <h4 className="font-semibold text-slate-900">Extract</h4>
              <p className="text-sm text-slate-500 mt-2">Text, visual & metadata</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="h-12 w-12 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-lg mb-4 shadow-md">3</div>
              <h4 className="font-semibold text-slate-900">Profile</h4>
              <p className="text-sm text-slate-500 mt-2">Heuristic scoring</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="h-12 w-12 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-lg mb-4 shadow-md">4</div>
              <h4 className="font-semibold text-slate-900">Improve</h4>
              <p className="text-sm text-slate-500 mt-2">Evidence-backed recs</p>
            </div>
          </div>
          
          <div className="mt-20">
            <Link
              href="/analyze"
              className="inline-flex h-12 items-center justify-center rounded-md bg-blue-600 px-8 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700"
            >
              Analyze your first piece of content <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
