import { useMemo, useState } from 'react';
import type { Policies } from '../types';

type Props = {
  initial: Policies;
  onSave: (payload: Policies) => Promise<void>;
};

export function PoliciesView({ initial, onSave }: Props) {
  const [allowedActions, setAllowedActions] = useState(initial.allowedActions.join(', '));
  const [rulesJson, setRulesJson] = useState(JSON.stringify(initial.rules, null, 2));
  const [error, setError] = useState<string | null>(null);
  const [savedAt, setSavedAt] = useState<string | null>(null);

  const parsedPolicies = useMemo((): Policies | null => {
    try {
      const rules = JSON.parse(rulesJson);
      if (!Array.isArray(rules)) {
        throw new Error('Rules must be an array');
      }
      return {
        allowedActions: allowedActions
          .split(',')
          .map((item) => item.trim())
          .filter(Boolean),
        rules
      };
    } catch {
      return null;
    }
  }, [allowedActions, rulesJson]);

  async function handleSave() {
    if (!parsedPolicies) {
      setError('Invalid policy JSON.');
      return;
    }

    setError(null);
    await onSave(parsedPolicies);
    setSavedAt(new Date().toLocaleTimeString());
  }

  return (
    <section>
      <h2>Policies</h2>
      <label>
        Allowed actions (comma separated)
        <input value={allowedActions} onChange={(e) => setAllowedActions(e.target.value)} />
      </label>

      <label>
        Access rules (JSON)
        <textarea rows={12} value={rulesJson} onChange={(e) => setRulesJson(e.target.value)} />
      </label>

      <div className="row gap-sm">
        <button onClick={() => void handleSave()}>Save policies</button>
        {savedAt && <span>Saved at: {savedAt}</span>}
      </div>
      {error && <p className="error">{error}</p>}
    </section>
  );
}
