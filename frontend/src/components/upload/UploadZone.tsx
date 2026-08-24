'use client';

import { useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { UploadCloud, FileType, Loader2 } from 'lucide-react';
import { config } from '@/lib/config';
import { analyzeFile } from '@/lib/api';
import { Button } from '@/components/ui/button';

export function UploadZone() {
  const router = useRouter();
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string | null => {
    if (!config.ALLOWED_MIMETYPES.includes(file.type)) {
      return `Unsupported file type. Please upload PDF, PNG, JPG, JPEG, or WEBP.`;
    }
    const fileSizeMB = file.size / (1024 * 1024);
    if (fileSizeMB > config.MAX_FILE_SIZE_MB) {
      return `File exceeds maximum size of ${config.MAX_FILE_SIZE_MB}MB.`;
    }
    return null;
  };

  const handleFile = useCallback((file: File) => {
    setError(null);
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }
    setSelectedFile(file);
  }, []);

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, [handleFile]);

  const handleUpload = async () => {
    if (!selectedFile) return;
    
    try {
      setIsUploading(true);
      setError(null);
      const data = await analyzeFile(selectedFile);
      router.push(`/analysis/${data.analysis_id}`);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to upload and analyze file');
      }
      setIsUploading(false);
    }
  };

  if (selectedFile) {
    return (
      <div className="flex flex-col items-center justify-center border-2 border-slate-200 rounded-lg p-8 bg-white max-w-md w-full mx-auto shadow-sm">
        <FileType className="w-12 h-12 text-primary mb-4" />
        <h3 className="text-lg font-medium text-slate-900 truncate w-full text-center px-4">
          {selectedFile.name}
        </h3>
        <p className="text-sm text-slate-500 mb-6">
          {selectedFile.type.split('/')[1].toUpperCase()} · {(selectedFile.size / (1024 * 1024)).toFixed(1)} MB
        </p>
        
        {error && (
          <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md w-full text-center mb-4">
            {error}
          </div>
        )}

        <div className="flex flex-col w-full gap-3">
          <Button 
            onClick={handleUpload} 
            disabled={isUploading}
            className="w-full"
          >
            {isUploading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Uploading...
              </>
            ) : (
              'Analyze Content'
            )}
          </Button>
          <Button 
            variant="outline" 
            onClick={() => setSelectedFile(null)}
            disabled={isUploading}
            className="w-full"
          >
            Remove
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-md mx-auto">
      <div 
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-10 cursor-pointer transition-colors ${
          isDragging ? 'border-primary bg-primary/5' : 'border-slate-300 hover:border-primary/50 hover:bg-slate-50'
        } bg-white`}
      >
        <UploadCloud className="w-12 h-12 text-slate-400 mb-4" />
        <h3 className="text-lg font-medium text-slate-900 mb-1">
          {isDragging ? 'Drop file to analyze' : 'Upload your content'}
        </h3>
        <p className="text-sm text-slate-500 text-center mb-6">
          Drag & drop your file here<br/>or <span className="text-primary font-medium">Browse files</span>
        </p>
        
        <div className="text-xs text-slate-400 text-center space-y-1">
          <p>PDF · PNG · JPG · WEBP</p>
          <p>Max {config.MAX_FILE_SIZE_MB} MB</p>
        </div>

        <input 
          type="file" 
          ref={fileInputRef} 
          className="hidden" 
          accept={config.ALLOWED_EXTENSIONS.join(',')}
          onChange={(e) => {
            if (e.target.files && e.target.files.length > 0) {
              handleFile(e.target.files[0]);
            }
          }}
        />
      </div>
      
      {error && (
        <div className="mt-4 text-sm text-red-600 bg-red-50 p-3 rounded-md text-center">
          {error}
        </div>
      )}
    </div>
  );
}
