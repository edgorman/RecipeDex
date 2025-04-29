import React from 'react';
import { Box, Stack, Chip } from '@mui/material';

export function Tags({ recipe }) {
  return (
    <Box className="recipeTags">
      <Stack direction={"row"} className="tagsContainer">
        <Chip label={`Serves: ${recipe.serves}`} />
        <Chip label={`Prep: ${recipe.prepTime}`} />
        <Chip label={`Cook: ${recipe.cookTime}`} />
        <Chip label={`Total: ${recipe.totalTime}`} />
        <Chip label={`Difficulty: ${recipe.difficulty}`} />
        <Chip label={`Cuisine: ${recipe.cuisine}`} />
      </Stack>

      <Stack direction={"row"} className="tagsContainer">
        {recipe.dietaryRestrictions.map((tag, i) => (
          <Chip key={i} label={tag} color="success" />
        ))}
      </Stack>
    </Box>
  )
};
