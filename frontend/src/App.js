import './App.css';
import React from 'react';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      name: "",
      servings: "",
      time: "",
      ingredients: [],
      instructions: []
    };
  }

  handleChange = (event) => {
    this.setState({url: event.target.value});
  }

  handleSubmit = (event) => {
    event.preventDefault();

    fetch('http://127.0.0.1:5000/recipes/' + encodeURIComponent(this.state.url))
      .then((response) => response.json())
      .then((data) => {
        var recipe = data[this.state.url];
        console.log(recipe);
        this.setState({
          name: recipe.name,
          servings: recipe.servings,
          time: recipe.time,
          ingredients: recipe.ingredients_list,
          instructions: recipe.instructions
        })
      })
      .catch((err) => {
        console.log(err.message);
      });
  }

  render () {
    return (
      <div className="container">
        <form onSubmit={this.handleSubmit}>
          <div className="p-3">
            <label htmlFor="url">Recipe URL</label>
            <div className="input-group pt-1">
              <input type="text" id="url" defaultValue={this.state.url} onChange={this.handleChange} className="form-control" placeholder="Enter a Recipe URL"/>
              <button className="btn btn-primary">Search</button>
            </div>
          </div>
        </form>
        <form className="form-floating">
          <fieldset disabled>
            <div className="p-3">
              <label htmlFor="name">Name</label>
              <input type="text" id="name" className="form-control" defaultValue={this.state.name}/>
              <label htmlFor="servings">Servings</label>
              <input type="text" id="servings" className="form-control" defaultValue={this.state.servings}/>
              <label htmlFor="time">Cooking Time</label>
              <input type="text" id="time" className="form-control" defaultValue={this.state.time}/>
              <label htmlFor="ingredients">Ingredients</label>
              <ul className="list-group list-group-flush">
                  {
                    this.state.ingredients.map(function(i, idx){
                      return (
                        <div key={idx} className="input-group mt-1 mb-1">
                          <input type="text" className="form-control" defaultValue={i.name}/>
                          <input type="text" className="form-control" defaultValue={i.comment}/>
                          <span className="input-group-text">{i.quantity}</span>
                          <span className="input-group-text">{i.unit}</span>
                        </div>
                      )
                    })
                  }
              </ul>
              <label htmlFor="instructions">Instructions</label>
              <ul className="list-group list-group-flush">
                  {
                    this.state.instructions.map(function(i, idx){
                      return (<li className="list-group-item" key={idx}>{i}</li>)
                    })
                  }
              </ul>
            </div>
          </fieldset>
        </form>
      </div>
    );
  }
}

export default App;
