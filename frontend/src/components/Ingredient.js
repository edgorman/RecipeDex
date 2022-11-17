import React from 'react';

class Ingredient extends React.Component {
  render () {
    return (
      <div id="ingredient-1" className="pt-3 ps-2 pe-2">
        <div className="input-group">
          <input type="text" className="form-control" defaultValue="egg"/>
          <span className="input-group-text">2</span>
          <span className="input-group-text">count</span>
        </div>
        <div className="input-group">
          <input type="text" className="form-control" defaultValue="beaten or whatever"/>
        </div>
      </div>
    )
  }
}

export default Ingredient;
