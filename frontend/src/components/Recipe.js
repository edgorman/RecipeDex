import React from 'react';
import IngredientPanel from './IngredientPanel';
import InstructionPanel from './InstructionPanel';
import Serving from './Serving';
import Unit from './Unit';
import './Recipe.css';

class Recipe extends React.Component {
  constructor(props) {
    super(props);

    this.handleRefresh = this.handleRefresh.bind(this);
    this.handleUpdate = this.handleUpdate.bind(this);
  }

  handleRefresh(e) {
    e.preventDefault();
    this.props.onSearchSubmit(this.props.value.url, this.props.unit, this.props.serves);
  }

  handleUpdate(unit=null, serving=null){
    unit = unit == null ? this.props.value.unit : unit
    serving = serving == null ? this.props.value.serving : serving
    this.props.onSearchSubmit(this.props.value.url, unit, serving);
  }
  
  render () {
    return (
      <div className="container pt-4 pb-4">
        <h2 className="d-flex justify-content-between border-bottom pb-3">
          {
            <Title 
              value={this.props.value.title} />
          }
          {
            <TitleButtons 
              url={this.props.value.url} 
              image={this.props.value.image} 
              onRefresh={this.handleRefresh} />
          }
        </h2>
        <div className="row pt-4">
          <div className="col-lg-5">
            <div className="row">
              <div className="col-sm-6 pb-4 text-center">
                <h5>Servings</h5>
                <Serving 
                  value={this.props.value.serving}
                  onUpdate={this.handleUpdate} />
              </div>
              <div className="col-sm-6 pb-4 text-center">
                <h5>Units</h5>
                <Units
                  value={this.props.value.unit}
                  onUpdate={this.handleUpdate} />
              </div>
              <div className="col-12 text-center">
                <h5>Time</h5>
                <Time
                  value={this.props.value.time} />
              </div>
              <div className="col-12 pb-4">
                <h5>Ingredients</h5>
                <IngredientPanel 
                  value={this.props.value.ingredients} />
              </div>
              <div className="col-12 pb-4">
                <h5>Tags</h5>
                <Tags 
                  value={this.props.value.tags}/>
              </div>
            </div>
          </div>
          <div className="col-lg-7">
            <h5>Instructions:</h5>
            <InstructionPanel 
              value={this.props.value.instructions} />
          </div>
        </div>
      </div>
    )
  }
}

class Title extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.value !== ""){
      return (
        this.props.value
      );
    }
    else{
      return (
        <span className="placeholder placeholder-wave col-5"></span>
      );
    }
  }
}

class TitleButtons extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.url !== ""){
      return (
        <div style={{maxHeight:"50px"}} className="d-flex justify-content-between align-items-center">
          <a className="ms-4" target="_blank" href={this.props.url}>
            <img className="recipe-image" src={this.props.image} alt={this.props.image} title="Open original recipe in new tab"/>
          </a>
          <button type="button" className="btn btn-secondary btn-sm ms-2 fs-5" disabled title="Report an error with this recipe">
            <i className="bi bi-exclamation-lg"></i>
          </button>
          <button type="button" className="btn btn-primary btn-sm ms-2 fs-5" onClick={this.props.onRefresh} title="Refresh the values on this recipe">
            <i className="bi bi-arrow-clockwise"></i>
          </button>
        </div>
      );
    }
    else{
      return (
        <div style={{maxHeight:"50px"}} className="d-flex justify-content-between align-items-center">
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
      );
    }
  }
}

class Units extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.value !== ""){
      return (
        <div>
          <Unit 
            name="metric"
            value={this.props.value}
            onUpdate={this.props.onUpdate} />
          <Unit 
            name="imperial"
            value={this.props.value}
            onUpdate={this.props.onUpdate} />
        </div>
      );
    }
    else{
      return (
        <div className="spinner-grow" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      );
    }
  }
}

class Time extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.value !== -1){
      return (
        <p>
          {this.props.value} mins 
          (~{Math.round(this.props.value / 6) / 10} hours)
        </p>
      );
    }
    else{
      return (
        <div className="spinner-grow" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      );
    }
  }
}

class Tags extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.value.length > 0){
      return (
        <p className="ps-3 pe-1">
          {this.props.value.join(", ")}
        </p>
      );
    }
    else{
      return (
        <p className="card-text placeholder-wave">
          <span className="placeholder col-9"></span>
          <span className="placeholder col-6"></span>
        </p>
      );
    }
  }
}

export default Recipe;
