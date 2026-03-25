import type { Run } from '../types';
import { StatusPill } from '../components/StatusPill';

type Props = {
  runs: Run[];
  onRetry: (runId: string) => Promise<void>;
  onCancel: (runId: string) => Promise<void>;
  onApprove: (runId: string, stepId: string) => Promise<void>;
};

const statusTone: Record<string, 'good' | 'warn' | 'bad' | 'muted'> = {
  success: 'good',
  healthy: 'good',
  running: 'warn',
  degraded: 'warn',
  blocked: 'warn',
  failed: 'bad',
  canceled: 'muted',
  pending: 'muted',
  queued: 'muted'
};

export function RunsView({ runs, onRetry, onCancel, onApprove }: Props) {
  return (
    <section>
      <h2>Runs</h2>
      {runs.map((run) => (
        <article key={run.id} className="card">
          <header className="row between">
            <div>
              <h3>{run.workflow}</h3>
              <small>{run.id}</small>
            </div>
            <StatusPill tone={statusTone[run.status] ?? 'muted'}>{run.status}</StatusPill>
          </header>

          <div className="row gap-sm actions">
            <button onClick={() => void onRetry(run.id)}>Retry run</button>
            <button className="ghost" onClick={() => void onCancel(run.id)}>
              Cancel run
            </button>
          </div>

          <ol className="timeline">
            {run.steps.map((step) => (
              <li key={step.id}>
                <div className="row between">
                  <strong>{step.name}</strong>
                  <StatusPill tone={statusTone[step.status] ?? 'muted'}>{step.status}</StatusPill>
                </div>
                {step.error && <p className="error">Error: {step.error}</p>}
                <details>
                  <summary>Tool logs ({step.toolLogs.length})</summary>
                  <pre>{step.toolLogs.join('\n')}</pre>
                </details>
                {step.requiresApproval && step.status === 'blocked' && (
                  <button onClick={() => void onApprove(run.id, step.id)}>Manual approve</button>
                )}
              </li>
            ))}
          </ol>
        </article>
      ))}
    </section>
  );
}
