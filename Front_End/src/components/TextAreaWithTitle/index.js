import { Box, Typography } from '@mui/material'
import React, { useState } from 'react'

function TextAreaWithTitle(props) {
  const {title} = props
  const textChangeHandler = (e) => {
    props.setText(e.target.value)
  }
  return (
    <Box flex={1}>
      <Box mb={1}>
        <Typography variant='h6'>{title}</Typography>
      </Box>
      <textarea value={props.text} onChange={textChangeHandler} className='textarea' disabled={props.disable}/>
    </Box>
  )
}

export default TextAreaWithTitle