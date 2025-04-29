import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import PersonAddAlt1Icon from '@mui/icons-material/PersonAddAlt1';
import axios from 'axios';

function RegisterPage() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    role: 'user'
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      await axios.post('/auth/register', form);
      navigate('/login');
    } catch (err) {
      setError('Registration failed');
    }
  };

  return (
    <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
        <PersonAddAlt1Icon />
      </Avatar>
      <Typography component="h1" variant="h5">
        Register
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
        <TextField
          margin="normal"
          required
          fullWidth
          id="username"
          label="Username"
          name="username"
          autoComplete="username"
          value={form.username}
          onChange={handleChange}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          id="email"
          label="Email"
          name="email"
          autoComplete="email"
          value={form.email}
          onChange={handleChange}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          id="first_name"
          label="First Name"
          name="first_name"
          value={form.first_name}
          onChange={handleChange}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          id="last_name"
          label="Last Name"
          name="last_name"
          value={form.last_name}
          onChange={handleChange}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          name="password"
          label="Password"
          type="password"
          id="password"
          autoComplete="new-password"
          value={form.password}
          onChange={handleChange}
        />
        {error && <Typography color="error">{error}</Typography>}
        <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
          Register
        </Button>
      </Box>
    </Box>
  );
}

export default RegisterPage;
