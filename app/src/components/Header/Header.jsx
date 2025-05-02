import React from 'react';
import { Box, Typography } from '@material-ui/core';
import { Login } from './Login';

export function Header({user, onLogin}) {
  return (
    <Box className={"header"}>
      <Typography variant="subtitle1" className={"headerLogo"}>
        RecipeDex
      </Typography>
      <Login user={user} onLogin={onLogin} />
    </Box>
  );
}
