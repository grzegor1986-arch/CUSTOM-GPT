import { useEffect, useState } from 'react';
import {
  approveStep,
  cancelRun,
  fetchConnectors,
  fetchKpis,
  fetchPolicies,
  fetchRuns,
  retryRun,
  savePolicies
} from './api';
import { mockConnectors, mockKpi, mockPolicies, mockRuns } from './mockData';
import type { Connector, KPI, Policies, Run } from './types';
import { ConnectorsView } from './views/ConnectorsView';
import { KpiView } from './views/KpiView';
import { PoliciesView } from './views/PoliciesView';
import { RunsView } from './views/RunsView';

type Tab = 'runs' | 'connectors' | 'policies' | 'kpi';

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('runs');
  const [runs, setRuns] = useState<Run[]>([]);
  const [connectors, setConnectors] = useState<Connector[]>([]);
  const [policies, setPolicies] = useState<Policies | null>(null);
  const [kpi, setKpi] = useState<KPI | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    try {
      const [r, c, p, k] = await Promise.all([fetchRuns(), fetchConnectors(), fetchPolicies(), fetchKpis()]);
      setRuns(r);
      setConnectors(c);
      setPolicies(p);
      setKpi(k);
    } catch {
      setError('Cannot connect to orchestrator API, fallback to mock data.');
      setRuns(mockRuns);
      setConnectors(mockConnectors);
      setPolicies(mockPolicies);
      setKpi(mockKpi);
    } finally {
      setLoading(false);
    }
  }

  async function handleRetry(runId: string) {
    await retryRun(runId).catch(() => undefined);
    await loadData();
  }

  async function handleCancel(runId: string) {
    await cancelRun(runId).catch(() => undefined);
    await loadData();
  }

  async function handleApprove(runId: string, stepId: string) {
    await approveStep(runId, stepId).catch(() => undefined);
    await loadData();
  }

  async function handleSavePolicies(payload: Policies) {
    await savePolicies(payload).catch(() => undefined);
    setPolicies(payload);
  }

  return (
    <div className="layout">
      <header>
        <h1>Ops UI / Orchestrator Console</h1>
        <p>Frontend connected to orchestrator API (`/api/*`).</p>
      </header>

      <nav className="tabs">
        <button className={activeTab === 'runs' ? 'active' : ''} onClick={() => setActiveTab('runs')}>
          Runs
        </button>
        <button className={activeTab === 'connectors' ? 'active' : ''} onClick={() => setActiveTab('connectors')}>
          Connectors
        </button>
        <button className={activeTab === 'policies' ? 'active' : ''} onClick={() => setActiveTab('policies')}>
          Policies
        </button>
        <button className={activeTab === 'kpi' ? 'active' : ''} onClick={() => setActiveTab('kpi')}>
          KPI
        </button>
      </nav>

      {loading && <p>Loading data...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && activeTab === 'runs' && <RunsView runs={runs} onRetry={handleRetry} onCancel={handleCancel} onApprove={handleApprove} />}
      {!loading && activeTab === 'connectors' && <ConnectorsView connectors={connectors} />}
      {!loading && activeTab === 'policies' && policies && <PoliciesView initial={policies} onSave={handleSavePolicies} />}
      {!loading && activeTab === 'kpi' && kpi && <KpiView kpi={kpi} />}
    </div>
  );
}
