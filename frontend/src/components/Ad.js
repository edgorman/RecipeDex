import React from 'react';

class Ad extends React.Component {
  render () {
    return (
      <div className="card">
        <div className="card-body">
        <h5 class="card-title">Ad title</h5>
        <h6 class="card-subtitle mb-2 text-muted">Ad subtitle</h6>
        <p class="card-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </p>
        <a href="#" class="card-link">Ad link</a>
        </div>
      </div>
    )
  }
}

export default Ad;
