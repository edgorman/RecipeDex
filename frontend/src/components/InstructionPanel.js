import React from 'react';
import Instruction from './Instruction';
import Serving from './Serving';
import Switch from './Switch';

class RecipePanel extends React.Component {
  render () {
    return (
      <div id="recipepanel" className="col-12 pb-4">
        <h5>Instructions:</h5>
        <ul className="list-group list-group-flush">
          <Instruction />
          <Instruction />
          <Instruction />
          <Instruction />
          <Instruction />
          <Instruction />
          <Instruction />
        </ul>
      </div>
    )
  }
}

export default RecipePanel;
