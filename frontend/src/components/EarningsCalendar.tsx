// ABOUTME: Interactive earnings calendar table with index filters and daily grouping.
// ABOUTME: Supports dense event display and stock selection callbacks.
'use client';

import { useEffect, useMemo, useState } from 'react';

import { EarningsEvent, getEarnings } from '@/lib/api';

export function EarningsCalendar({ onSelect }: { onSelect: (ticker: string) => void }) {
  const [index, setIndex] = useState('sp500');
  const [events, setEvents] = useState<EarningsEvent[]>([]);

  useEffect(() => {
    const start = new Date();
    const end = new Date();
    end.setDate(start.getDate() + 30);
    getEarnings(index, start.toISOString().slice(0, 10), end.toISOString().slice(0, 10))
      .then(setEvents)
      .catch(() => setEvents([]));
  }, [index]);

  const grouped = useMemo(() => {
    return events.reduce<Record<string, EarningsEvent[]>>((acc, event) => {
      acc[event.date] = [...(acc[event.date] || []), event];
      return acc;
    }, {});
  }, [events]);

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Earnings Calendar</h2>
        <select value={index} onChange={(e) => setIndex(e.target.value)}>
          <option value="sp500">S&P 500</option>
          <option value="nasdaq100">NASDAQ-100</option>
          <option value="dow30">Dow 30</option>
        </select>
      </div>
      <p>Total events: {events.length}</p>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Events</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(grouped).map(([day, dayEvents]) => (
            <tr key={day}>
              <td>{day}</td>
              <td>
                <details>
                  <summary>{dayEvents.length} stocks</summary>
                  {dayEvents.map((event) => (
                    <div key={event.ticker}>
                      <button onClick={() => onSelect(event.ticker)}>{event.ticker}</button> · EPS est {event.eps_estimate ?? 'n/a'}
                    </div>
                  ))}
                </details>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
