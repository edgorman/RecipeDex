import React from 'react';
import { Box, Chip } from '@material-ui/core';

export function Tags({ recipe }) {
  return (
    <Box className="recipeTags">
      <div direction={"row"} className="tagsContainer">
        <Chip label={`Serves: ${recipe.serves}`} />
        <Chip label={`Prep: ${recipe.prepTime}`} />
        <Chip label={`Cook: ${recipe.cookTime}`} />
        <Chip label={`Total: ${recipe.totalTime}`} />
        <Chip label={`Difficulty: ${recipe.difficulty}`} />
        <Chip label={`Cuisine: ${recipe.cuisine}`} />
      </div>

      <div direction={"row"} className="tagsContainer">
        {recipe.dietaryRestrictions.map((tag, i) => (
          <Chip key={i} label={tag} />
        ))}
      </div>
    </Box>
  )
};
