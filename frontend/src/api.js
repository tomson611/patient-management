import axios from 'axios';

const baseURL = import.meta.env.DEV ? '' : import.meta.env.VITE_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// attach token from localStorage if present
const token = localStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export default api;
