import React from 'react';
import IngredientPanel from './IngredientPanel';
import InstructionPanel from './InstructionPanel';
import Serving from './Serving';
import Metric from './Metric';
import './Recipe.css';

class Recipe extends React.Component {
  constructor(props) {
    super(props);

    this.refreshPage = this.refreshPage.bind(this);
  }

  refreshPage(e) {
    e.preventDefault();
    this.props.onSearchSubmit(this.props.url);
  }
  
  render () {
    if (this.props.title !== "") {
      return (
        <div className="container pt-4 pb-4">
          <h2 className="d-flex justify-content-between border-bottom pb-3">
            <div>
              {this.props.title}
            </div>
            <div style={{maxHeight:"50px"}} className="d-flex justify-content-between align-items-center">
              <a className="ms-4" target="_blank" href={this.props.url}>
                <img className="recipe-image" src={this.props.image} alt={this.props.image} title="Open original recipe in new tab"/>
              </a>
              <button type="button" className="btn btn-secondary btn-sm ms-2 fs-5" disabled title="Report an error with this recipe">
                <i className="bi bi-exclamation-lg"></i>
              </button>
              <button type="button" className="btn btn-primary btn-sm ms-2 fs-5" onClick={this.refreshPage} title="Refresh the values on this recipe">
                <i className="bi bi-arrow-clockwise"></i>
              </button>
            </div>
          </h2>
          <div className="row pt-4">
            <div className="col-lg-5">
              <div className="row">
                <div className="col-sm-6 pb-4 text-center">
                  <h5>Servings</h5>
                  <Serving 
                    value={this.props.servings}
                    onChange={this.props.onServingChange} />
                </div>
                <div className="col-sm-6 pb-4 text-center">
                  <h5>Units</h5>
                  <Metric 
                    name="Metric"
                    value={this.props.metric}
                    onChange={this.props.onMetricChange} />
                  <Metric 
                    name="Imperial"
                    value={this.props.metric}
                    onChange={this.props.onMetricChange} />
                </div>
                <div className="col-12 text-center">
                  <h5>Time</h5>
                  <p>{this.props.time} mins (~{Math.round(this.props.time / 6) / 10} hours)</p>
                </div>
                <div className="col-12 pb-4">
                  <h5>Ingredients</h5>
                  <IngredientPanel 
                    values={this.props.ingredients} />
                </div>
                <div className="col-12 pb-4">
                  <h5>Tags</h5>
                  <p className="ps-3 pe-1">{this.props.tags.join(", ")}</p>
                </div>
              </div>
            </div>
            <div className="col-lg-7">
              <h5>Instructions:</h5>
              <InstructionPanel 
                values={this.props.instructions} />
            </div>
          </div>
        </div>
      )
    }
    else {
      return (
        <div className="container pt-4 pb-4">
          <h2 className="d-flex justify-content-between border-bottom pb-3 placeholder-glow">
            <span className="placeholder col-5"></span>
            <div>
              <div className="spinner-grow ms-2" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              <div className="spinner-grow ms-2" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              <div className="spinner-grow text-primary ms-2" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          </h2>
          <div className="row pt-4">
            <div className="col-lg-5">
              <div className="row">
              <div className="col-sm-6 pb-4 text-center">
                  <h5>Servings</h5>
                  <div className="spinner-grow" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div className="col-sm-6 pb-4 text-center">
                  <h5>Units</h5>
                  <div className="spinner-grow" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div className="col-12 text-center">
                  <h5>Time</h5>
                  <div className="spinner-grow" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div className="col-12 pb-4">
                  <h5>Ingredients</h5>
                  <p className="card-text placeholder-wave">
                    <span className="placeholder col-9"></span>
                    <span className="placeholder col-7"></span>
                    <span className="placeholder col-8"></span>
                    <span className="placeholder col-9"></span>
                    <span className="placeholder col-5"></span>
                    <span className="placeholder col-8"></span>
                    <span className="placeholder col-7"></span>
                    <span className="placeholder col-6"></span>
                  </p>
                </div>
                <div className="col-12 pb-4">
                  <h5>Tags</h5>
                  <p className="card-text placeholder-wave">
                    <span className="placeholder col-9"></span>
                    <span className="placeholder col-6"></span>
                  </p>
                </div>
              </div>
            </div>
            <div className="col-lg-7">
              <h5>Instructions:</h5>
              <p className="card-text placeholder-wave">
                <span className="placeholder col-9"></span>
                <span className="placeholder col-7"></span>
                <span className="placeholder col-8"></span>
                <span className="placeholder col-9"></span>
                <span className="placeholder col-5"></span>
                <span className="placeholder col-8"></span>
                <span className="placeholder col-7"></span>
                <span className="placeholder col-6"></span>
                <span className="placeholder col-9"></span>
                <span className="placeholder col-7"></span>
                <span className="placeholder col-8"></span>
                <span className="placeholder col-9"></span>
                <span className="placeholder col-5"></span>
                <span className="placeholder col-8"></span>
                <span className="placeholder col-7"></span>
                <span className="placeholder col-6"></span>
              </p>
            </div>
          </div>
        </div>
      )
    }
  }
}

export default Recipe;
