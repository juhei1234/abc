// ABOUTME: Lightweight frontend API client wrapping backend market and portfolio endpoints.
// ABOUTME: Centralizes fetch logic and auth token handling for SPA components.
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export interface EarningsEvent {
  ticker: string;
  company_name: string;
  date: string;
  eps_estimate: number | null;
  eps_actual: number | null;
  surprise_pct: number | null;
  sector: string | null;
  market_cap: number | null;
}

export interface SecurityOverview {
  ticker: string;
  pe_ratio: number | null;
  forward_pe: number | null;
  price_to_sales: number | null;
  price_to_book: number | null;
  ev_to_ebitda: number | null;
  analyst_buy: number;
  analyst_hold: number;
  analyst_sell: number;
  target_low: number | null;
  target_mean: number | null;
  target_high: number | null;
  forward_eps_consensus: number | null;
  forward_revenue_consensus: number | null;
  surprise_history: number[];
}

export async function getEarnings(index: string, start: string, end: string): Promise<EarningsEvent[]> {
  const res = await fetch(`${API_BASE}/api/market/earnings?index=${index}&start=${start}&end=${end}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load earnings calendar');
  return res.json();
}

export async function getSecurity(ticker: string): Promise<SecurityOverview> {
  const res = await fetch(`${API_BASE}/api/market/security/${ticker}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load security');
  return res.json();
}
