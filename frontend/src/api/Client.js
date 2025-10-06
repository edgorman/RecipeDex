const BASE_URL = process.env.REACT_APP_BACKEND_API || 'http://127.0.0.1:8080';

async function getIdToken() {
  try {
    const { getAuth } = await import('firebase/auth');
    const auth = getAuth();
    const user = auth.currentUser;
    if (!user) return undefined;
    return await user.getIdToken();
  } catch (_) {
    return undefined;
  }
}

function parseJsonMaybe(text) {
  try { return text ? JSON.parse(text) : null; } catch { return text; }
}

async function request(path, { method = 'GET', query, body, headers } = {}) {
  const url = new URL(path, BASE_URL);
  if (query) {
    for (const [k, v] of Object.entries(query)) {
      if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, String(v));
    }
  }

  const token = await getIdToken();
  const res = await fetch(url.toString(), {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}`, 'Authorization-Provider': 'firebase' } : {}),
      ...(headers || {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const payload = parseJsonMaybe(await res.text());
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status}`);
    err.status = res.status;
    err.body = payload;
    throw err;
  }
  return payload;
}

export class RecipeMessageWebSocket {
  constructor(recipeId, options = {}) {
    this.recipeId = recipeId;
    this.options = {
      onOpen: () => {},
      onMessage: () => {},
      onError: () => {},
      onClose: () => {},
      ...options
    };
    this.socket = null;
    this.isConnected = false;
  }

  async connect() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    try {
      const base = new URL(`/recipe/${encodeURIComponent(this.recipeId)}/message`, BASE_URL);
      base.protocol = base.protocol === 'https:' ? 'wss:' : 'ws:';
      
      const token = await getIdToken();
      if (token) {
        base.searchParams.set('authorization', `Bearer ${token}`);
        base.searchParams.set('authorization_provider', 'firebase');
      }

      this.socket = new WebSocket(base.toString());

      this.socket.onopen = () => {
        this.isConnected = true;
        this.options.onOpen();
      };

      this.socket.onmessage = (event) => {
        let data;
        try {
          data = JSON.parse(event.data);
        } catch {
          data = event.data;
        }
        this.options.onMessage(data);
      };

      this.socket.onerror = (event) => {
        this.options.onError(event);
      };

      this.socket.onclose = (event) => {
        this.isConnected = false;
        this.options.onClose(event);
      };

    } catch (error) {
      this.options.onError(error);
    }
  }

  send(message) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket not connected');
    }
    
    const payload = typeof message === 'string' ? { value: message } : message;
    this.socket.send(JSON.stringify(payload));
  }

  disconnect() {
    if (this.socket) {
      try {
        this.socket.close();
      } catch (error) {
        // Ignore close errors
      }
      this.socket = null;
      this.isConnected = false;
    }
  }

  get readyState() {
    return this.socket ? this.socket.readyState : WebSocket.CLOSED;
  }
}

export const api = {
  root: () => request('/'),
  getUser: (userId) => request(`/user/${encodeURIComponent(userId)}`),
  updateUser: (userId, update) => request(`/user/${encodeURIComponent(userId)}`, { method: 'PUT', body: { data: update } }),
  deleteUser: (userId) => request(`/user/${encodeURIComponent(userId)}`, { method: 'DELETE' }),
  getUserByProvider: (provider, provider_id) => request(`/user/provider/${encodeURIComponent(provider)}/${encodeURIComponent(provider_id)}`),
  listRecipes: (page, page_size) => request('/recipe/', { query: { page, page_size } }),
  getRecipe: (recipeId) => request(`/recipe/${encodeURIComponent(recipeId)}`),
  createRecipe: (name) => request('/recipe/', { method: 'POST', body: { data: { name } } }),
  updateRecipe: (recipeId, update) => request(`/recipe/${encodeURIComponent(recipeId)}`, { method: 'PUT', body: { data: update } }),
  deleteRecipe: (recipeId) => request(`/recipe/${encodeURIComponent(recipeId)}`, { method: 'DELETE' }),
  getRecipeMetadata: (recipeId) => request(`/recipe/${encodeURIComponent(recipeId)}/metadata`),
  getRecipeMessages: (recipeId) => request(`/recipe/${encodeURIComponent(recipeId)}/message`),
  
  // WebSocket helper method
  createRecipeMessageWebSocket: (recipeId, options) => new RecipeMessageWebSocket(recipeId, options),
};

export { BASE_URL };
