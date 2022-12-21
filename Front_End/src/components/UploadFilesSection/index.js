import { Box, Button, Typography } from "@mui/material";
import React, { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
var FormData = require('form-data');

function UploadFilesSection() {
  const { acceptedFiles, getRootProps, getInputProps, isDragActive } =
    useDropzone({ maxFiles: 20 });
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const files = uploadedFiles.map((file) => (
    <Box key={file.path}>
      <Typography variant="body1" key={`${file.path}.name`}>
        <b>File name:</b> {file.path}
      </Typography>
    </Box>
  ));
  
  const BASE_URL = "http://127.0.0.1:5000/";

  async function maskFiles(){
    console.log(uploadedFiles)

    var data = new FormData();
    // console.log("df",data.getHeaders())
    for(let file of uploadedFiles){
      data.append('files',
      file );
    }
    const response = await axios.post(BASE_URL+"mask-files",data,{
      responseType:"blob",
      headers: {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    });

    console.log(response.data);
    var blob = new Blob([response.data], {
        type: response.headers['content-type']
    }); 
    console.log(blob); 
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'masked.zip'); //or any other extension
    document.body.appendChild(link);
    link.click();
  }

  useEffect(() => {
    setUploadedFiles(acceptedFiles);
  }, [acceptedFiles]);

  const onResetClickHandler = useCallback(() => {
    setUploadedFiles([]);
  }, []);

  const { onClick } = getRootProps();

  return (
    <Box>
      <Box {...getRootProps()} className="file-drop-section">
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the files here ...</p>
        ) : (
          <p>Drag 'n' drop files here, or click to select files</p>
        )}
      </Box>
      {uploadedFiles.length > 0 && (
        <Box pt={2} textAlign="left">
          {files}
        </Box>
      )}
      <Box textAlign={"left"} mt={2} display="flex">
        <Box mr={2}>
          <Button color="secondary" variant="contained" onClick={onClick}>
            Select Files
          </Button>
        </Box>
        <Button variant="contained" onClick={onResetClickHandler}>
          Reset
        </Button>
        <Box ml={2}>
          <Button variant="contained" onClick={maskFiles}>
            Mask files
          </Button>
        </Box>
      </Box>
    </Box>
  );
}

export default UploadFilesSection;
