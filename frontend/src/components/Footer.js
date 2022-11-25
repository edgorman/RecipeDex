import React from 'react';
import version from './Version.js'

class Footer extends React.Component {
  
  render () {
    const link = "https://github.com/edgorman/RecipeDex/commit/" + version;

    return (
      <div className="container pb-5">
        <br/>
        <small>RecipeDex © {new Date().getFullYear()}</small>
        <br/>
        <a target="_blank" style={{fontSize:"12px"}} href={link}>v.{version}</a>
      </div>
    )
  }
}

export default Footer;
