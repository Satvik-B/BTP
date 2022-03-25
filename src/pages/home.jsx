import React, { useState } from 'react';
import axios from 'axios';
import { Box, Button } from '@mui/material';
// import { Box } from '@mui/system';
// import { Link } from 'react-router-dom';
const HomePage = () => {
  const [file, setfile] = useState(null);
  const [fileText, setFileText] = useState(null);
  const [highlight, setHighlight] = useState(null);
  function changeHandler(e){
    e.preventDefault();
    const selected = e.target.files;
    setfile(selected[0]);
  }
  function handleSubmit(){
    console.log('Handle submit called');
    const formData = new FormData();
    formData.append('file', file);
  
    axios.post('/getPdf', formData, {
      headers: {
        'Content-Type' : 'multipart/form-data',
      },
    })
      .then((response) => {
        console.log(response.data['message']);
        console.log(response);
        response.data['txt'] && setFileText(response.data['txt']);
        response.data['highlight'] && setHighlight(response.data['highlight']);
      }).catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  }
  return(<>
    <Button
      variant="contained"
      component="label"
    >
      {/* Upload File */}
      <input
        type="file"
        accept=".pdf"
        hidden
        onChange={changeHandler}
      />
      UPLOAD
    </Button>
    <Button variant="contained" disabled={file==null} onClick={handleSubmit}>Submit</Button>
    <br />
    {
      fileText!=null && highlight!=null && fileText.map((line, ind) => (<Box key={line} sx={{ backgroundColor:(highlight[ind]==1?'blue':null) }}>{ind}: {line}</Box>))
    }
  </>)  ;
};

function Home() {
  return (
    <div>
      <HomePage />
    </div>
  );
}

export default Home;