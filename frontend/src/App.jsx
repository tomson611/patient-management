import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PatientsPage from './pages/PatientsPage';
import ProtectedRoute from './ProtectedRoute';
import ProfilePage from './pages/ProfilePage';
import Navbar from './components/Navbar';
import { AuthProvider } from './AuthContext';

function App() {
  // TODO: Add authentication state and protected route logic
  return (
    <AuthProvider>
      <CssBaseline />
      <Navbar />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/patients" element={<ProtectedRoute><PatientsPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="/" element={<Navigate to="/patients" replace />} />
        </Routes>
      </Container>
    </AuthProvider>
  );
}

export default App;
