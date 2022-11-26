import React from 'react';
import Searchbar from './Searchbar';

class Navbar extends React.Component {
  constructor(props) {
    super(props);
    this.resetSearch = this.resetSearch.bind(this);
  }

  resetSearch(e){
    e.preventDefault();
    this.props.onSearchSubmit("");
    this.props.onSearchChange("");
    this.props.onRefreshRecents();
  }

  render () {
    return (
      <nav className="navbar navbar-expand-sm mt-3 mb-3">
        <div className="container">
          <a className="navbar-brand fw-bold" href="#" onClick={this.resetSearch}>RecipeDex</a>
          <Searchbar 
            value={this.props.value}
            onSubmit={this.props.onSearchSubmit}
            onChange={this.props.onSearchChange} />
        </div>
      </nav>
    )
  }
}

export default Navbar;
