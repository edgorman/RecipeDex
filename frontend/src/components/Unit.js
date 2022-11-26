import React from 'react';
import './Serving.css';

class Unit extends React.Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    if (this.props.name === this.props.value) {
      this.props.onUpdate("default", null);
    }
    else {
      this.props.onUpdate(this.props.name, null);
    }
  }

  render () {
    const checked = this.props.name === this.props.value;
    const name = this.props.name.charAt(0).toUpperCase() + this.props.name.slice(1);

    return (
      <div id="unit" className="form-check form-switch d-flex w-auto justify-content-center align-items-center">
        <input className="form-check-input" type="checkbox" id={name} onChange={this.handleChange} checked={checked}/>
        <label className="form-check-label ps-3" htmlFor={name}>{name}</label>
      </div>
    )
  }
}

export default Unit;
