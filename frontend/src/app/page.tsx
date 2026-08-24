import { UploadZone } from '@/components/upload/UploadZone';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] p-4">
      <div className="w-full max-w-2xl mx-auto space-y-12">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Analyze your social content
          </h2>
          <p className="text-lg text-slate-500">
            Extract. Profile. Score. Improve.
          </p>
        </div>
        
        <UploadZone />
      </div>
    </div>
  );
}
