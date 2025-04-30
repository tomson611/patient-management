import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PatientsPage from './pages/PatientsPage';
import ProfilePage from './pages/ProfilePage';
import Navbar from './components/Navbar';

function App() {
  // TODO: Add authentication state and protected route logic
  return (
    <>
      <CssBaseline />
      <Navbar />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/patients" element={<PatientsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/" element={<Navigate to="/patients" replace />} />
        </Routes>
      </Container>
    </>
  );
}

export default App;
