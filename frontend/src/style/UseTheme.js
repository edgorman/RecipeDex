import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'themeOverride'; // 'light' | 'dark' | null (system)


function getStored() {
  try { return localStorage.getItem(STORAGE_KEY); } catch { return null; }
}

function systemPref() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function useTheme() {
  const [override, setOverride] = useState(() => getStored());
  const effective = override || systemPref();

  // Apply class to <html>
  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(effective);
  }, [effective]);

  // Persist only if user explicitly picked one
  useEffect(() => {
    try {
      if (override) localStorage.setItem(STORAGE_KEY, override);
      else localStorage.removeItem(STORAGE_KEY);
    } catch {}
  }, [override]);

  // React to OS changes when not overridden
  useEffect(() => {
    if (override) return; // follow system only
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = () => {
      // trigger re-render
      setOverride(prev => prev);
    };
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, [override]);

  const setTheme = useCallback(mode => {
    if (mode === 'system') setOverride(null);
    else if (mode === 'light' || mode === 'dark') setOverride(mode);
  }, []);

  const toggle = useCallback(() => {
    setTheme(effective === 'dark' ? 'light' : 'dark');
  }, [effective, setTheme]);

  return { theme: effective, override, isSystem: override == null, setTheme, toggle };
}
