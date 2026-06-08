export const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

const SESSION_STORAGE_KEY = 'accaunt';

function normalizeApiPath(path) {
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  return path.startsWith('/') ? path : `/${path}`;
}

function buildUrl(path) {
  const normalized = normalizeApiPath(path);
  return normalized.startsWith('/') ? `${API_BASE}${normalized}` : `${API_BASE}/${normalized}`;
}

function parseSessionValue(value) {
  if (!value) return null;
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function normalizeSession(session) {
  if (!session || typeof session !== 'object') return null;

  const access = session.access || session.token || null;
  const refresh = session.refresh || session.refreshToken || null;
  const accaunt = session.accaunt || session.account || (
    session.id ? {
      id: session.id,
      login: session.login,
      name: session.name,
      isTeacher: session.isTeacher,
    } : null
  );

  if (!access && !refresh && !accaunt) return null;

  return { access, refresh, accaunt };
}

function getSession() {
  const stored = parseSessionValue(localStorage.getItem(SESSION_STORAGE_KEY));
  return normalizeSession(stored);
}

function getAuthToken() {
  return getSession()?.access || null;
}

export function getStoredAccaunt() {
  return getSession();
}

export function saveSession(data) {
  const normalized = normalizeSession(data);
  if (!normalized) return null;
  try {
    localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(normalized));
    return normalized;
  } catch (err) {
    console.error('Unable to save auth session to localStorage', err);
    return null;
  }
}

async function tryRefreshToken() {
  try {
    const stored = getStoredAccaunt();
    if (!stored?.refresh) return false;

    const response = await fetch(`${API_BASE}/api/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ refresh: stored.refresh }),
    });

    if (!response.ok) return false;

    const data = await response.json();
    if (!data.access) return false;

    localStorage.setItem('accaunt', JSON.stringify({
      ...stored,
      access: data.access,
    }));
    return true;
  } catch {
    return false;
  }
}

function buildHeaders(defaults = {}, options = {}) {
  const headers = { ...defaults, ...(options.headers || {}) };
  if (options.auth) {
    const token = getAuthToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }
  return headers;
}

function parseResponseBody(bodyText) {
  try {
    return JSON.parse(bodyText);
  } catch {
    return bodyText;
  }
}

function createError(url, status, bodyText, body) {
  const reason = body?.detail || body?.error || bodyText || `HTTP ${status}`;
  return new Error(`HTTP ${status}: ${reason}`);
}

async function fetchWithRefresh(url, fetchOptions, options) {
  let response = await fetch(url, fetchOptions);

  if (response.status === 401 && options.auth) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      const newToken = getAuthToken();
      const newFetchOptions = {
        ...fetchOptions,
        headers: {
          ...fetchOptions.headers,
          Authorization: `Bearer ${newToken}`,
        },
      };
      response = await fetch(url, newFetchOptions);
    } else {
      localStorage.removeItem('accaunt');
      // Бросаем явно — чтобы вызывающий код попал в catch и мог сделать navigate('/login')
      throw new Error('HTTP 401: Session expired');
    }
  }

  return response;
}

export async function getApiJson(path, options = {}) {
  const url = buildUrl(path);
  const fetchOptions = {
    ...options,
    headers: buildHeaders({ Accept: 'application/json' }, options),
  };
  const response = await fetchWithRefresh(url, fetchOptions, options);
  const bodyText = await response.text();
  const body = parseResponseBody(bodyText);
  if (!response.ok) {
    throw createError(url, response.status, bodyText, body);
  }
  return body;
}

export async function postApiJson(path, body = {}, options = {}) {
  const url = buildUrl(path);
  const fetchOptions = {
    method: 'POST',
    ...options,
    headers: buildHeaders(
      { 'Content-Type': 'application/json', Accept: 'application/json' },
      options
    ),
    body: JSON.stringify(body),
  };
  const response = await fetchWithRefresh(url, fetchOptions, options);
  const bodyText = await response.text();
  const responseBody = parseResponseBody(bodyText);
  if (!response.ok) {
    throw createError(url, response.status, bodyText, responseBody);
  }
  return responseBody;
}