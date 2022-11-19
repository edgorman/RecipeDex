import React from 'react';
import './Result.css';

class Result extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      title: "",
      image: "",
      description: ""
    };
    
    this.handleClick = this.handleClick.bind(this);

    fetch('http://127.0.0.1:5000/recipes/' + encodeURIComponent(this.props.url))
      .then((response) => response.json())
      .then((data) => {
        const recipe_data = data[this.props.url];
        const description = recipe_data.instructions.join(" ").slice(0, 150) + "...";

        this.setState({
            title: recipe_data.name,
            image: recipe_data.image_url,
            description: description
        });
      })
      .catch((err) => {
        console.log(err.message);
      });
  }

  handleClick(e){
    e.preventDefault();
    this.props.onSubmit(this.props.url);
  }
  
  render () {
    if (this.state.title !== "") {
      return (
        <div className="example-recipe col" onClick={this.handleClick}>
          <div className="card">
            <img src={this.state.image} className="card-img-top" alt={this.state.image}/>
            <div className="card-body">
              <h5 className="card-title">{this.state.title}</h5>
              <p className="card-text">{this.state.description}</p>
            </div>
          </div>
        </div>
      )
    }
    else{
      return (
        <div className="example-recipe col">
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
