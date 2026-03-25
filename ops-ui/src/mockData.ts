import type { Connector, KPI, Policies, Run } from './types';

export const mockRuns: Run[] = [
  {
    id: 'run-193',
    workflow: 'customer-onboarding',
    status: 'failed',
    startedAt: new Date(Date.now() - 16 * 60_000).toISOString(),
    endedAt: new Date(Date.now() - 4 * 60_000).toISOString(),
    steps: [
      {
        id: 's1',
        name: 'Collect CRM data',
        status: 'success',
        startedAt: new Date(Date.now() - 16 * 60_000).toISOString(),
        endedAt: new Date(Date.now() - 14 * 60_000).toISOString(),
        toolLogs: ['crm.fetchCustomer: 200 OK', 'crm.normalizeRecord: 1 warning']
      },
      {
        id: 's2',
        name: 'Credit risk check',
        status: 'blocked',
        startedAt: new Date(Date.now() - 13 * 60_000).toISOString(),
        requiresApproval: true,
        toolLogs: ['risk.score: score=0.89', 'requires manual approval due policy: risk>0.8']
      },
      {
        id: 's3',
        name: 'Issue contract',
        status: 'failed',
        startedAt: new Date(Date.now() - 9 * 60_000).toISOString(),
        endedAt: new Date(Date.now() - 4 * 60_000).toISOString(),
        error: 'Connector DocuSign timeout after 3 retries',
        toolLogs: ['contract.render: ok', 'docusign.send: timeout', 'docusign.send: timeout', 'docusign.send: timeout']
      }
    ]
  }
];

export const mockConnectors: Connector[] = [
  {
    id: 'c1',
    name: 'Salesforce',
    type: 'CRM',
    health: 'healthy',
    authStatus: 'authorized',
    lastCheckAt: new Date(Date.now() - 2 * 60_000).toISOString()
  },
  {
    id: 'c2',
    name: 'DocuSign',
    type: 'Signature',
    health: 'degraded',
    authStatus: 'authorized',
    lastCheckAt: new Date(Date.now() - 6 * 60_000).toISOString()
  },
  {
    id: 'c3',
    name: 'NetSuite',
    type: 'ERP',
    health: 'down',
    authStatus: 'expired',
    lastCheckAt: new Date(Date.now() - 9 * 60_000).toISOString()
  }
];

export const mockPolicies: Policies = {
  allowedActions: ['run.retry', 'run.cancel', 'step.approve'],
  rules: [
    {
      id: 'r1',
      subject: 'role:operator',
      resource: 'workflow:*',
      effect: 'allow'
    },
    {
      id: 'r2',
      subject: 'role:operator',
      resource: 'step:sensitive',
      condition: 'requiresMFA == true',
      effect: 'allow'
    },
    {
      id: 'r3',
      subject: 'role:viewer',
      resource: 'run:*',
      effect: 'deny'
    }
  ]
};

export const mockKpi: KPI = {
  averageDurationMs: 184_000,
  successRate: 0.93,
  mostUsedTools: [
    { tool: 'crm.fetchCustomer', count: 126 },
    { tool: 'risk.score', count: 115 },
    { tool: 'docusign.send', count: 101 }
  ]
};
