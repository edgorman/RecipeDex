import React from 'react';
import ReactDOM from 'react-dom/client';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import Navbar from './components/Navbar';
import Recipe from './components/Recipe';
import Footer from './components/Footer';
import Introduction from './components/Introduction';
import Search from './components/Search';
import Error from './components/Error';


class RecipeDex extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errors: [],
      search: "",
      recipe: {
        url: "",
        time: -1,
        tags: [],
        unit: "default",
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
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.handleSearchSubmit = this.handleSearchSubmit.bind(this);
    this.handleRecipeChange = this.handleRecipeChange.bind(this);
    this.handleRecentsChange = this.handleRecentsChange.bind(this);
    this.handleResultsChange = this.handleResultsChange.bind(this);

    this.getRecents();
  }

  getRecipe(url, unit=null, serving=null){
    return new Promise(resolve => {
      let params = "";
      params += unit !== null && serving != null ? "?" : "";
      params += unit !== null ? "unit=" + encodeURIComponent(unit) : "";
      params += unit !== null && serving != null ? "&" : "";
      params += serving !== null ? "serves=" + encodeURIComponent(serving) : "";

      fetch('http://127.0.0.1:5000/recipes/' + encodeURIComponent(url) + params)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);

          if (url in data.data) {
            resolve(data.data[url]);
          }
          else if ("detail" in data){
            this.handleErrorSubmit("You have reached the limit for requests, please wait for one minute before continuing.");
          }
          else {
            this.handleErrorSubmit("Could not scrape a recipe from the URL: '" + url + "'");
          }
        })
        .catch((err) => {
          console.log(err.message);
          resolve({});
        });
    });
  }

  getRecents(){
    const limit = 6;

    fetch('http://127.0.0.1:5000/recipes/recent?limit=' + limit)
      .then((response) => response.json())
      .then((data) => {
        this.setState({recents: []});
        this.handleRecentsChange(data.data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }

  handleErrorSubmit(value){
    this.setState(prevState => ({
      errors: [
        ...prevState.errors,
        value
      ]
    }));
  }

  handleSearchChange(value){
    this.setState({search: value});
    const limit = 12;

    fetch('http://127.0.0.1:5000/search/?limit=' + limit + '&t=' + value.split(" ").join("&t="))
      .then((response) => response.json())
      .then((data) => {
        this.handleRecipeChange({url: ""});
        this.setState({results: []});

        if (data.data.length > 0) {
          data.data.forEach(async function(result) {
            const recipe = await this.getRecipe(result.url);
            this.handleResultsChange({
              [result.url]: recipe
            })
          }, this);
        }
      })
      .catch((err) => {
        console.log(err.message);
      });
  }

  async handleSearchSubmit(value, unit=null, serving=null) {
    if (value !== this.state.recipe.url) {
      this.handleRecipeChange({
        url: "",
        time: -1,
        tags: [],
        unit: "default",
        image: "",
        title: "",
        serving: -1,
        ingredients: [],
        instructions: []
      });
    }
    
    // TODO: other checks this is a valid URL
    if (value.length > 0) {
      this.setState({search: value});
      const result = await this.getRecipe(value, unit, serving);
      
      if (Object.keys(result).length > 0) {
        this.handleRecipeChange({
          url: value,
          time: result.time,
          tags: result.tags,
          unit: result.unit,
          image: result.image,
          title: result.name,
          serving: result.servings,
          ingredients: result.ingredient_list,
          instructions: result.instruction_strs
        });
      }
      else{
        this.handleSearchChange(value);
      }
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
                  onSearchSubmit={this.handleSearchSubmit} />
    }
    else if (this.state.search !== ""){
      content = <Search
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
          onSearchChange={this.handleSearchChange} 
          onRefreshRecents={this.getRecents} />
        {
          content
        }
        <Footer />
        <div className="toast-container position-fixed top-0 end-0 p-3" style={{zIndex: "11"}}>
          {
            this.state.errors.map(function(error, idx){
              const key = "error-" + idx;
              return (
                <Error 
                  key={key}
                  id={key}
                  value={error} />
              )
            })
          }
        </div>
      </React.StrictMode>
    );
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<RecipeDex />);
