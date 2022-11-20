import React from 'react';
import ReactDOM from 'react-dom/client';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import Navbar from './components/Navbar';
import Recipe from './components/Recipe';
import Footer from './components/Footer';
import Introduction from './components/Introduction';


class RecipeDex extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      time: 0,
      tags: [],
      image: "",
      title: "",
      search: "",
      metric: "default",
      results: [],
      servings: 1,
      ingredients: [],
      instructions: [],
    };

    this.handleSearchSubmit = this.handleSearchSubmit.bind(this);

    this.handleUrlChange = this.handleUrlChange.bind(this);
    this.handleTagsChange = this.handleTagsChange.bind(this);
    this.handleTimeChange = this.handleTimeChange.bind(this);
    this.handleImageChange = this.handleImageChange.bind(this);
    this.handleTitleChange = this.handleTitleChange.bind(this);
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.handleMetricChange = this.handleMetricChange.bind(this);
    this.handleServingChange = this.handleServingChange.bind(this);
    this.handleIngredientChange = this.handleIngredientChange.bind(this);
    this.handleInstructionsChange = this.handleInstructionsChange.bind(this);
  }

  handleSearchSubmit(value) {
    this.handleUrlChange(value);
    this.handleTagsChange([]);
    this.handleTimeChange(0);
    this.handleImageChange("");
    this.handleTitleChange("");
    this.handleSearchChange(value);
    this.handleMetricChange("default");
    this.handleServingChange(0);
    this.handleIngredientChange([]);
    this.handleInstructionsChange([]);

    if (value.length > 0) {
      fetch('http://127.0.0.1:5000/recipes/' + encodeURIComponent(value))
        .then((response) => response.json())
        .then((data) => {
          if (!(value in data)) {
            throw new Error("Could not parse URL '"+value+"'.");
          }
          const recipe_data = data[value];
          this.handleTagsChange(recipe_data.tags);
          this.handleTimeChange(recipe_data.time);
          this.handleImageChange(recipe_data.image_url);
          this.handleTitleChange(recipe_data.name);
          this.handleMetricChange("default");
          this.handleServingChange(recipe_data.servings);
          this.handleIngredientChange(recipe_data.ingredients_list);
          this.handleInstructionsChange(recipe_data.instructions);
        })
        .catch((err) => {
          console.log(err.message);
        });
    }
  }

  handleUrlChange(value){
    this.setState({url: value});
  }

  handleSearchChange(value){
    this.setState({search: value});
  }

  handleTagsChange(value){
    this.setState({tags: value});
  }

  handleTimeChange(value){
    this.setState({time: value});
  }

  handleTitleChange(value){
    this.setState({title: value});
  }

  handleImageChange(value){
    this.setState({image: value});
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
    if (this.state.url !== "") {
      return (
        <React.StrictMode>
          <Navbar
            value={this.state.search}
            onSearchSubmit={this.handleSearchSubmit}
            onSearchChange={this.handleSearchChange} />
          <Recipe 
            url={this.state.url}
            tags={this.state.tags}
            time={this.state.time}
            image={this.state.image}
            title={this.state.title}
            metric={this.state.metric}
            servings={this.state.servings}
            ingredients={this.state.ingredients}
            instructions={this.state.instructions}
            onSearchSubmit={this.handleSearchSubmit}
            onMetricChange={this.handleMetricChange}
            onServingChange={this.handleServingChange} />
          <Footer />
        </React.StrictMode>
      );
    }
    else {
      return (
        <React.StrictMode>
          <Navbar
            value={this.state.search}
            onSearchSubmit={this.handleSearchSubmit}
            onSearchChange={this.handleSearchChange} />
          <Introduction 
            onSearchSubmit={this.handleSearchSubmit} />
          <Footer />
        </React.StrictMode>
      );
    }
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<RecipeDex />);
