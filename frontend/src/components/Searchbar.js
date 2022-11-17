import React from 'react';

class Searchbar extends React.Component {
  render () {
    return (
      <form className="container-fluid" role="search">
        <div className="input-group">
          <input type="text" id="url" defaultValue="" className="form-control" placeholder="Search for names, ingredients or enter a URL..."/>
          <button className="btn btn-primary">Search</button>
        </div>
      </form>
    )
  }
}

export default Searchbar;
