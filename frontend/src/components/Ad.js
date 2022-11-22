import React from 'react';

class Ad extends React.Component {
  render () {
    return (
      <div className="card">
        <div className="card-body">
        <h5 className="card-title">Ad title</h5>
        <h6 className="card-subtitle mb-2 text-muted">Ad subtitle</h6>
        <p className="card-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </p>
        <a href="#" className="card-link">Ad link</a>
        </div>
      </div>
    )
  }
}

export default Ad;
