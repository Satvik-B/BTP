import { Box } from '@mui/system';
import React from 'react';

const header = () => {

  function logMeOut() {
    axios({
      method: "POST",
      url:"/logout",
    })
    .then((response) => {
       props.token()
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

  return (
    <Box sx={{ width:'100%', height:'10vh', display:'flex', flexDirection:'row', justifyContent:'space-between' }}>
      <Button variant="contained">Home Page</Button>
      <Button variant="contained" onClick={logOut}>Logout</Button>
    </Box>
  )
}