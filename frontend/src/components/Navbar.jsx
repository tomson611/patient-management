import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  // TODO: Add auth logic for showing/hiding buttons
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Patient Management
          </Typography>
          <Button color="inherit" component={Link} to="/patients">Patients</Button>
          <Button color="inherit" component={Link} to="/profile">Profile</Button>
          <Button color="inherit" component={Link} to="/login">Login</Button>
          <Button color="inherit" component={Link} to="/register">Register</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Navbar;
