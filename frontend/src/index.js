import React from 'react';
import ReactDOM from 'react-dom/client';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import Navbar from './components/Navbar';
import Recipe from './components/Recipe';
import Footer from './components/Footer';


class RecipeDex extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      time: 0,
      title: "",
      metric: "default",
      servings: 1,
      ingredients: [],
      instructions: []
    };

    this.handleUrlSubmit = this.handleUrlSubmit.bind(this);
    this.handleTimeChange = this.handleTimeChange.bind(this);
    this.handleTitleChange = this.handleTitleChange.bind(this);
    this.handleMetricChange = this.handleMetricChange.bind(this);
    this.handleServingChange = this.handleServingChange.bind(this);
    this.handleIngredientChange = this.handleIngredientChange.bind(this);
    this.handleInstructionsChange = this.handleInstructionsChange.bind(this);
  }

  handleUrlSubmit(value) {
    fetch('http://127.0.0.1:5000/recipes/' + encodeURIComponent(value))
      .then((response) => response.json())
      .then((data) => {
        const recipe_data = data[value];

        this.handleMetricChange("default");
        this.handleTimeChange(recipe_data.time);
        this.handleTitleChange(recipe_data.name);
        this.handleServingChange(recipe_data.servings);
        this.handleIngredientChange(recipe_data.ingredients_list);
        this.handleInstructionsChange(recipe_data.instructions);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }

  handleTimeChange(value){
    this.setState({time: value});
  }

  handleTitleChange(value){
    this.setState({title: value});
  }

  handleMetricChange(value){
    this.setState({metric: value});
  }

  handleServingChange(value){
    this.setState({servings: value});
  }

  handleIngredientChange(value){
    this.setState({ingredients: value});
  }

  handleInstructionsChange(value){
    this.setState({instructions: value});
  }

  render() {
    return (
      <React.StrictMode>
        <Navbar
          url={this.state.url}
          onUrlSubmit={this.handleUrlSubmit} />
        <Recipe 
          time={this.state.time}
          title={this.state.title}
          metric={this.state.metric}
          servings={this.state.servings}
          ingredients={this.state.ingredients}
          instructions={this.state.instructions}
          onMetricChange={this.handleMetricChange}
          onServingChange={this.handleServingChange} />
        <Footer />
      </React.StrictMode>
    );
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<RecipeDex />);
