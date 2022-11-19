import React from 'react';
import Ingredient from './Ingredient';

class IngredientPanel extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    return (
      <div id="ingredientpanel" className="row">
        <div className="col-12">
          <ul className="list-group list-group-flush">
            {
              this.props.values.map(function(ingredient, idx){
                const key = "ingredient-" + idx;
                return (
                  <Ingredient 
                    key={key}
                    name={ingredient.name}
                    quantity={ingredient.quantity}
                    unit={ingredient.unit}
                    comment={ingredient.comment} />
                )
              })
            }
          </ul>
        </div>
      </div>
    )
  }
}

export default IngredientPanel;
