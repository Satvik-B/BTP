import { TextField, Typography, Box, Button } from '@mui/material';
import axios from 'axios';
import React, { useState } from 'react';
import validator from 'validator';

const User = () => {
  const [signup, setSignup] = useState({
    name: null,
    email: null,
    pass: null,
  });

  const [message, setMessage] = useState(null);
  function handleChange(event) { 
    const { value, name } = event.target;
    console.log(value);
    console.log(name);
    setSignup(prevNote => ({ ...prevNote, [name]: value }));
  }

  function handleEmail(event){
    const { value, name } = event.target;
    if(validator.isEmail(value)) setSignup(prevNote => ({ ...prevNote, [name]: value }));
    else setSignup(prevNote => ({ ...prevNote, [name]:'' }));
  }

  function handleSubmit(event){
    axios({
      method: 'POST',
      url:'/register',
      data:{
        email: signup.email,
        password: signup.pass,
        name: signup.name,
      },
    })
      .then((response) => {
        console.log(response);
        if(response.data['message']=='User already exist.') setMessage(response.data['message']+' Try Again.');
        else history.push('/userLogin');
      }).catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });

    setSignup((
      {
        email: null,
        password: null,
      }
    ));
    event.preventDefault();
  }

  return (
    <Box sx={{ justifyContent: 'center', display:'flex', alignItems:'center', textAlign:'center', flexDirection:'column' }}>
      <Typography variant="h3">
        User Sign Up
      </Typography>
      <TextField
        required
        error={signup['name']===''}
        id="outlined-error"
        label="Enter Name"
        placeholder="Name"
        name="name"
        onChange={handleChange}
        onClick={handleChange}
        helperText={signup['name']==='' && 'Name is required'}
        sx={{ width:['100%', '50%'], m:'2%' }}
      />
      <TextField
        required
        type="email"
        error={signup['email']===''}
        id="outlined-error"
        label="Enter Email"
        placeholder="Email"
        name="email"
        onChange={handleEmail}
        onClick={handleEmail}
        helperText={signup['email']==='' && 'Email is required'}
        sx={{ width:['100%', '50%'], m:'2%' }}
      />
      <TextField
        required
        error={signup['pass']===''}
        type="password"
        id="outlined-error"
        label="Enter Password"
        placeholder="Password"
        name="pass"
        onChange={handleChange}
        onClick={handleChange}
        helperText={signup['pass']==='' && 'Password is required'}
        sx={{ width:['100%', '50%'], m:'2%' }}
      />
      <Button variant="contained" onClick={handleSubmit} disabled={signup['name']==='' || signup['email']==='' || signup['pass']===''}>Submit</Button>
      {message}
    </Box>
  );
};

function UserSignUp ()
{
  return(
    <div>
      <User />
    </div>
  );
}

export default UserSignUp;