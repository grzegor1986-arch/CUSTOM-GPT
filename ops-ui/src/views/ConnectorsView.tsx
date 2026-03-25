import type { Connector } from '../types';
import { StatusPill } from '../components/StatusPill';

type Props = {
  connectors: Connector[];
};

export function ConnectorsView({ connectors }: Props) {
  const toneForHealth = {
    healthy: 'good',
    degraded: 'warn',
    down: 'bad'
  } as const;

  const toneForAuth = {
    authorized: 'good',
    expired: 'warn',
    missing: 'bad'
  } as const;

  return (
    <section>
      <h2>Connectors</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Healthcheck</th>
            <th>Authorization</th>
            <th>Last check</th>
          </tr>
        </thead>
        <tbody>
          {connectors.map((connector) => (
            <tr key={connector.id}>
              <td>{connector.name}</td>
              <td>{connector.type}</td>
              <td>
                <StatusPill tone={toneForHealth[connector.health]}>{connector.health}</StatusPill>
              </td>
              <td>
                <StatusPill tone={toneForAuth[connector.authStatus]}>{connector.authStatus}</StatusPill>
              </td>
              <td>{new Date(connector.lastCheckAt).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
