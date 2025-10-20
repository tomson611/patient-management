import React, { createContext, useState, useEffect } from 'react';
import api from './api';

export const AuthContext = createContext({
  token: null,
  setToken: () => {},
  logout: () => {},
  user: null,
});

export function AuthProvider({ children }) {
  const [token, setTokenState] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const setToken = (t) => setTokenState(t);
  const logout = () => setTokenState(null);

  // fetch current user info when token changes
  const [user, setUser] = React.useState(null);
  React.useEffect(() => {
    let mounted = true;
    async function fetchUser() {
      if (!token) {
        setUser(null);
        return;
      }
      try {
        const resp = await api.get('/auth/me');
        if (mounted) setUser(resp.data);
      } catch (err) {
        console.error('Failed to fetch user', err);
        if (mounted) setUser(null);
      }
    }
    fetchUser();
    return () => (mounted = false);
  }, [token]);

  return (
    <AuthContext.Provider value={{ token, setToken, logout, user }}>
      {children}
    </AuthContext.Provider>
  );
}
