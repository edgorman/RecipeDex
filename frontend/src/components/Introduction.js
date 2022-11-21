import React from 'react';
import ResultPanel from './ResultPanel';

class Introduction extends React.Component {
  constructor(props) {
    super(props);
  }
  
  render () {
    return (
      <div className="container pt-4 pb-4">
        <div className="row">
          <div className="col-xl-8 col-lg-10">
            <h2 className="border-bottom pb-4 mb-4">Welcome to RecipeDex!</h2>
            <p>
              This is the <b>Recipe</b> in<b>Dex</b>er website where you can enter any URL and automatically parse and extract only the
              information needed to follow the recipe instructions! It uses a large recipe-scraper library from Python combined with
              NLP techniques to extract the ingredients and instructions from the web page, as well as any other useful metadata.
            </p>
            <p>
              To use the website either enter a URL in the search bar or keywords to see recipes that match the terms provided.
              Below are several recipes you can click to see an example of the website in action:
            </p>
            <br/>
            <ResultPanel
              value={this.props.value}
              onSearchSubmit={this.props.onSearchSubmit} />
          </div>
        </div>
      </div>
    )
  }
}

export default Introduction;
