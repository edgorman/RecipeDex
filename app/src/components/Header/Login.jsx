import React from 'react';
import { IconButton } from '@mui/material';
import { default as LoginIcon } from '@mui/icons-material/Login';
import { default as PersonIcon } from '@mui/icons-material/Person';

export function Login({user, onLogin}) {
  return (
    <IconButton color="default" onClick={onLogin}>
      {user ? <PersonIcon /> : <LoginIcon />}
    </IconButton>
  );
}
