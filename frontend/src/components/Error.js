import React from 'react';

class Error extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
        seconds: 1,
        visible: true,
        timeout: 15
    }
  }

  componentDidMount() {
    const interval = setInterval(function(error){
        error.setState({seconds: error.state.seconds + 1});
    }, 1000, this);

    setTimeout(function(error, interval){ 
        clearInterval(interval);
        error.setState({visible: false});
    }, this.state.timeout * 1000, this, interval);
  }
  
  render () {
    const className = "toast " + (this.state.visible ? "show" : "hide");

    return (
      <div id={this.props.id} className={className} role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="true">
        <div className="toast-header">
          <div className="rounded p-2 me-2 bg-danger"></div>
          <strong className="me-auto">Error</strong>
          <small>{this.state.seconds} seconds ago</small>
          <button type="button" className="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div className="toast-body">
          {this.props.value}
        </div>
      </div>
    )
  }
}

export default Error;
