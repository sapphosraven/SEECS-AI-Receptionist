const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");
const fs = require("fs");
const path = require("path");

const app = express();
const audioDir = path.join(__dirname, "../public/audios"); // Directory to watch for new files

// Use CORS middleware
app.use(cors());

// Endpoint to run the Python script
app.post("/api/run-stt", (req, res) => {
  const scriptPath = "./stt/stt.py"; // Adjust the path if needed

  exec(`python ${scriptPath}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error.message}`);
      return res.status(500).json({ error: "Failed to execute script" });
    }

    if (stderr) {
      console.error(`Script stderr: ${stderr}`);
      return res.status(500).json({ error: "Script execution error" });
    }

    const transcription = stdout.trim();
    res.json({ transcription });
  });
});

// Directory watcher
let latestFiles = null;

fs.watch(audioDir, (eventType, filename) => {
  if (filename && (filename.endsWith(".json") || filename.endsWith(".wav"))) {
    const jsonFile = fs
      .readdirSync(audioDir)
      .find((file) => file.endsWith(".json"));
    const wavFile = fs
      .readdirSync(audioDir)
      .find((file) => file.endsWith(".wav"));

    if (jsonFile && wavFile) {
      latestFiles = {
        jsonFile: path.join(audioDir, jsonFile),
        wavFile: path.join(audioDir, wavFile),
      };

      console.log("New files detected:", latestFiles);
    }
  }
});

// Endpoint to get the latest files
app.get("/api/latest-files", (req, res) => {
  if (latestFiles) {
    res.json(latestFiles);
    latestFiles = null; // Reset after sending to the client
  } else {
    res.status(404).json({ message: "No new files detected." });
  }
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
