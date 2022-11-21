import React from 'react';
import Result from './Result';

class ResultPanel extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    return (
      <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4">
        {
          Object.keys(this.props.value).map(function(key){
            return (
              <Result 
                key={key}
                url={key}
                value={this.props.value[key]}
                onSubmit={this.props.onSearchSubmit} />
            )
          }, this)  // This is an amazing solution
        }
      </div>
    )
  }
}

export default ResultPanel;
