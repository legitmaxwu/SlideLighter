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

class App extends Component {
  constructor (props) {
    super(props);
    this.regionRenderer = this.regionRenderer.bind(this);
    this.onChange = this.onChange.bind(this);
    this.state = {
      regions: [],
      imgArray: [],
      slideNum: 0
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
      height: this.state.regions[regionProps.index].height * 7.68, 
      width: this.state.regions[regionProps.index].width * 10.24, 
      backgroundColor: 'rgba(255, 255, 0, 0.5)'}}/>
    );
  }

  uploadCoords = async () => {
    const {regions} = this.state;
    for (let i = 0; i < regions.length; i++) {
      http.post('/savepoints', { // FIX DIS SHITE
        x1: regions[i].x,
        x2: regions[i].x + regions[i].width,
        y1: 100 - regions[i].y,
        y2: 100 - (regions[i].y + regions[i].height),
        pageNum: this.state.slideNum + 1,
        fileName: 'test_cal',
      }) 
      .then((result) => {
        console.log(result.data)
      }).catch(err=>console.log(err))
    }
    this.setState(state => {
      return {regions: []}
    })
  }
  
  nextimg = async() => {
    this.uploadCoords();
    this.setState(state => {
      if(state.slideNum < state.imgArray.length - 1){
        return {slideNum: (state.slideNum + 1), regions: []}
      }
    })
  }

  previmg = async() => {
    this.uploadCoords();
    this.setState(state => {
      if (state.slideNum != 0) {
        return {slideNum: (state.slideNum - 1), regions: []}
      }
    })
  }

  getppt = async() => {
    http.post('/requestslides', {
      request: true
    })
    .then(response => {
      console.log(response.data["jpeglinks"])
      this.setState(state => {
        return {imgArray: state.imgArray.concat(response.data["jpeglinks"])}
      })
    })
    .catch(err=>console.log(err))
  }

/*
  importppt = async() => {
    this.setState(state => {
      return {imgArray: state.imgArray.concat(['https://i.imgur.com/6aGu2lh.jpg',
'https://i.imgur.com/hoHdERH.jpg',
'https://i.imgur.com/8FdDSaS.jpg',
'https://i.imgur.com/gay809F.jpg',
'https://i.imgur.com/5AImPPV.jpg',
'https://i.imgur.com/PnXmcr3.jpg',
'https://i.imgur.com/SLAiXFX.jpg',
'https://i.imgur.com/2YId7bv.jpg',
'https://i.imgur.com/NdxKBB4.jpg',
'https://i.imgur.com/jBhKEeH.jpg',
'https://i.imgur.com/IlipFx3.jpg',
'https://i.imgur.com/TUt8ibH.jpg',
'https://i.imgur.com/7oX0Rwr.jpg',
'https://i.imgur.com/bdRQp2c.jpg',
'https://i.imgur.com/hm7ZUd8.jpg',
'https://i.imgur.com/fa2jBkU.jpg',
'https://i.imgur.com/BIm6oak.jpg',
'https://i.imgur.com/mhWnMDs.jpg',
'https://i.imgur.com/OheueRk.jpg'])}
    })
  }
*/

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <div>
            <button style = {{fontSize: "15px"}} id= 'importbutton' onClick={this.getppt}>IMPORT</button>
          </div>
          <div>
            <RegionSelect
              maxRegions={3}
              regions={this.state.regions}
              onChange={this.onChange}
              regionRenderer={this.regionRenderer}
              style={{ border: null }}
            >
              <img id= "slide" src={this.state.imgArray[this.state.slideNum]} width = "1024px" height = "768px"></img>
            </RegionSelect>
            {/* <RegionSelect
            maxRegions={5}
            regions={this.state.regions}
            onChange={this.onChange}
            regionRenderer={this.regionRenderer}>
                <img src='data:image/jpeg;base64,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'/>
            </RegionSelect> */}
          </div>
        </header>
        <div>
          <button style = {{fontSize: "15px"}} onClick= {this.previmg}>PREV</button>
          <button style = {{fontSize: "15px"}} onClick= {this.uploadCoords}>SUBMIT</button>
          <button style = {{fontSize: "15px"}} onClick= {this.nextimg}>NEXT</button>
        </div>
      </div>
    );
  }
}

export default App;
