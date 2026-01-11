import { useState } from 'react';
import Upload from './components/Upload';
import Dashboard from './components/Dashboard';
import { uploadDocument } from './services/api';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [originalFile, setOriginalFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleUpload = async (file) => {
    setIsAnalyzing(true);
    setOriginalFile(file);

    try {
      const data = await uploadDocument(file);
      setAnalysisData(data.analysis);
      setDownloadUrl(data.download_url);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to analyze document. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setAnalysisData(null);
    setOriginalFile(null);
    setDownloadUrl(null);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-10 h-10 bg-brand-600 rounded-lg flex items-center justify-center text-white font-bold text-xl mr-3">R</div>
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">ResearchMate</h1>
          </div>
          <p className="text-sm text-gray-500 font-medium">AI-Powered Formatter & Tagger</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow">
        {!analysisData ? (
          <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-10">
              <h2 className="text-2xl font-semibold text-gray-800">Review & Format Your Paper in Seconds</h2>
              <p className="mt-2 text-gray-600">Upload your raw draft and let our AI standardized sections, fix references, and suggest keywords.</p>
            </div>
            <Upload onUploadSuccess={handleUpload} isAnalyzing={isAnalyzing} />
          </div>
        ) : (
          <Dashboard
            analysis={analysisData}
            originalFile={originalFile}
            downloadUrl={downloadUrl}
            onReset={handleReset}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-400">&copy; 2024 ResearchMate. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
