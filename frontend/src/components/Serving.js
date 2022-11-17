import React from 'react';
import './Serving.css';

class Serving extends React.Component {
  render () {
    return (
      <div id="serving" className="input-group w-auto justify-content-center align-items-center">
        <input type="button" value="-" className="button-minus rounded-circle icon-shape icon-sm mx-1" data-field="quantity"/>
        <input type="number" step="1" max="10" value="1" name="quantity" className="quantity-field border-0 text-center w-25"/>
        <input type="button" value="+" className="button-plus rounded-circle icon-shape icon-sm " data-field="quantity"/>
      </div>
    )
  }
}

export default Serving;
