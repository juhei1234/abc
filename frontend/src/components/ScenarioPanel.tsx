// ABOUTME: Scenario analysis UI for macro shocks and benchmark comparison outputs.
// ABOUTME: Presents configurable assumptions with immediate simulated risk metrics.
'use client';

import { useMemo, useState } from 'react';

export function ScenarioPanel() {
  const [yieldShift, setYieldShift] = useState(-25);
  const [rateShift, setRateShift] = useState(-25);
  const [inflationShift, setInflationShift] = useState(10);
  const [sectorShock, setSectorShock] = useState(4);

  const projection = useMemo(() => {
    const projected = -0.02 * (yieldShift / 100) - 0.015 * (rateShift / 100) - 0.01 * (inflationShift / 100) + sectorShock / 100;
    const returnPct = projected * 100;
    const vol = 12 + Math.abs(rateShift) * 0.01;
    return {
      projected: returnPct.toFixed(2),
      var95: (1.65 * vol).toFixed(2),
      sharpe: (returnPct / vol).toFixed(2),
      benchmark: (returnPct * 0.85).toFixed(2),
    };
  }, [yieldShift, rateShift, inflationShift, sectorShock]);

  return (
    <div className="card">
      <h2>Macro Scenario Simulator</h2>
      <label>US Treasury yield change (bps): <input type="number" value={yieldShift} onChange={(e) => setYieldShift(Number(e.target.value))} /></label><br />
      <label>Fed rate change (bps): <input type="number" value={rateShift} onChange={(e) => setRateShift(Number(e.target.value))} /></label><br />
      <label>Inflation change (bps): <input type="number" value={inflationShift} onChange={(e) => setInflationShift(Number(e.target.value))} /></label><br />
      <label>Sector shock (%): <input type="number" value={sectorShock} onChange={(e) => setSectorShock(Number(e.target.value))} /></label>
      <p>Projected Return: {projection.projected}%</p>
      <p>VaR 95: {projection.var95}%</p>
      <p>Sharpe: {projection.sharpe}</p>
      <p>Benchmark: {projection.benchmark}%</p>
    </div>
  );
}
