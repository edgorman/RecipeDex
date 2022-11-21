import React from 'react';
import Instruction from './Instruction';

class InstructionPanel extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    if (this.props.value.length > 0) {
      return (
        <div id="instructionpanel" className="col-12 pb-4">
          <ul className="list-group list-group-flush">
            {
              this.props.value.map(function(instruction, idx){
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
      );
    }
    else {
      return (
        <p className="card-text placeholder-wave">
          <span className="placeholder col-9"></span>
          <span className="placeholder col-7"></span>
          <span className="placeholder col-8"></span>
          <span className="placeholder col-9"></span>
          <span className="placeholder col-5"></span>
          <span className="placeholder col-8"></span>
          <span className="placeholder col-7"></span>
          <span className="placeholder col-6"></span>
          <span className="placeholder col-9"></span>
          <span className="placeholder col-7"></span>
          <span className="placeholder col-8"></span>
          <span className="placeholder col-9"></span>
          <span className="placeholder col-5"></span>
          <span className="placeholder col-8"></span>
          <span className="placeholder col-7"></span>
          <span className="placeholder col-6"></span>
        </p>
      );
    }
  }
}

export default InstructionPanel;
