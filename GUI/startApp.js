// startApp.js
const { exec } = require('child_process');
const path = require('path');

const pythonScriptPath = "F:\\Uni_Stuff\\5th_Sem\\AI\\Project\\SEECS-AI-Receptionist\\LLM\\RAG-DATA\\local.py";  // Adjust the path accordingly
const backendServerPath = "F:\\Uni_Stuff\\5th_Sem\\AI\\Project\\SEECS-AI-Receptionist\\GUI\\backend\\server.js";  // Adjust the path accordingly

// Start local.py
exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error starting local.py: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`stderr: ${stderr}`);
    return;
  }
  console.log(`local.py output: ${stdout}`);
});

// Start backend server
exec(`node ${backendServerPath}`, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error starting backend server: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`stderr: ${stderr}`);
    return;
  }
  console.log(`Backend server output: ${stdout}`);
});
