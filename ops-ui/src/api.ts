import type { Connector, KPI, Policies, Run } from './types';

const jsonHeaders = {
  'Content-Type': 'application/json'
};

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchRuns(): Promise<Run[]> {
  return parseResponse<Run[]>(await fetch('/api/runs'));
}

export async function retryRun(runId: string): Promise<void> {
  const response = await fetch(`/api/runs/${runId}/retry`, { method: 'POST', headers: jsonHeaders });
  if (!response.ok) throw new Error('Retry failed');
}

export async function cancelRun(runId: string): Promise<void> {
  const response = await fetch(`/api/runs/${runId}/cancel`, { method: 'POST', headers: jsonHeaders });
  if (!response.ok) throw new Error('Cancel failed');
}

export async function approveStep(runId: string, stepId: string): Promise<void> {
  const response = await fetch(`/api/runs/${runId}/steps/${stepId}/approve`, {
    method: 'POST',
    headers: jsonHeaders
  });
  if (!response.ok) throw new Error('Approve failed');
}

export async function fetchConnectors(): Promise<Connector[]> {
  return parseResponse<Connector[]>(await fetch('/api/connectors'));
}

export async function fetchPolicies(): Promise<Policies> {
  return parseResponse<Policies>(await fetch('/api/policies'));
}

export async function savePolicies(payload: Policies): Promise<void> {
  const response = await fetch('/api/policies', {
    method: 'PUT',
    headers: jsonHeaders,
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error('Save policies failed');
}

export async function fetchKpis(): Promise<KPI> {
  return parseResponse<KPI>(await fetch('/api/kpi'));
}
