import React, { useState } from 'react';
import {
  List,
  ListItem,
  TextField,
  Collapse,
  IconButton,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import { ExpandLess, ExpandMore } from '@mui/icons-material';

export function Ingredients({ recipe, onIngredientChange }) {
  const [open, setOpen] = useState(true);

  return (
    <div className="recipeIngredients">
      <ListItem>
        <ListItemText primary="Ingredients" />
        <ListItemIcon>
          <IconButton onClick={() => setOpen(!open)}>
            {open ? <ExpandLess /> : <ExpandMore />}
          </IconButton>
        </ListItemIcon>
      </ListItem>

      <Collapse in={open} timeout="auto" unmountOnExit>
        <List dense>
          {recipe.ingredients.map((item, i) => (
            <ListItem key={i}>
              <TextField
                fullWidth
                value={item}
                onChange={(e) => onIngredientChange(i, e.target.value)}
                variant="outlined"
                size="small"
              />
            </ListItem>
          ))}
        </List>
      </Collapse>
    </div>
  );
}
