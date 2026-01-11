import React from 'react';

export default function Dashboard({ analysis, originalFile, downloadUrl, onReset }) {
    if (!analysis) return null;

    return (
        <div className="w-full max-w-6xl mx-auto mt-8 p-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Left: AI Analysis */}
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    <h2 className="text-2xl font-bold mb-4 text-blue-700">AI Analysis Report</h2>

                    <div className="mb-6">
                        <h3 className="text-lg font-semibold text-gray-800 mb-2">Suggested Title</h3>
                        <p className="p-3 bg-gray-50 rounded border border-gray-200 italic text-gray-700">{analysis.title}</p>
                    </div>

                    <div className="mb-6">
                        <h3 className="text-lg font-semibold text-gray-800 mb-2">Suggested Keywords</h3>
                        <div className="flex flex-wrap gap-2">
                            {(analysis.keywords || []).map((kw, idx) => (
                                <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                                    {kw}
                                </span>
                            ))}
                        </div>
                    </div>

                    <div className="mb-6">
                        <h3 className="text-lg font-semibold text-gray-800 mb-2">Identified Issues</h3>
                        {(!analysis.issues || analysis.issues.length === 0) ? (
                            <p className="text-green-600">No major issues found!</p>
                        ) : (
                            <ul className="space-y-2">
                                {(analysis.issues || []).map((issue, idx) => (
                                    <li key={idx} className="flex items-start p-3 bg-red-50 rounded border border-red-100">
                                        <span className="flex-shrink-0 w-2 h-2 mt-2 bg-red-500 rounded-full mr-3"></span>
                                        <div>
                                            <span className="text-xs font-bold text-red-600 uppercase block mb-1">{issue.type}</span>
                                            <span className="text-sm text-gray-700">{issue.description}</span>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>

                {/* Right: Actions & Preview */}
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 flex flex-col justify-between">
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-gray-800">Your Formatted Document</h2>
                        <p className="text-gray-600 mb-6">
                            The AI has re-formatted your document according to the journal standards (IEEE/ACM style base).
                            References have been checked and layout adjusted.
                        </p>

                        <div className="p-4 bg-blue-50 border border-blue-100 rounded mb-4">
                            <h4 className="font-semibold text-blue-800 mb-1">Files Ready:</h4>
                            <p className="text-sm text-blue-600">Original: {originalFile.name}</p>
                            {/* We could list the new file name too */}
                        </div>
                    </div>

                    <div className="flex flex-col gap-3">
                        <a
                            href={`http://localhost:8000${downloadUrl}`}
                            download
                            className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white text-center font-bold rounded-lg shadow transition-transform transform hover:scale-[1.02] flex items-center justify-center gap-2"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                            Download Formatted .DOCX
                        </a>

                        <button
                            onClick={onReset}
                            className="w-full py-3 bg-white text-gray-600 hover:bg-gray-50 border border-gray-300 font-semibold rounded-lg transition-colors"
                        >
                            Analyze Another Paper
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
