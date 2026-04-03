// ABOUTME: Root layout for the earnings platform app with shared stylesheet imports.
// ABOUTME: Provides shell metadata and wraps all pages in the Next.js app router.
import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Earnings Calendar Platform',
  description: 'Professional earnings calendar and portfolio analytics',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
