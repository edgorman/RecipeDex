import React from 'react';
import ResultPanel from './ResultPanel';

class Search extends React.Component {
  constructor(props) {
    super(props);
  }
  
  render () {
    return (
      <div className="container pt-4 pb-4">
        <div className="row">
          <div className="col-xl-8 col-lg-10">
            <h2 className="border-bottom pb-4 mb-4">Search results...</h2>
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

export default Search;
