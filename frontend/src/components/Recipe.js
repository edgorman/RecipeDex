import React from 'react';
import IngredientPanel from './IngredientPanel';
import InstructionPanel from './InstructionPanel';
import Serving from './Serving';
import Metric from './Metric';
import './Recipe.css';

class Recipe extends React.Component {
  constructor(props) {
    super(props);
  }
  
  render () {
    return (
      <div className="container pt-4 pb-4">
        <h2 className="d-flex justify-content-between border-bottom pb-4">
          {this.props.title}
          <a target="_blank" href={this.props.url}>
            <img className="recipe-image" src={this.props.image} alt={this.props.image}/>
          </a>
        </h2>
        <div className="row pt-3">
          <div className="col-lg-5">
            <div className="row">
              <div className="col-sm-6 pb-4">
                <h5 className="text-center">Servings</h5>
                <Serving 
                  value={this.props.servings}
                  onChange={this.props.onServingChange} />
              </div>
              <div className="col-sm-6 pb-4">
                <h5 className="text-center">Units</h5>
                <Metric 
                  name="Metric"
                  value={this.props.metric}
                  onChange={this.props.onMetricChange} />
                <Metric 
                  name="Imperial"
                  value={this.props.metric}
                  onChange={this.props.onMetricChange} />
              </div>
              <IngredientPanel 
                values={this.props.ingredients} />
            </div>
          </div>
          <div className="col-lg-7">
            <div className="row">
              <div className="col-12">
                <InstructionPanel 
                  values={this.props.instructions} />
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Recipe;
