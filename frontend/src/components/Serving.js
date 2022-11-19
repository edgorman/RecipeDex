import React from 'react';
import './Serving.css';

class Serving extends React.Component {
  constructor(props) {
    super(props);
    this.updateValue = this.updateValue.bind(this);
    this.increaseValue = this.increaseValue.bind(this);
    this.decreaseValue = this.decreaseValue.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  updateValue(value) {
    if (this.props.value !== value && 1 <= value && value <= 10) {
      this.props.onChange(value);
    }
  }

  increaseValue() {
    this.updateValue(this.props.value + 1);
  }

  decreaseValue() {
    this.updateValue(this.props.value - 1);
  }

  onChange(e){
    e.preventDefault();
    this.updateValue(parseInt(e.target.value));
  }

  onSubmit(e) {
    e.preventDefault();
    this.updateValue(parseInt(e.target.elements.quantity.value));
  }

  render () {
    return (
      <form id="serving" className="input-group w-auto justify-content-center align-items-center" onSubmit={this.onSubmit}>
        <input type="button" value="-" onClick={this.decreaseValue} className="button-minus rounded-circle icon-shape icon-sm mx-1" data-field="quantity"/>
        <input type="number" step="1" max="10" onBlur={this.onChange} onChange={this.onChange} value={this.props.value} name="quantity" className="quantity-field border-0 text-center w-25"/>
        <input type="button" value="+" onClick={this.increaseValue} className="button-plus rounded-circle icon-shape icon-sm " data-field="quantity"/>
      </form>
    )
  }
}

export default Serving;
