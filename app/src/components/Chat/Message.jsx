import React from 'react';
import { Box, Typography } from '@material-ui/core';

export function Message({ sender, text }) {
  return (
    <Box className={`message ${sender}`}>
      <Typography variant="body2">
        <strong>{sender === "user" ? "You" : "AI"}:</strong> {text}
      </Typography>
    </Box>
  );
}
