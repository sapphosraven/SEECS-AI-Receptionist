
// Updated Express Backend
const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(cors());

const directoryToWatch = path.join(__dirname, "watched_directory");
let latestJsonFile = null;

// Watch for new files in the directory
fs.watch(directoryToWatch, (eventType, filename) => {
  if (eventType === "rename" && filename.endsWith(".json")) {
    const jsonFilePath = path.join(directoryToWatch, filename);
    const wavFilePath = jsonFilePath.replace(".json", ".wav");

    if (fs.existsSync(wavFilePath)) {
      latestJsonFile = { jsonFilePath, wavFilePath };
    }
  }
});

// Endpoint to send the latest file data
app.get("/api/get-file", (req, res) => {
  if (latestJsonFile) {
    const jsonData = JSON.parse(fs.readFileSync(latestJsonFile.jsonFilePath, "utf-8"));
    res.json({
      audioFile: `/audios/${path.basename(latestJsonFile.wavFilePath)}`,
      jsonData,
    });
  } else {
    res.status(404).json({ error: "No files available" });
  }
});


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

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
