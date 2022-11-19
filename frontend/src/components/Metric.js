import React from 'react';
import './Serving.css';

class Metric extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    if (this.props.name == this.props.value) {
      this.props.onChange("default");
    }
    else {
      this.props.onChange(this.props.name);
    }
  }

  render () {
    const checked = this.props.name == this.props.value;
    
    return (
      <div id="metric" className="form-check form-switch d-flex w-auto justify-content-center align-items-center">
        <input className="form-check-input" type="checkbox" id={this.props.name} onChange={this.handleChange} checked={checked}/>
        <label className="form-check-label ps-3" htmlFor={this.props.name}>{this.props.name}</label>
      </div>
    )
  }
}

export default Metric;
