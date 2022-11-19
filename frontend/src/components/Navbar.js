import React from 'react';
import Searchbar from './Searchbar';

class Navbar extends React.Component {
  constructor(props) {
    super(props);
    this.resetUrl = this.resetUrl.bind(this);
  }

  resetUrl(e){
    e.preventDefault();
    this.props.onUrlSubmit("");
  }

  render () {
    return (
      <nav className="navbar navbar-expand-sm mt-3 mb-3">
        <div className="container">
          <a className="navbar-brand fw-bold" href="#" onClick={this.resetUrl}>RecipeDex</a>
          <Searchbar 
            value={this.props.url}
            onSubmit={this.props.onUrlSubmit}/>
        </div>
      </nav>
    )
  }
}

export default Navbar;
