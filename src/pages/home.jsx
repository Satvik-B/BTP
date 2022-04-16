import React, { useState } from 'react';
import axios from 'axios';
import { Box, Button, Typography } from '@mui/material';
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
    console.log(selected[0]);
  }
  function handleSubmit(){
    console.log('Handle submit called');
    const formData = new FormData();
    formData.append('file', file);
    if(file.size>=15728640)
    {
      console.log('size is more than allowed please try again.');
      window.location.reload(true);
      return;
    }
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
    <Box m={4}></Box>
    <Button
      variant="contained"
      component="label"
      sx={{ margin: '5%' }}
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
    <Button variant="contained" disabled={file==null} onClick={handleSubmit} sx={{ margin: '5%' }}>Submit</Button>
    <Typography>
      {file!=null?file.name:null}
    </Typography>
    <Box m={4}></Box>
    <Box sx={{ display: 'inline-block', flexDirection: 'column', alignItems: 'left', justifyContent:'left', textAlign:'left', backgroundColor:'white', borderRadius:'10px' }}>
      {
        fileText!=null && highlight!=null && fileText.map((line, ind) => 
          <>
            {
              (line.split('\n').map((part, item) => (
                <>
                  {item!=0?<br />:null}
                  <Typography key={ind*fileText.len+item} sx={{ display:'inline-block', justifyContent:'space-between', backgroundColor:(highlight[ind]==1?'yellow':null), margin:'-1', color:'black' }}>
                    {part}
                  </Typography>
                </>
              )))
            }
            {/* <p> */}
            &nbsp;
            {/* </p> */}
          </>,
        )
      }
    </Box>
    <Box m={4}></Box>
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