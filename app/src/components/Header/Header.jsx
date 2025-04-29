import React from 'react';
import { Box, Typography } from '@mui/material';
import { Login } from './Login';

export function Header({user, onLogin}) {
  return (
    <Box className={"header"}>
      <Typography variant="h7" paddingTop={"8px"}>
        RecipeDex
      </Typography>
      <Login user={user} onLogin={onLogin} />
    </Box>
  );
}
