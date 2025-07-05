'use client';
import React, { useState } from 'react';
import axios from 'axios';

export default function Page() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!file || !question) {
      alert("Please upload a PDF and enter a question.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    try {
      const response = await axios.post("http://localhost:8000/ask", formData);
      setAnswer(response.data.answer);
      setSources(response.data.sources);
    } catch (error) {
      alert("Something went wrong while fetching the answer.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0e0e0e] text-white flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-3xl bg-[#1a1a1a] border border-orange-500 rounded-xl shadow-xl p-8">
        <h1 className="text-4xl font-bold text-center text-orange-500 mb-10 tracking-wide">
          📘 Ask Questions from Your PDF
        </h1>

        <div className="flex flex-col gap-5">
          <label className="text-sm uppercase font-semibold tracking-wide text-gray-300">Upload PDF</label>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="p-2 bg-white text-black rounded-lg file:border-none"
          />

          <label className="text-sm uppercase font-semibold tracking-wide text-gray-300">Your Question</label>
          <input
            type="text"
            placeholder="Type your question here..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="p-3 rounded-md text-white"
          />

          <button
            onClick={handleAsk}
            disabled={loading}
            className="mt-4 bg-orange-500 hover:bg-orange-600 transition-colors duration-300 px-6 py-3 rounded-md font-semibold text-white disabled:bg-gray-500"
          >
            {loading ? 'Thinking...' : 'Ask'}
          </button>
        </div>

        {answer && (
          <div className="mt-10 bg-white text-black rounded-lg p-6">
            <h2 className="text-2xl font-bold text-orange-600 mb-4">💡 Answer</h2>
            <p className="text-lg">{answer}</p>

            {sources.length > 0 && (
              <>
                <h3 className="mt-6 text-xl font-semibold text-gray-800">📚 Sources</h3>
                <ul className="list-disc ml-6 mt-2 text-sm space-y-1 text-gray-700">
                  {sources.map((src, idx) => (
                    <li key={idx}>{src}...</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
