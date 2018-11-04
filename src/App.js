import React, { Component } from 'react';
import logo from './logo.svg';
import objectAssign from 'object-assign';
import RegionSelect from 'react-region-select';
import './App.css';

import axios from 'axios';

const serverURL = 'http://10.142.173.86:5000'

const http = axios.create({
  baseURL: serverURL,
});

// const language = require('@google-cloud/language');

// const client = new language.v1beta2.LanguageServiceClient({
//   // optional auth parameters.
// });

// const document = {};
// const features = {};
// const request = {
//   document: document,
//   features: features,
// };
// client.annotateText(request)
//   .then(responses => {
//     const response = responses[0];
//     // doThingsWith(response)
//   })
//   .catch(err => {
//     console.error(err);
//   });

class App extends Component {
  constructor (props) {
		super(props);
		this.regionRenderer = this.regionRenderer.bind(this);
		this.onChange = this.onChange.bind(this);
		this.state = {
			regions: []
    };
	}
	onChange (regions) {
		this.setState({
      regions: regions
    });
	}
	regionRenderer (regionProps) {
		return (
      <div style={{ position: 'absolute', left: 0,
      pointerEvents: 'none',
      height: this.state.regions[regionProps.index].height * 3.84, 
      width: this.state.regions[regionProps.index].width * 5.12, 
      backgroundColor: 'rgba(255, 255, 0, 0.5)'}}>
      </div>
		);
  }
  // getdict = async () => {
  //   http.post('/getdict', { // FIX DIS SHITE
  //   }) 
  //   .then((result) => {
  //     console.log(result)
  //   }).catch(err=>console.log(err))
  // }
  uploadCoords = async () => {
    const {regions} = this.state;
    for (let i = 0; i < regions.length; i++) {
      document.write('(' + regions[i].x + ' ' + regions[i].y + ' ' + (100 - regions[i].x - regions[i].width) + ' ' + (100 - regions[i].y - regions[i].height) + ')')
      document.write("\n");
      http.post('/savepoints', { // FIX DIS SHITE
        x1: regions[i].x,
        x2: regions[i].x + regions[i].width,
        y1: 100 - regions[i].y,
        y2: 100 - (regions[i].y + regions[i].height),
        pageNum: 1,
        fileName: 'test',
      }) 
      .then((result) => {
        console.log(result)
      }).catch(err=>console.log(err))
    }
  }
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>box shit plz</p>
          <div>
            <RegionSelect
              maxRegions={3}
              regions={this.state.regions}
              onChange={this.onChange}
              regionRenderer={this.regionRenderer}
              style={{ border: '10px solid yellow' }}
            >
              <img src='https://i.imgur.com/cZZszWQ.jpg' height='384px' width='512px'></img>
            </RegionSelect>
          </div>
        </header>
        <div>
          <button onClick={this.uploadCoords}>
            <p>MOTHAFUCKA</p>
          </button>
        </div>
        <div>
          <p>yeet?</p>
        </div>
      </div>
    );
  }
}

export default App;
