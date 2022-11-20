import React from 'react';

class Searchbar extends React.Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSubmit(e) {
    e.preventDefault();
    this.props.onSubmit(e.target.elements.search.value);
  }

  handleChange(e) {
    this.props.onChange(e.target.value);
  }

  render () {
    return (
      <form className="container-fluid" role="search" onSubmit={this.handleSubmit}>
        <div className="input-group">
          <input type="text" id="search" value={this.props.value} onChange={this.handleChange} className="form-control" placeholder="Search for names, ingredients or enter a URL..."/>
          <button className="btn btn-primary">Search</button>
        </div>
      </form>
    )
  }
}

export default Searchbar;
