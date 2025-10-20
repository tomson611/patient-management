import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link, useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../AuthContext';

function Navbar() {
  const navigate = useNavigate();
  const { token, logout } = useContext(AuthContext);
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Patient Management
          </Typography>
          <Button color="inherit" component={Link} to="/patients">Patients</Button>
          <Button color="inherit" component={Link} to="/profile">Profile</Button>
          {!token ? (
            <>
              <Button color="inherit" component={Link} to="/login">Login</Button>
              <Button color="inherit" component={Link} to="/register">Register</Button>
            </>
          ) : (
            <Button color="inherit" onClick={() => { logout(); navigate('/login'); }}>Logout</Button>
          )}
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Navbar;
