'use client';

import { useState, useRef } from 'react';
import { CanvasOverlay } from '@/components/CanvasOverlay';
import { InferResponse, Page } from '@/lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<InferResponse | null>(null);
  const [showTranslation, setShowTranslation] = useState(true);
  const [sourceLanguage, setSourceLanguage] = useState('kan_Knda');
  const [targetLanguage, setTargetLanguage] = useState('eng_Latn');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = (ev) => {
      setPreview(ev.target?.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    try {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64 = (e.target?.result as string).split(',')[1];

        const response = await fetch(`${API_BASE_URL}/infer`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image_b64: base64,
            language: sourceLanguage,
            target_language: targetLanguage,
          }),
        });

        const data: InferResponse = await response.json();

        if (data.success) {
          setResult(data);
        } else {
          alert(`Error: ${data.error}`);
        }
      };
      reader.readAsDataURL(selectedFile);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload image');
    } finally {
      setLoading(false);
    }
  };

  const canvasWidth = result?.pages[0]?.width || 600;
  const canvasHeight = result?.pages[0]?.height || 800;
  const lines = result?.pages[0]?.lines || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-2">
          OCR + Translation
        </h1>
        <p className="text-center text-gray-600 mb-8">
          Upload an image to extract and translate text with live canvas overlay
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">Upload Image</h2>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Source Language
              </label>
              <select
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="kan_Knda">Kannada</option>
                <option value="hin_Deva">Hindi</option>
                <option value="ben_Beng">Bengali</option>
                <option value="tam_Tamil">Tamil</option>
                <option value="tel_Telu">Telugu</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Language
              </label>
              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="eng_Latn">English</option>
              </select>
            </div>

            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center mb-4 cursor-pointer hover:border-blue-500 transition"
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
              />
              {preview ? (
                <div className="text-center">
                  <img src={preview} alt="Preview" className="h-48 mx-auto rounded mb-2" />
                  <p className="text-sm text-gray-600">{selectedFile?.name}</p>
                </div>
              ) : (
                <div>
                  <p className="text-gray-600 font-medium">Click to upload image</p>
                  <p className="text-sm text-gray-500 mt-1">PNG, JPG, GIF up to 10MB</p>
                </div>
              )}
            </div>

            <button
              onClick={handleUpload}
              disabled={!selectedFile || loading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition"
            >
              {loading ? 'Processing...' : 'Extract & Translate'}
            </button>
          </div>

          {/* Results Section */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">Results</h2>

            {result && (
              <div className="space-y-4">
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="text-sm text-gray-600">
                    ⏱️ Processing time: <strong>{result.processing_time.toFixed(2)}s</strong>
                  </p>
                  <p className="text-sm text-gray-600">
                    📝 Lines detected: <strong>{lines.length}</strong>
                  </p>
                </div>

                <div className="flex items-center justify-between bg-blue-50 p-3 rounded-lg">
                  <label className="text-sm font-medium text-gray-700">Show Translation</label>
                  <button
                    onClick={() => setShowTranslation(!showTranslation)}
                    className={`px-4 py-2 rounded-lg font-semibold transition ${
                      showTranslation
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-300 text-gray-800'
                    }`}
                  >
                    {showTranslation ? 'Translation' : 'Original'}
                  </button>
                </div>

                <div className="max-h-96 overflow-y-auto bg-gray-50 p-3 rounded-lg border border-gray-200">
                  <h3 className="font-semibold text-gray-800 mb-2">
                    {showTranslation ? 'Translated Text' : 'Original Text'}
                  </h3>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {showTranslation ? result.translated_text : result.text}
                  </p>
                </div>
              </div>
            )}

            {!result && (
              <div className="text-center text-gray-500 py-12">
                <p>Upload an image to see results</p>
              </div>
            )}
          </div>
        </div>

        {/* Canvas Overlay Section */}
        {result && lines.length > 0 && (
          <div className="mt-8 bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">
              Live Canvas Overlay - {showTranslation ? 'Translation' : 'Original'}
            </h2>
            <div className="overflow-x-auto">
              <CanvasOverlay
                imageFile={selectedFile!}
                lines={lines}
                showTranslation={showTranslation}
                canvasWidth={Math.min(canvasWidth, 1000)}
                canvasHeight={(Math.min(canvasWidth, 1000) / canvasWidth) * canvasHeight}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
