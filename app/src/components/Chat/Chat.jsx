import React from 'react';
import { Box, TextField, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { Message } from './Message';

export function Chat({ chatInput, onInputChange, onSend, messages }) {
  return (
    <Box className="chat">
      {messages.map((msg, index) => (
        <Message key={index} sender={msg.sender} text={msg.text} />
      ))}
      <Box className="chatInput">
        <TextField
          fullWidth
          size="small"
          variant="outlined"
          placeholder="Ask the assistant..."
          value={chatInput}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') onSend(); }}
        />
        <IconButton color="primary" onClick={onSend}>
          <SendIcon />
        </IconButton>
      </Box>
    </Box>
  );
}
