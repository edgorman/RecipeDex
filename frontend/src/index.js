import React from 'react';
import ReactDOM from 'react-dom/client';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import Navbar from './components/Navbar';
import Recipe from './components/Recipe';
import Footer from './components/Footer';
import Introduction from './components/Introduction';
import ResultPanel from './components/ResultPanel';


class RecipeDex extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      search: "",
      recipe: {
        url: "",
        time: -1,
        tags: [],
        unit: "",
        image: "",
        title: "",
        serving: -1,
        ingredients: [],
        instructions: []
      },
      recents: {},
      results: {},
    };

    this.getRecipe = this.getRecipe.bind(this);
    this.getRecents = this.getRecents.bind(this);
    this.getResults = this.getResults.bind(this);
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.handleSearchSubmit = this.handleSearchSubmit.bind(this);
    this.handleRecipeChange = this.handleRecipeChange.bind(this);
    this.handleRecentsChange = this.handleRecentsChange.bind(this);
    this.handleResultsChange = this.handleResultsChange.bind(this);

    this.getRecents();
  }

  getRecipe(url){
    return new Promise(resolve => {
      fetch('http://127.0.0.1:5000/recipes/' + encodeURIComponent(url))
        .then((response) => response.json())
        .then((data) => {
          if (!(url in data)) {
            throw new Error("Could not parse URL '"+url+"'.");
          }
          resolve(data[url]);
        })
        .catch((err) => {
          console.log(err.message);
          resolve({});
        });
    });
  }

  getRecents(){
    const limit = this.state.recents.length;
    
    // TODO: query backend endpoint and get recents
    //       this will likely have the recipe details autofilled
    //       for now we will use `getRecipe` to populate the info
    this.state.recents = {
      "https://www.bbcgoodfood.com/recipes/pizza-margherita-4-easy-steps": {},
      "https://www.bbcgoodfood.com/recipes/keto-pizza": {},
      "https://www.bbcgoodfood.com/recipes/sourdough-pizza": {},
      "https://www.bbcgoodfood.com/recipes/easy-garlic-mayonnaise": {},
      "https://www.bbcgoodfood.com/recipes/easy-vegetarian-chilli": {},
      "https://www.bbcgoodfood.com/recipes/easy-baba-ganoush": {},
    }

    Object.keys(this.state.recents).forEach(async function(url) {
      const recipe = await this.getRecipe(url);
      this.handleRecentsChange({
        [url]: recipe
      })
    }, this);
  }

  getResults(){
    const limit = 12;
    // TODO: query backend endpoint and get results
  }

  handleSearchChange(value){
    this.setState({search: value});
    // TODO: query database endpoint and update results
  }

  async handleSearchSubmit(value) {
    this.handleSearchChange(value);
    this.handleRecipeChange({
      url: "",
      time: -1,
      tags: [],
      unit: "",
      image: "",
      title: "",
      serving: -1,
      ingredients: [],
      instructions: []
    });
    
    // TODO: other checks this is a valid URL
    if (value.length > 0) {
      const result = await this.getRecipe(value);

      this.handleRecipeChange({
        url: value,
        time: result.time,
        tags: result.tags,
        unit: "default",
        image: result.image_url,
        title: result.name,
        serving: result.servings,
        ingredients: result.ingredients_list,
        instructions: result.instructions
      });
    }
  }

  handleRecipeChange(update){
    for (const[key, value] of Object.entries(update)){
      this.setState(prevState => ({
        recipe: {
          ...prevState.recipe,
          [key]: value
        }
      }));
    }
  }

  handleRecentsChange(update){
    for (const[key, value] of Object.entries(update)){
      this.setState(prevState => ({
        recents: {
          ...prevState.recents,
          [key]: value
        }
      }));
    }
  }

  handleResultsChange(update){
    for (const[key, value] of Object.entries(update)){
      this.setState(prevState => ({
        results: {
          ...prevState.results,
          [key]: value
        }
      }));
    }
  }

  render() {
    let content;
    if (this.state.recipe.url !== "") {
      content = <Recipe 
                  value={this.state.recipe}
                  onSearchSubmit={this.handleSearchSubmit}
                  onRecipeChange={this.handleRecipeChange} />
    }
    else if (this.state.search !== ""){
      content = <ResultPanel
                  value={this.state.results}
                  onSearchSubmit={this.handleSearchSubmit} />
    }
    else{
      content = <Introduction
                  value={this.state.recents}
                  onSearchSubmit={this.handleSearchSubmit}
                  onRecipeChange={this.handleRecipeChange} />
    }

    return (
      <React.StrictMode>
        <Navbar
          value={this.state.search}
          onSearchSubmit={this.handleSearchSubmit}
          onSearchChange={this.handleSearchChange} />
        {
          content
        }
        <Footer />
      </React.StrictMode>
    );
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<RecipeDex />);
