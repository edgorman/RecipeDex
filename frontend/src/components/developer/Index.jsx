import React from 'react';
import { api, BASE_URL } from '../../api/Client';
import { useAuthUser } from '../../auth/UseAuthUser';

// Material Web components
import '@material/web/button/filled-button.js';
import '@material/web/button/outlined-button.js';
import '@material/web/textfield/outlined-text-field.js';
import '@material/web/checkbox/checkbox.js';
import '@material/web/elevation/elevation.js';

function Section({ title, children }) {
  return (
    <md-elevated-card style={{display: 'block', padding: 16, marginBottom: 16}}>
      <div slot="headline" style={{fontSize: '1.1rem', fontWeight: 600, marginBottom: 8}}>{title}</div>
      {children}
    </md-elevated-card>
  );
}

function JsonView({ data }) {
  return (
    <pre style={{ padding: 12, borderRadius: 6, overflow: 'auto' }}>
      {data == null ? '—' : JSON.stringify(data, null, 2)}
    </pre>
  );
}

export function DeveloperConsole() {
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
  const [wsConnection, setWsConnection] = React.useState(null);
  const [wsConnected, setWsConnected] = React.useState(false);
  const [wsLog, setWsLog] = React.useState([]);
  const [wsMessage, setWsMessage] = React.useState('');

  const user = useAuthUser();

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
      wsConnection?.disconnect();
    };
  }, [wsConnection]);

  async function connectWs() {
    if (!recipeId) {
      setWsLog((l) => [...l, { type: 'error', message: 'Provide recipe_id before connecting' }]);
      return;
    }

    const connection = api.createRecipeMessageWebSocket(recipeId, {
      onOpen: () => {
        setWsConnected(true);
        setWsLog((l) => [...l, { type: 'open', at: new Date().toISOString() }]);
      },
      onMessage: (data) => {
        setWsLog((l) => [...l, { type: 'message', at: new Date().toISOString(), data }]);
      },
      onError: (error) => {
        setWsLog((l) => [...l, { type: 'error', at: new Date().toISOString(), data: String(error?.message || 'ws error') }]);
      },
      onClose: (event) => {
        setWsConnected(false);
        setWsLog((l) => [...l, {
          type: 'close',
          at: new Date().toISOString(),
          data: {
            code: event.code,
            reason: event.reason,
            wasClean: event.wasClean,
          },
        }]);
      }
    });

    try {
      await connection.connect();
      setWsConnection(connection);
    } catch (e) {
      setWsLog((l) => [...l, { type: 'error', at: new Date().toISOString(), data: e?.message }]);
    }
  }

  function disconnectWs() {
    wsConnection?.disconnect();
    setWsConnection(null);
  }

  function sendWs() {
    if (!wsConnection || !wsConnection.isConnected) {
      setWsLog((l) => [...l, { type: 'error', message: 'WebSocket not connected' }]);
      return;
    }
    try {
      wsConnection.send(wsMessage);
      setWsLog((l) => [...l, { type: 'sent', at: new Date().toISOString(), data: { value: wsMessage } }]);
      setWsMessage('');
    } catch (error) {
      setWsLog((l) => [...l, { type: 'error', at: new Date().toISOString(), data: error.message }]);
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: 16 }}>
      <h2>Developer Console</h2>
      <p>Backend base URL: <code>{BASE_URL}</code></p>
      {user && (
        <p>
          Firebase UID: <code>{user.uid}</code>
          {panel('currentAppUser').data?.id && (
            <> &nbsp;| RecipeDex User ID: <code>{panel('currentAppUser').data.id}</code></>
          )}
        </p>
      )}

      <Section title="Root">
        <md-filled-button onClick={() => run('root', () => api.root())}>GET /</md-filled-button>
        <JsonView data={panel('root').data || panel('root').error} />
      </Section>

      <Section title="User">
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <md-outlined-text-field label="user_id" value={state.userId || ''} onInput={(e) => setState((s) => ({ ...s, userId: e.target.value }))} />
          <md-filled-button onClick={() => run('getUser', () => api.getUser(state.userId))}>GET /user/{'{user_id}'}</md-filled-button>
          <md-filled-button onClick={() => run('deleteUser', () => api.deleteUser(state.userId))}>DELETE /user/{'{user_id}'}</md-filled-button>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', marginTop: 8, flexWrap: 'wrap' }}>
          <md-outlined-text-field label="provider" value={state.provider || ''} onInput={(e) => setState((s) => ({ ...s, provider: e.target.value }))} />
          <md-outlined-text-field label="provider_id" value={state.providerId || ''} onInput={(e) => setState((s) => ({ ...s, providerId: e.target.value }))} />
          <md-filled-button onClick={() => run('getUserByProvider', () => api.getUserByProvider(state.provider, state.providerId))}>GET /user/provider/{'{provider}/{provider_id}'}</md-filled-button>
        </div>
        <JsonView data={panel('getUser').data || panel('getUser').error || panel('getUserByProvider').data || panel('getUserByProvider').error || panel('deleteUser').data || panel('deleteUser').error} />
      </Section>

      <Section title="Update User">
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <md-outlined-text-field label="user_id" value={state.updateUserId || ''} onInput={(e) => setState((s) => ({ ...s, updateUserId: e.target.value }))} />
          <md-outlined-text-field label="name" value={state.updateUserName || ''} onInput={(e) => setState((s) => ({ ...s, updateUserName: e.target.value }))} />
          <md-filled-button onClick={() => run('updateUser', () => api.updateUser(state.updateUserId, { name: state.updateUserName || undefined }))}>PUT /user/{'{user_id}'}</md-filled-button>
          <md-outlined-button onClick={() => setState((s) => ({ ...s, updateUserId: '', updateUserName: '' }))}>Clear</md-outlined-button>
        </div>
        <JsonView data={panel('updateUser').data || panel('updateUser').error} />
      </Section>

      <Section title="List Recipes">
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <md-outlined-text-field type="number" label="page" value={listPage} onInput={(e) => setListPage(parseInt(e.target.value, 10) || 0)} style={{ width: 120 }} />
          <md-outlined-text-field type="number" label="page_size" value={listPageSize} onInput={(e) => setListPageSize(parseInt(e.target.value, 10) || 25)} style={{ width: 120 }} />
          <md-filled-button onClick={() => run('listRecipes', () => api.listRecipes(listPage, listPageSize))}>GET /recipe/</md-filled-button>
        </div>
        <JsonView data={panel('listRecipes').data || panel('listRecipes').error} />
      </Section>

      <Section title="Create Recipe">
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <md-outlined-text-field label="name (optional)" value={createName} onInput={(e) => setCreateName(e.target.value)} />
          <md-filled-button onClick={() => run('createRecipe', async () => {
            const res = await api.createRecipe(createName || undefined);
            const id = res?.data?.id || res?.id;
            if (id) { setCreatedId(id); setRecipeId(id); }
            return res;
          })}>POST /recipe/</md-filled-button>
          {createdId && <span>Created id: <code>{createdId}</code></span>}
        </div>
        <JsonView data={panel('createRecipe').data || panel('createRecipe').error} />
      </Section>

      <Section title="Recipe">
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <md-outlined-text-field label="recipe_id" value={recipeId} onInput={(e) => setRecipeId(e.target.value)} />
          <md-filled-button onClick={() => { setRecipeResultKey('getRecipe'); run('getRecipe', () => api.getRecipe(recipeId)); }}>GET /recipe/{'{recipe_id}'}</md-filled-button>
          <md-filled-button onClick={() => { setRecipeResultKey('getMetadata'); run('getMetadata', () => api.getRecipeMetadata(recipeId)); }}>GET /recipe/{'{recipe_id}'}/metadata</md-filled-button>
        </div>
        {(() => {
          const p = recipeResultKey ? panel(recipeResultKey) : {};
          return <JsonView data={p.data || p.error} />;
        })()}
      </Section>

      <Section title="Update Recipe">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <md-outlined-text-field label="recipe_id" value={recipeId} onInput={(e) => setRecipeId(e.target.value)} />
          <md-outlined-text-field label="name" value={state.updateRecipeName || ''} onInput={(e) => setState((s) => ({ ...s, updateRecipeName: e.target.value }))} />
          <label style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <md-checkbox checked={state.updateRecipePrivate || false} onChange={(e) => setState((s) => ({ ...s, updateRecipePrivate: e.target.checked }))}></md-checkbox>
            <span style={{ fontSize: 14 }}>Private</span>
          </label>
          <md-filled-button onClick={() => {
            const updateData = {};
            if (state.updateRecipeName) updateData.name = state.updateRecipeName;
            if (state.updateRecipePrivate !== undefined) updateData.private = state.updateRecipePrivate;
            run('updateRecipe', () => api.updateRecipe(recipeId, updateData));
          }}>PUT /recipe/{'{recipe_id}'}</md-filled-button>
        </div>
        <JsonView data={panel('updateRecipe').data || panel('updateRecipe').error} />
      </Section>

      <Section title="Delete Recipe">
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <md-outlined-text-field label="recipe_id" value={recipeId} onInput={(e) => setRecipeId(e.target.value)} />
          <md-filled-button onClick={() => run('deleteRecipe', () => api.deleteRecipe(recipeId))}>DELETE /recipe/{'{recipe_id}'}</md-filled-button>
        </div>
        <JsonView data={panel('deleteRecipe').data || panel('deleteRecipe').error} />
      </Section>

      <Section title="Recipe Messages (GET & WebSocket)">
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <md-outlined-text-field label="recipe_id" value={recipeId} onInput={(e) => setRecipeId(e.target.value)} />
          <md-filled-button onClick={() => run('getMessages', () => api.getRecipeMessages(recipeId))}>GET /recipe/{'{recipe_id}'}/message</md-filled-button>
        </div>
        <JsonView data={panel('getMessages').data || panel('getMessages').error} />
        <div style={{ marginTop: 12, display: 'flex', gap: 8, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <md-filled-button disabled={wsConnected} onClick={connectWs}>Connect WS</md-filled-button>
            <md-filled-button disabled={!wsConnected} onClick={disconnectWs}>Disconnect WS</md-filled-button>
          <md-outlined-text-field label="message" value={wsMessage} onInput={(e) => setWsMessage(e.target.value)} />
          <md-filled-button disabled={!wsConnected || !wsMessage} onClick={sendWs}>Send</md-filled-button>
        </div>
        <pre style={{ padding: 12, borderRadius: 6, maxHeight: 240, overflow: 'auto', marginTop: 8 }}>
{JSON.stringify(wsLog, null, 2)}
        </pre>
      </Section>
    </div>
  );
}
