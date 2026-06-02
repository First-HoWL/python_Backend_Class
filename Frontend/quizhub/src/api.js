export const API_BASE = process.env.REACT_APP_API_BASE || '';

function normalizeApiPath(path) {
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  return path.startsWith('/') ? path : `/${path}`;
}

export async function getApiJson(path, options = {}) {
  const normalizedPath = normalizeApiPath(path);
  const url = normalizedPath.startsWith('/') ? `${API_BASE}${normalizedPath}` : `${API_BASE}/${normalizedPath}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      Accept: 'application/json',
      ...(options.headers || {}),
    },
  });

  const bodyText = await response.text();
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} ${response.statusText}: ${bodyText}`);
  }

  try {
    return JSON.parse(bodyText);
  } catch (err) {
    throw new Error(`Invalid JSON response from ${url}: ${bodyText}`);
  }
}
