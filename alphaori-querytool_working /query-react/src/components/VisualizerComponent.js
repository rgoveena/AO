import React, { Component } from 'react';
import { Col, Row } from 'reactstrap';

class Visualizer extends Component {
  
  constructor(props) {
    super(props);
    this.state = {image: ''};
    this.handleUploadFile = this.handleUploadFile.bind(this);
  }

  getImg = () => {
    return (this.state.image)
  }


  handleUploadFile(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    //console.log("react fetching from node");
    //console.log(this.uploadInput.files[0]);

    fetch('http://localhost:3001/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then(data => ({
        data: data,
        status: response.status
      }) //only necessary if directly fetching like this
      ).then(res => {
        var file = JSON.stringify(res.data);
        file = file.substring(1,file.length-1);
        this.setState({ image: 'http://localhost:3001/graphs/'+file+'.png' });
      });
    });
  }

  
  render() {
    return (
      <Row>
        <Col md={{offset: 1}}>  
          <br/><br/>
          <form onSubmit={this.handleUploadFile}>
            <div>
              <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
            </div>
            <br/>
            <div>
              <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter file title" />
            </div>
            <br />
            <div>
              <button>Upload</button>
            </div>
          </form>
        </Col>
        <Col>
          <br/><br/>
          <img src={this.getImg()} alt=''/>
        </Col>
      </Row>
    );
  }
}

export default Visualizer;