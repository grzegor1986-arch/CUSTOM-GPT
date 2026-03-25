export type RunStep = {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'success' | 'failed' | 'blocked' | 'canceled';
  startedAt?: string;
  endedAt?: string;
  error?: string;
  toolLogs: string[];
  requiresApproval?: boolean;
};

export type Run = {
  id: string;
  workflow: string;
  status: 'queued' | 'running' | 'success' | 'failed' | 'canceled';
  startedAt: string;
  endedAt?: string;
  steps: RunStep[];
};

export type Connector = {
  id: string;
  name: string;
  type: string;
  health: 'healthy' | 'degraded' | 'down';
  authStatus: 'authorized' | 'expired' | 'missing';
  lastCheckAt: string;
};

export type PolicyRule = {
  id: string;
  subject: string;
  resource: string;
  condition?: string;
  effect: 'allow' | 'deny';
};

export type Policies = {
  allowedActions: string[];
  rules: PolicyRule[];
};

export type KPI = {
  averageDurationMs: number;
  successRate: number;
  mostUsedTools: Array<{ tool: string; count: number }>;
};
