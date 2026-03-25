import type { ReactNode } from 'react';

type Props = {
  tone: 'good' | 'warn' | 'bad' | 'muted';
  children: ReactNode;
};

export function StatusPill({ tone, children }: Props) {
  return <span className={`pill ${tone}`}>{children}</span>;
}
