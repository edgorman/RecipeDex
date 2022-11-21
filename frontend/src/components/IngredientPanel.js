import React from 'react';
import Ingredient from './Ingredient';

class IngredientPanel extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    if (this.props.value.length > 0) {
      return (
        <div id="ingredientpanel" className="col-12">
          <ul className="list-group list-group-flush">
            {
              this.props.value.map(function(ingredient, idx){
                const key = "ingredient-" + idx;
                return (
                  <Ingredient 
                    key={key}
                    name={ingredient.name}
                    quantity={ingredient.quantity}
                    unit={ingredient.unit}
                    comment={ingredient.comment} />
                );
              })
            }
          </ul>
        </div>
      );
    }
    else {
      return (
        <p className="card-text placeholder-wave">
          <span className="placeholder col-9"></span>
          <span className="placeholder col-7"></span>
          <span className="placeholder col-8"></span>
          <span className="placeholder col-9"></span>
          <span className="placeholder col-5"></span>
          <span className="placeholder col-8"></span>
          <span className="placeholder col-7"></span>
          <span className="placeholder col-6"></span>
        </p>
      );
    }
  }
}

export default IngredientPanel;
