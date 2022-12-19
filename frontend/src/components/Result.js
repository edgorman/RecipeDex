import React from 'react';
import './Result.css';

class Result extends React.Component {
  constructor(props) {
    super(props);
    
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e){
    e.preventDefault();
    this.props.onSubmit(this.props.value.url);
  }
  
  render () {
    if ("name" in this.props.value && "instruction_strs" in this.props.value) {
      const description = this.props.value.instruction_strs.join(" ").substring(0, 150)

      return (
        <div className="example-recipe col" onClick={this.handleClick}>
          <div className="card">
            <img src={this.props.value.image} className="card-img-top" alt={this.props.value.name}/>
            <div className="card-body">
              <h5 className="card-title">{this.props.value.name}</h5>
              <p className="card-text">{description}...</p>
            </div>
          </div>
        </div>
      )
    }
    else{
      return (
        <div className="col">
          <div className="card">
            <div className="d-flex justify-content-center pt-5 pb-5">
              <div className="spinner-grow text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
            <div className="card-body">
              <h5 className="card-title placeholder-glow">
                <span className="placeholder col-6"></span>
              </h5>
              <p className="card-text placeholder-glow">
                <span className="placeholder col-7"></span>
                <span className="placeholder col-4"></span>
                <span className="placeholder col-4"></span>
                <span className="placeholder col-6"></span>
                <span className="placeholder col-8"></span>
              </p>
            </div>
          </div>
        </div>
      )
    }
  }
}

export default Result;
