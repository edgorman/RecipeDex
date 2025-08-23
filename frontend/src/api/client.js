/* API client for RecipeDex backend */

const BASE_URL = process.env.REACT_APP_BACKEND_API || 'http://127.0.0.1:8080';

// Lazy import to avoid circulars if firebase isn't set up yet
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

async function request(path, { method = 'GET', query, body, headers } = {}) {
  const url = new URL(path, BASE_URL);
  if (query) {
    Object.entries(query)
      .filter(([, v]) => v !== undefined && v !== null && v !== '')
      .forEach(([k, v]) => url.searchParams.set(k, String(v)));
  }

  const token = await getIdToken();
  const res = await fetch(url.toString(), {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}`, "Authorization-Provider": `firebase` } : {}),
      ...(headers || {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const text = await res.text();
  let json;
  try { json = text ? JSON.parse(text) : null; } catch { json = text; }
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status}`);
    err.status = res.status;
    err.body = json;
    throw err;
  }
  return json;
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
};

export { BASE_URL };
