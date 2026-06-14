import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function DeployForm() {
  const [repoUrl, setRepoUrl] = useState('');
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: repoUrl }),
      });

      const data = await response.json();
      
      // Add this strict check: If Python sent back an error key, force the UI to fail
      if (data.error) {
        throw new Error(data.error);
      }
      
      setResult(data);
      setStatus('success');
    } catch (error) {
      console.error(error);
      // We can even display the specific error message now!
      setResult({ message: error.message });
      setStatus('error');
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-20 p-8 bg-slate-800 rounded-xl shadow-lg border border-slate-700 w-full">
      <h2 className="text-2xl font-bold text-white mb-2">Deploy a New Service</h2>
      <p className="text-slate-400 mb-6">Paste a GitHub repository URL to auto-detect and deploy.</p>
      
      <form onSubmit={handleSubmit} className="flex gap-4 mb-6">
        <input
          type="url"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          placeholder="https://github.com/username/repo"
          required
          className="flex-1 bg-slate-900 text-white border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
        />
        <button
          type="submit"
          disabled={status === 'loading'}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white font-semibold px-6 py-3 rounded-lg transition-colors min-w-[120px]"
        >
          {status === 'loading' ? 'Scanning...' : 'Detect'}
        </button>
      </form>

      {/* Result Display Area */}
      {status === 'success' && result && (
        <div className="bg-slate-900 p-4 rounded-lg border border-green-500/30 w-full mt-6 text-left">
          <h3 className="text-green-400 font-semibold mb-4 text-lg">Infrastructure Generated Successfully!</h3>
          
          <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div className="bg-slate-800 p-3 rounded border border-slate-700">
              <span className="text-slate-400 block mb-1">Detected Runtime</span>
              <span className="text-white font-mono">{result.stack_detected.runtime}</span>
            </div>
            <div className="bg-slate-800 p-3 rounded border border-slate-700">
              <span className="text-slate-400 block mb-1">Framework</span>
              <span className="text-white font-mono">{result.stack_detected.framework}</span>
            </div>
          </div>

          <div className="mt-4">
            <span className="text-slate-400 text-sm block mb-2">Generated Kubernetes Manifest:</span>
            <SyntaxHighlighter 
              language="yaml" 
              style={vscDarkPlus}
              className="rounded-lg text-sm border border-slate-700"
              customStyle={{ padding: '1.5rem', margin: 0 }}
            >
              {result.manifest_preview}
            </SyntaxHighlighter>
          </div>
        </div>
      )}

      {status === 'error' && (
        <div className="bg-red-900/20 p-4 rounded-lg border border-red-500/30">
          <p className="text-red-400">Failed to connect to the deployment engine. Is the backend running?</p>
        </div>
      )}
    </div>
  );
}