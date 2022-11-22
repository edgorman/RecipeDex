import React from 'react';

class Ingredient extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    let ingredient = `${this.props.name}`;
    if (this.props.unit !== ""){
      ingredient += ` (${this.props.quantity} ${this.props.unit})`
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
