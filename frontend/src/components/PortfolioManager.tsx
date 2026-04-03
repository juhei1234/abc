// ABOUTME: Portfolio management widget for creating holdings and reviewing allocations.
// ABOUTME: Acts as starter UI for authenticated import/export and persistence workflows.
'use client';

import { FormEvent, useState } from 'react';

interface HoldingRow {
  ticker: string;
  weight: number;
}

export function PortfolioManager() {
  const [name, setName] = useState('Core Growth');
  const [rows, setRows] = useState<HoldingRow[]>([{ ticker: 'AAPL', weight: 25 }, { ticker: 'MSFT', weight: 25 }, { ticker: 'NVDA', weight: 50 }]);

  function addRow() {
    setRows([...rows, { ticker: '', weight: 0 }]);
  }

  function savePortfolio(e: FormEvent) {
    e.preventDefault();
    alert(`Portfolio '${name}' prepared with ${rows.length} holdings. Connect auth token + backend call in next iteration.`);
  }

  return (
    <div className="card">
      <h2>Portfolio Manager</h2>
      <form onSubmit={savePortfolio}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Portfolio name" />
        {rows.map((row, idx) => (
          <div key={`${idx}-${row.ticker}`} style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <input value={row.ticker} onChange={(e) => setRows(rows.map((r, i) => (i === idx ? { ...r, ticker: e.target.value.toUpperCase() } : r)))} placeholder="Ticker" />
            <input
              type="number"
              value={row.weight}
              onChange={(e) => setRows(rows.map((r, i) => (i === idx ? { ...r, weight: Number(e.target.value) } : r)))}
              placeholder="Weight %"
            />
          </div>
        ))}
        <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
          <button type="button" onClick={addRow}>Add Holding</button>
          <button type="submit">Save Portfolio</button>
        </div>
      </form>
    </div>
  );
}
