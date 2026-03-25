import type { KPI } from '../types';

type Props = {
  kpi: KPI;
};

export function KpiView({ kpi }: Props) {
  return (
    <section>
      <h2>Dashboard KPI</h2>
      <div className="kpi-grid">
        <article className="card">
          <h3>Execution time</h3>
          <p>{Math.round(kpi.averageDurationMs / 1000)} s (avg)</p>
        </article>
        <article className="card">
          <h3>Success rate</h3>
          <p>{(kpi.successRate * 100).toFixed(1)}%</p>
        </article>
        <article className="card">
          <h3>Top tools</h3>
          <ul>
            {kpi.mostUsedTools.map((tool) => (
              <li key={tool.tool}>
                {tool.tool}: {tool.count}
              </li>
            ))}
          </ul>
        </article>
      </div>
    </section>
  );
}
