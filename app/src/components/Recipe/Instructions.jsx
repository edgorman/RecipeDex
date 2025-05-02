import React, { useState } from 'react';
import {
  List,
  ListItem,
  TextField,
  Collapse,
  IconButton,
  ListItemText,
  ListItemIcon,
} from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';

export function Instructions({ recipe, onInstructionChange }) {
  const [open, setOpen] = useState(true);

  return (
    <div className="recipeInstructions">
      <ListItem>
        <ListItemText primary="Instructions" />
        <ListItemIcon>
          <IconButton onClick={() => setOpen(!open)}>
            {open ? <ExpandLess /> : <ExpandMore />}
          </IconButton>
        </ListItemIcon>
      </ListItem>

      <Collapse in={open} timeout="auto" unmountOnExit>
        <List dense>
          {recipe.instructions.map((item, i) => (
            <ListItem key={i}>
              <TextField
                fullWidth
                value={item}
                onChange={(e) => onInstructionChange(i, e.target.value)}
                variant="outlined"
                size="small"
                label={`Step ${i + 1}`}
              />
            </ListItem>
          ))}
        </List>
      </Collapse>
    </div>
  );
}
