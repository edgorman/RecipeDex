import React from 'react';
import { Box, Typography } from '@material-ui/core';
import { Tags } from './Tags';
import { Ingredients } from './Ingredients';
import { Instructions } from './Instructions';

export function Recipe({ recipe, onIngredientChange, onInstructionChange }) {
  return (
    <Box className="recipe">
      <Typography variant="h5" gutterBottom>{recipe.name}</Typography>
      <Typography variant="subtitle1" gutterBottom>{recipe.description}</Typography>
      <Tags recipe={recipe} />

      <Ingredients recipe={recipe} onIngredientChange={onIngredientChange} />
      <Instructions recipe={recipe} onInstructionChange={onInstructionChange} />
    </Box>
  );
}
