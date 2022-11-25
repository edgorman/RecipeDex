import React from 'react';

class Ingredient extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    let ingredient = `${this.props.name}`;
    let quantity = this.props.quantity;
    quantity = quantity.endsWith(".0") ? quantity.substring(0, quantity.length - 2) : quantity;

    if (this.props.unit !== ""){
      ingredient += ` (${quantity} ${this.props.unit})`
    }
    if (this.props.comment !== ""){
      ingredient += `, ${this.props.comment}`;
    }

    return (
      <li className="list-group-item">{ingredient}</li>
    )
  }
}

export default Ingredient;
