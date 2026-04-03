// ABOUTME: Security detail panel with valuation metrics, analyst mix, and earnings trends.
// ABOUTME: Renders selected stock fundamentals and forward consensus figures.
'use client';

import { useEffect, useState } from 'react';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

import { getSecurity, SecurityOverview } from '@/lib/api';

export function SecurityOverviewPanel({ ticker }: { ticker: string }) {
  const [data, setData] = useState<SecurityOverview | null>(null);

  useEffect(() => {
    getSecurity(ticker)
      .then(setData)
      .catch(() => setData(null));
  }, [ticker]);

  if (!data) return <div className="card">Select a security to view details.</div>;

  const surprises = data.surprise_history.map((value, idx) => ({ q: `Q-${idx + 1}`, value }));

  return (
    <div className="card">
      <h2>{data.ticker} Overview</h2>
      <p>P/E {data.pe_ratio} · Fwd P/E {data.forward_pe} · P/S {data.price_to_sales} · P/B {data.price_to_book} · EV/EBITDA {data.ev_to_ebitda}</p>
      <p>Ratings: Buy {data.analyst_buy} / Hold {data.analyst_hold} / Sell {data.analyst_sell}</p>
      <p>Targets: {data.target_low} - {data.target_mean} - {data.target_high}</p>
      <p>Forward EPS: {data.forward_eps_consensus} · Forward Revenue: {data.forward_revenue_consensus}</p>
      <div style={{ width: '100%', height: 180 }}>
        <ResponsiveContainer>
          <LineChart data={surprises}>
            <XAxis dataKey="q" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#1f2937" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
