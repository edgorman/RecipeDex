import React from 'react';
import Ingredient from './Ingredient';

class IngredientPanel extends React.Component {
  render () {
    return (
      <div id="ingredientpanel" className="row">
        <div className="col-12">
          <h5>Ingredients</h5>
          <ul className="list-group list-group-flush">
            <Ingredient />
            <Ingredient />
            <Ingredient />
            <Ingredient />
            <Ingredient />
          </ul>
        </div>
      </div>
    )
  }
}

export default IngredientPanel;
