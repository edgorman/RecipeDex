import React from 'react';
import ResultPanel from './ResultPanel';

class Search extends React.Component {
  constructor(props) {
    super(props);
  }
  
  render () {
    return (
      <div className="container pt-4 pb-4">
        <div className="row">
          <div className="col-xl-8 col-lg-10">
            <h2 className="border-bottom pb-4 mb-4">Search results...</h2>
            <br/>
            <ResultPanel
              value={this.props.value}
              onSearchSubmit={this.props.onSearchSubmit} />
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5255512781190546" crossOrigin="anonymous"></script>
            <ins className="adsbygoogle"
              style={{display:"block"}}
              data-ad-client="ca-pub-5255512781190546"
              data-ad-slot="3758051723"
              data-ad-format="auto"
              data-full-width-responsive="true"/>
            <script>
              (adsbygoogle = window.adsbygoogle || []).push({});
            </script>
          </div>
        </div>
      </div>
    )
  }
}

export default Search;
