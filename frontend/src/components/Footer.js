import React from 'react';

class Footer extends React.Component {
  render () {
    return (
      <div className="container pb-5">
        <br/>
        <small>RecipeDex © {new Date().getFullYear()}</small>
        <br/>
        <a style={{fontSize:"12px"}} href="https://github.com/edgorman/RecipeDex/commit/76ed6a7">Last commit 76ed6a7 by edgorman</a>
      </div>
    )
  }
}

export default Footer;
