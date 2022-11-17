import React from 'react';
import AdPanel from './AdPanel';
import IngredientPanel from './IngredientPanel';
import InstructionPanel from './InstructionPanel';
import Serving from './Serving';
import Switch from './Switch';

class Recipe extends React.Component {
  render () {
    return (
      <div className="container pt-4 pb-4">
        <h2 className="border-bottom pb-4">Recipe Name</h2>
        <div className="row pt-3">
          <div className="col-lg-4">
            <div className="row pb-5">
              <div className="col-lg-12 col-md-6">
                <IngredientPanel />
              </div>
              <div className="col-lg-12 col-md-6">
                <AdPanel />
              </div>
            </div>
          </div>
          <div className="col-lg-8">
            <div className="row">
              <div className="col-sm-6 pb-4">
                <h5 className="text-center">Servings</h5>
                <Serving />
              </div>
              <div className="col-sm-6 pb-4">
                <h5 className="text-center">Units</h5>
                <Switch />
                <Switch />
              </div>
              <InstructionPanel />
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Recipe;
