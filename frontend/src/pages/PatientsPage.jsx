import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import axios from 'axios';

function PatientsPage() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPatients() {
      try {
        const token = localStorage.getItem('token');
        console.log('Token in localStorage:', token);
        if (!token) {
          console.warn('No token found in localStorage!');
        }
        const authHeader = `Bearer ${token}`;
        console.log('Authorization header:', authHeader);
        const response = await axios.get('/patients/', {
          headers: {
            Authorization: authHeader
          }
        });
        setPatients(response.data);
      } catch (err) {
        console.error('Error fetching patients:', err);
        // Handle error
      } finally {
        setLoading(false);
      }
    }
    fetchPatients();
  }, []);

  const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'first_name', headerName: 'First name', width: 130 },
    { field: 'last_name', headerName: 'Last name', width: 130 },
    { field: 'date_of_birth', headerName: 'DOB', width: 120 },
    { field: 'gender', headerName: 'Gender', width: 100 },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'phone_number', headerName: 'Phone', width: 140 },
  ];

  return (
    <Box sx={{ height: 500, width: '100%' }}>
      <Typography variant="h4" gutterBottom>
        Patients
      </Typography>
      <DataGrid
        rows={patients}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10]}
        loading={loading}
        disableSelectionOnClick
      />
    </Box>
  );
}

export default PatientsPage;
