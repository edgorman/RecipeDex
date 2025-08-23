import React from 'react';
import { api, BASE_URL } from '../api/client';
import { getAuth } from 'firebase/auth';

function Section({ title, children }) {
  return (
    <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, marginBottom: 16 }}>
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      {children}
    </div>
  );
}

function JsonView({ data }) {
  return (
    <pre style={{ background: '#f7f7f7', padding: 12, borderRadius: 6, overflow: 'auto' }}>
      {data == null ? '—' : JSON.stringify(data, null, 2)}
    </pre>
  );
}

export default function EngineeringConsole() {
  const [state, setState] = React.useState({});

  const run = async (key, fn) => {
    setState((s) => ({ ...s, [key]: { loading: true } }));
    try {
      const data = await fn();
      setState((s) => ({ ...s, [key]: { data } }));
    } catch (err) {
      setState((s) => ({ ...s, [key]: { error: { message: err.message, status: err.status, body: err.body } } }));
    }
  };

  const [listPage, setListPage] = React.useState(0);
  const [listPageSize, setListPageSize] = React.useState(25);
  const [recipeId, setRecipeId] = React.useState('');
  const [createdId, setCreatedId] = React.useState('');
  const [createName, setCreateName] = React.useState('');
  const [recipeResultKey, setRecipeResultKey] = React.useState(null);

  // WebSocket state for Recipe Messages
  const [ws, setWs] = React.useState(null);
  const [wsConnected, setWsConnected] = React.useState(false);
  const [wsLog, setWsLog] = React.useState([]);
  const [wsMessage, setWsMessage] = React.useState('');

  const auth = getAuth();
  const [user, setUser] = React.useState(auth.currentUser);
  React.useEffect(() => auth.onAuthStateChanged(setUser), [auth]);

  const panel = (key) => state[key] || {};

  React.useEffect(() => {
    // If logged in, try to resolve their app user id via provider mapping
    (async () => {
      if (!user) return;
      try {
        const res = await api.getUserByProvider('firebase', user.uid);
        setState((s) => ({ ...s, currentAppUser: { data: res?.data || res } }));
      } catch (e) {
        setState((s) => ({ ...s, currentAppUser: { error: { message: e.message, status: e.status, body: e.body } } }));
      }
    })();
  }, [user]);

  // Cleanup WebSocket on unmount or recipe change
  React.useEffect(() => {
    return () => {
      try { ws?.close(); } catch {}
    };
  }, [ws]);

  async function connectWs() {
    if (!recipeId) {
      setWsLog((l) => [...l, { type: 'error', message: 'Provide recipe_id before connecting' }]);
      return;
    }
    try {
      const base = new URL(`/recipe/${encodeURIComponent(recipeId)}/message`, BASE_URL);
      base.protocol = base.protocol === 'https:' ? 'wss:' : 'ws:';
      const idToken = await auth.currentUser?.getIdToken();
      if (idToken) {
        base.searchParams.set('authorization', `Bearer ${idToken}`);
        base.searchParams.set('authorization_provider', 'firebase');
      }
      const socket = new WebSocket(base.toString());
      socket.onopen = () => {
        setWsConnected(true);
        setWsLog((l) => [...l, { type: 'open', at: new Date().toISOString() }]);
      };
      socket.onmessage = (ev) => {
        let data;
        try { data = JSON.parse(ev.data); } catch { data = ev.data; }
        setWsLog((l) => [...l, { type: 'message', at: new Date().toISOString(), data }]);
      };
      socket.onerror = (ev) => {
        setWsLog((l) => [...l, { type: 'error', at: new Date().toISOString(), data: String(ev?.message || 'ws error') }]);
      };
      socket.onclose = () => {
        setWsConnected(false);
        setWsLog((l) => [...l, { type: 'close', at: new Date().toISOString() }]);
      };
      setWs(socket);
    } catch (e) {
      setWsLog((l) => [...l, { type: 'error', at: new Date().toISOString(), data: e?.message }]);
    }
  }

  function disconnectWs() {
    try { ws?.close(); } catch {}
    setWs(null);
  }

  function sendWs() {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      setWsLog((l) => [...l, { type: 'error', message: 'WebSocket not connected' }]);
      return;
    }
    const payload = { value: wsMessage };
    ws.send(JSON.stringify(payload));
    setWsLog((l) => [...l, { type: 'sent', at: new Date().toISOString(), data: payload }]);
    setWsMessage('');
  }

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: 16 }}>
      <h2>RecipeDex Engineering Console</h2>
      <p>Backend base URL: <code>{BASE_URL}</code></p>
      {user && (
        <p>
          Firebase UID: <code>{user.uid}</code>
          {panel('currentAppUser').data?.user_id && (
            <> &nbsp;| App User ID: <code>{panel('currentAppUser').data.user_id}</code></>
          )}
        </p>
      )}

      <Section title="Root">
        <button onClick={() => run('root', () => api.root())}>GET /</button>
        <JsonView data={panel('root').data || panel('root').error} />
      </Section>

      <Section title="User">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <input placeholder="user_id" value={state.userId || ''} onChange={(e) => setState((s) => ({ ...s, userId: e.target.value }))} />
          <button onClick={() => run('getUser', () => api.getUser(state.userId))}>GET /user/{'{user_id}'}</button>
          <button onClick={() => run('deleteUser', () => api.deleteUser(state.userId))}>DELETE /user/{'{user_id}'}</button>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 8, flexWrap: 'wrap' }}>
          <input placeholder="provider (e.g. firebase)" value={state.provider || ''} onChange={(e) => setState((s) => ({ ...s, provider: e.target.value }))} />
          <input placeholder="provider_id (e.g. Firebase UID)" value={state.providerId || ''} onChange={(e) => setState((s) => ({ ...s, providerId: e.target.value }))} />
          <button onClick={() => run('getUserByProvider', () => api.getUserByProvider(state.provider, state.providerId))}>GET /user/provider/{'{provider}/{provider_id}'}</button>
        </div>
        <JsonView data={panel('getUser').data || panel('getUser').error || panel('getUserByProvider').data || panel('getUserByProvider').error || panel('deleteUser').data || panel('deleteUser').error} />
      </Section>

      <Section title="Update User">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <input placeholder="user_id" value={state.updateUserId || ''} onChange={(e) => setState((s) => ({ ...s, updateUserId: e.target.value }))} />
          <input placeholder="name" value={state.updateUserName || ''} onChange={(e) => setState((s) => ({ ...s, updateUserName: e.target.value }))} />
          <button onClick={() => run('updateUser', () => api.updateUser(state.updateUserId, { name: state.updateUserName || undefined }))}>PUT /user/{'{user_id}'}</button>
          <button onClick={() => setState((s) => ({ ...s, updateUserId: '', updateUserName: '' }))}>Clear</button>
        </div>
        <JsonView data={panel('updateUser').data || panel('updateUser').error} />
      </Section>

      <Section title="List Recipes">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <label>page</label>
          <input type="number" value={listPage} onChange={(e) => setListPage(parseInt(e.target.value, 10) || 0)} style={{ width: 80 }} />
          <label>page_size</label>
          <input type="number" value={listPageSize} onChange={(e) => setListPageSize(parseInt(e.target.value, 10) || 25)} style={{ width: 80 }} />
          <button onClick={() => run('listRecipes', () => api.listRecipes(listPage, listPageSize))}>GET /recipe/</button>
        </div>
        <JsonView data={panel('listRecipes').data || panel('listRecipes').error} />
      </Section>

      <Section title="Create Recipe">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <input placeholder="name (optional)" value={createName} onChange={(e) => setCreateName(e.target.value)} />
          <button onClick={() => run('createRecipe', async () => {
            const res = await api.createRecipe(createName || undefined);
            const id = res?.data?.id || res?.id;
            if (id) { setCreatedId(id); setRecipeId(id); }
            return res;
          })}>POST /recipe/</button>
          {createdId && <span>Created id: <code>{createdId}</code></span>}
        </div>
        <JsonView data={panel('createRecipe').data || panel('createRecipe').error} />
      </Section>

      <Section title="Recipe">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <input placeholder="recipe_id" value={recipeId} onChange={(e) => setRecipeId(e.target.value)} />
          <button onClick={() => { setRecipeResultKey('getRecipe'); run('getRecipe', () => api.getRecipe(recipeId)); }}>GET /recipe/{'{recipe_id}'}</button>
          <button onClick={() => { setRecipeResultKey('getMetadata'); run('getMetadata', () => api.getRecipeMetadata(recipeId)); }}>GET /recipe/{'{recipe_id}'}/metadata</button>
        </div>
        {(() => {
          const p = recipeResultKey ? panel(recipeResultKey) : {};
          return <JsonView data={p.data || p.error} />;
        })()}
      </Section>

      <Section title="Update Recipe">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <input placeholder="recipe_id" value={recipeId} onChange={(e) => setRecipeId(e.target.value)} />
          <input placeholder="name" value={state.updateRecipeName || ''} onChange={(e) => setState((s) => ({ ...s, updateRecipeName: e.target.value }))} />
          <label style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <input 
              type="checkbox" 
              checked={state.updateRecipePrivate || false} 
              onChange={(e) => setState((s) => ({ ...s, updateRecipePrivate: e.target.checked }))} 
            />
            Private
          </label>
          <button onClick={() => {
            const updateData = {};
            if (state.updateRecipeName) updateData.name = state.updateRecipeName;
            if (state.updateRecipePrivate !== undefined) updateData.private = state.updateRecipePrivate;
            run('updateRecipe', () => api.updateRecipe(recipeId, updateData));
          }}>PUT /recipe/{'{recipe_id}'}</button>
        </div>
        <JsonView data={panel('updateRecipe').data || panel('updateRecipe').error} />
      </Section>

      <Section title="Delete Recipe">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <input placeholder="recipe_id" value={recipeId} onChange={(e) => setRecipeId(e.target.value)} />
          <button onClick={() => run('deleteRecipe', () => api.deleteRecipe(recipeId))}>DELETE /recipe/{'{recipe_id}'}</button>
        </div>
        <JsonView data={panel('deleteRecipe').data || panel('deleteRecipe').error} />
      </Section>

      <Section title="Recipe Messages (GET & WebSocket)">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <input placeholder="recipe_id" value={recipeId} onChange={(e) => setRecipeId(e.target.value)} />
          <button onClick={() => run('getMessages', () => api.getRecipeMessages(recipeId))}>GET /recipe/{'{recipe_id}'}/message</button>
        </div>
        <JsonView data={panel('getMessages').data || panel('getMessages').error} />
        <div style={{ marginTop: 12, display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <button disabled={wsConnected} onClick={connectWs}>Connect WS</button>
          <button disabled={!wsConnected} onClick={disconnectWs}>Disconnect WS</button>
          <input placeholder="message" value={wsMessage} onChange={(e) => setWsMessage(e.target.value)} />
          <button disabled={!wsConnected || !wsMessage} onClick={sendWs}>Send</button>
        </div>
        <pre style={{ background: '#f0f0f0', padding: 12, borderRadius: 6, maxHeight: 240, overflow: 'auto', marginTop: 8 }}>
{JSON.stringify(wsLog, null, 2)}
        </pre>
      </Section>
    </div>
  );
}
