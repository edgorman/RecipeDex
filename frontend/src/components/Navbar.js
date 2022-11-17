import React from 'react';
import Searchbar from './Searchbar';

class Navbar extends React.Component {
  render () {
    return (
      <nav className="navbar navbar-expand-sm mt-3 mb-3">
        <div className="container">
          <a className="navbar-brand fw-bold" href="#">RecipeDex</a>
          <Searchbar />
        </div>
      </nav>
    )
  }
}

export default Navbar;
