import React, { useEffect, useState } from 'react'

export const App: React.FC = () => {
  const [health, setHealth] = useState<string>('')
  const [fromDate, setFromDate] = useState<string>('')
  const [toDate, setToDate] = useState<string>('')
  const [symbols, setSymbols] = useState<string>('')
  const [results, setResults] = useState<any | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')
  useEffect(() => {
    fetch('http://localhost:8000/health').then(r => r.json()).then(j => setHealth(j.status))
  }, [])

  const runBacktest = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResults(null)
    try {
      const resp = await fetch('http://localhost:8000/backtest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from_date: fromDate,
          to_date: toDate || 'today',
          symbols: symbols.split(',').map(s => s.trim()).filter(Boolean)
        })
      })
      if (!resp.ok) throw new Error('Request failed')
      setResults(await resp.json())
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="p-4 font-sans">
      <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4">
        <p className="font-bold">No Financial Advice</p>
        <p>Trade at Your Own Risk.</p>
      </div>
      <h1 className="text-2xl font-bold mb-2">MarketSage-Pro</h1>
      <p className="text-sm text-gray-600 mb-6">API health: {health || '...'}</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 border rounded">Ticker Cards (placeholder)</div>
        <div className="p-4 border rounded">Mini-chart (placeholder)</div>
        <div className="p-4 border rounded">IVR Meter (placeholder)</div>
      </div>

      <form onSubmit={runBacktest} className="p-4 border rounded mt-4 space-y-2">
        <div className="flex flex-col">
          <label className="text-sm">From Date</label>
          <input className="border p-1" type="date" value={fromDate} onChange={e => setFromDate(e.target.value)} required />
        </div>
        <div className="flex flex-col">
          <label className="text-sm">To Date</label>
          <input className="border p-1" type="date" value={toDate} onChange={e => setToDate(e.target.value)} />
        </div>
        <div className="flex flex-col">
          <label className="text-sm">Symbols (comma separated)</label>
          <input className="border p-1" value={symbols} onChange={e => setSymbols(e.target.value)} required />
        </div>
        <button className="bg-blue-500 text-white px-3 py-1 rounded" type="submit" disabled={loading}>
          {loading ? 'Running...' : 'Run Backtest'}
        </button>
        {error && <p className="text-red-500 text-sm">{error}</p>}
      </form>

      {results && (
        <div className="p-4 border rounded mt-4">
          <h2 className="font-bold mb-2">Backtest Results</h2>
          <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}