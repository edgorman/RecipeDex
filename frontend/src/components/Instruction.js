import React from 'react';

class Instruction extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    return (
      <li className="list-group-item">{this.props.value}</li>
    )
  }
}

export default Instruction;
