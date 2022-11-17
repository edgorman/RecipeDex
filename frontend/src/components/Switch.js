import React from 'react';
import './Serving.css';

class Switch extends React.Component {
  render () {
    return (
      <div id="switch" className="form-check form-switch d-flex w-auto justify-content-center align-items-center">
        <input className="form-check-input" type="checkbox" id="flexSwitchCheckDefault"/>
        <label className="form-check-label ps-3" htmlFor="flexSwitchCheckDefault">Unit</label>
      </div>
    )
  }
}

export default Switch;
