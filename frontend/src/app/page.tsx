// ABOUTME: Main SPA page composing earnings calendar, security details, and analytics panels.
// ABOUTME: Delivers data-dense professional dashboard optimized for desktop and mobile.
'use client';

import { useState } from 'react';

import { EarningsCalendar } from '@/components/EarningsCalendar';
import { PortfolioManager } from '@/components/PortfolioManager';
import { ScenarioPanel } from '@/components/ScenarioPanel';
import { SecurityOverviewPanel } from '@/components/SecurityOverviewPanel';

export default function HomePage() {
  const [ticker, setTicker] = useState('AAPL');

  return (
    <main className="container">
      <h1>Earnings Calendar & Portfolio Analytics</h1>
      <div className="grid grid-3">
        <EarningsCalendar onSelect={setTicker} />
        <SecurityOverviewPanel ticker={ticker} />
        <ScenarioPanel />
      </div>
      <div className="grid" style={{ marginTop: '1rem' }}>
        <PortfolioManager />
      </div>
    </main>
  );
}
