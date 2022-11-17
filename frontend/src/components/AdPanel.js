import React from 'react';
import Ad from './Ad';

class AdPanel extends React.Component {
  render () {
    return (
      <div id="adpanel" className="pt-5">
        <Ad />
      </div>
    )
  }
}

export default AdPanel;
