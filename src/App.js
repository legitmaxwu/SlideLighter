import React, { Component } from 'react';
import RegionSelect from 'react-region-select';
import ReactTable from "react-table";
import 'react-table/react-table.css'
import './App.css';
import axios from 'axios';
import Tabs from './tabs';
import { strict } from 'assert';

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
      slideNum: 0,
      data: [],
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
        console.log(result)
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
      if (state.slideNum !== 0) {
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

  generate = async() => {
    http.post('/generate', { 
      
    }) 
    .then((result) => {
      console.log(result);
      this.setState(state => {
        let temp = [];
        for (let key in result.data.dictionary) {
          temp.push({word: key, metric: result.data.dictionary[key]});
        }
        return {data: temp}
      })

      console.log(this.state.data);
    }).catch(err=>console.log(err))
  }
  render() {
    const columns = [{
      Header: 'Concept',
      accessor: 'word' // String-based value accessors!
    }, {
      Header: 'Importance',
      accessor: 'metric',
    },]

    return (
      <div className="App">
        <div className="App-header">
          <Tabs>
            <div label="Slides">
              <div>
                <div>
                  <button style = {{fontSize: "25px", margin: "5px"}} id= 'importbutton' onClick={this.getppt}>IMPORT</button>
                </div>
                <div>
                  <RegionSelect
                    maxRegions={5}
                    regions={this.state.regions}
                    onChange={this.onChange}
                    regionRenderer={this.regionRenderer}
                    style={{ border: null }}
                  >
                    <img id= "slide" src={this.state.imgArray[this.state.slideNum]} width = "1024px" height = "768px"></img>
                  </RegionSelect>
                </div>
                <div>
                  <button style = {{fontSize: "25px", margin: "5px"}} onClick= {this.previmg}>PREV</button>
                  <button style = {{fontSize: "25px", margin: "5px"}} onClick= {this.uploadCoords}>SUBMIT</button>
                  <button style = {{fontSize: "25px", margin: "5px"}} onClick= {this.nextimg}>NEXT</button>
                </div>
              </div>
            </div>

            <div label="Concepts">
              <button style = {{fontSize: "25px", margin: "5px"}} onClick= {this.generate}>GENERATE CONCEPTS</button>
              <div style={{backgroundColor:"#565b63"}}>
                <ReactTable
                  data={this.state.data}
                  columns={columns}
                  defaultSorted={[
                    {
                      id: "metric",
                      desc: true,
                    }
                  ]}
                  defaultPageSize={8}
                />
              </div>
            </div>

            <div label="Instructions">
              <div style={{width: '60%', margin: 'auto'}}>
                <h4>
                  To highlight slides:
                </h4>
                <p>
                  Go to <b>Slides</b>. Press <b>IMPORT</b>, enable running unsafe scripts in your URL bar if needed (we promise that our program is non-malicious), and click/drag to draw highlight boxes on the slides. Make sure to click <b>SUBMIT</b> so the program can track your highlights! Use <b>PREV</b> and <b>NEXT</b> to navigate the slides.
                </p>
                <h4>
                  To generate a concept map:
                </h4>
                <p>
                  Go to <b>Concepts</b>. Press <b>GENERATE CONCEPTS</b> to generate a table of important key terms based on what you're "confused" about (what you highlighted!). Note that the table will be empty unless you've submitted a few highlights.
                </p>
              </div>
            </div>
          </Tabs>
        </div>
      </div>
    );
  }
}

export default App;
