import React, { useEffect, useState } from 'react'

export const App: React.FC = () => {
  const [health, setHealth] = useState<string>('')
  useEffect(() => {
    fetch('http://localhost:8000/health').then(r => r.json()).then(j => setHealth(j.status))
  }, [])
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

      <div className="p-4 border rounded mt-4">Trade Log (placeholder)</div>
      <div className="p-4 border rounded mt-4">Control Center (placeholder)</div>
    </div>
  )
}