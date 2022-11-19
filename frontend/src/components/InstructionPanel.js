import React from 'react';
import Instruction from './Instruction';

class InstructionPanel extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    return (
      <div id="instructionpanel" className="col-12 pb-4">
        <h5>Instructions:</h5>
        <ul className="list-group list-group-flush">
          {
            this.props.values.map(function(instruction, idx){
              const key = "instruction-" + idx;
              return (
                <Instruction 
                  key={key}
                  value={instruction} />
              )
            })
          }
        </ul>
      </div>
    )
  }
}

export default InstructionPanel;
