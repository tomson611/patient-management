import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import api from '../api';
import { useContext } from 'react';
import { AuthContext } from '../AuthContext';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';

function PatientsPage() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPatients() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          console.warn('No token found in localStorage!');
        }
        const response = await api.get('/patients/');
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

  // simple create form state
  const [newPatient, setNewPatient] = React.useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    gender: '',
    address: '',
    phone_number: '',
    email: '',
    medical_history: ''
  });

  const handleCreate = async (e) => {
    e.preventDefault();
    // Basic client-side validation
    if (!newPatient.first_name || !newPatient.last_name || !newPatient.email) {
      console.warn('first_name, last_name and email are required');
      return;
    }

    try {
      const resp = await api.post('/patients/', newPatient);
      setPatients((prev) => [resp.data, ...prev]);
      setNewPatient({
        first_name: '',
        last_name: '',
        date_of_birth: '',
        gender: '',
        address: '',
        phone_number: '',
        email: '',
        medical_history: ''
      });
    } catch (err) {
      console.error('Create patient failed', err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/patients/${id}`);
      setPatients(prev => prev.filter(p => p.id !== id));
    } catch (err) {
      console.error('Delete failed', err);
    }
  };

  const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'first_name', headerName: 'First name', width: 130 },
    { field: 'last_name', headerName: 'Last name', width: 130 },
    { field: 'date_of_birth', headerName: 'DOB', width: 120 },
    { field: 'gender', headerName: 'Gender', width: 100 },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'phone_number', headerName: 'Phone', width: 140 },
  ];

  const { user } = useContext(AuthContext);

  return (
    <Box sx={{ height: 500, width: '100%' }}>
      <Typography variant="h4" gutterBottom>
        Patients
      </Typography>
      <Box component="form" onSubmit={handleCreate} sx={{ mb: 2 }}>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} alignItems="center">
          <TextField size="small" label="First name" required value={newPatient.first_name} onChange={e => setNewPatient({ ...newPatient, first_name: e.target.value })} />
          <TextField size="small" label="Last name" required value={newPatient.last_name} onChange={e => setNewPatient({ ...newPatient, last_name: e.target.value })} />
          <TextField size="small" label="Email" required type="email" value={newPatient.email} onChange={e => setNewPatient({ ...newPatient, email: e.target.value })} />
        </Stack>

        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mt: 1 }}>
          <TextField size="small" label="Date of birth" type="date" InputLabelProps={{ shrink: true }} value={newPatient.date_of_birth} onChange={e => setNewPatient({ ...newPatient, date_of_birth: e.target.value })} />
          <TextField size="small" label="Gender" value={newPatient.gender} onChange={e => setNewPatient({ ...newPatient, gender: e.target.value })} />
          <TextField size="small" label="Phone" value={newPatient.phone_number} onChange={e => setNewPatient({ ...newPatient, phone_number: e.target.value })} />
        </Stack>

        <TextField label="Address" size="small" fullWidth sx={{ mt: 1 }} value={newPatient.address} onChange={e => setNewPatient({ ...newPatient, address: e.target.value })} />

        <TextField label="Medical history" size="small" fullWidth multiline minRows={2} sx={{ mt: 1 }} value={newPatient.medical_history} onChange={e => setNewPatient({ ...newPatient, medical_history: e.target.value })} />

        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 1 }}>
          <Button type="submit" variant="contained">Create</Button>
        </Box>
      </Box>
      <DataGrid
        rows={patients}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10]}
        loading={loading}
        disableSelectionOnClick
      />
      {/* Simple delete buttons in a separate list for clarity */}
      <Box sx={{ mt: 2 }}>
        {patients.map(p => (
          <Box key={p.id} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <Typography>{p.first_name} {p.last_name} ({p.email})</Typography>
            {user && user.role === 'admin' && (
              <Button size="small" color="error" onClick={() => handleDelete(p.id)}>Delete</Button>
            )}
          </Box>
        ))}
      </Box>
    </Box>
  );
}

export default PatientsPage;
