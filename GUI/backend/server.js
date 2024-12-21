const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const WebSocket = require("ws");
const { exec } = require("child_process");

const app = express();
app.use(cors());

// Constants
const DIRECTORY_TO_WATCH = path.join(__dirname, "../public/audios");
const AUDIO_PUBLIC_PATH = path.join(__dirname, "audios");
let latestJsonFile = null;
let lastSentFile = null; // Track the last file sent to clients

// Create a WebSocket server
const wss = new WebSocket.Server({ noServer: true });

// Watch for new files in the directory
fs.watch(DIRECTORY_TO_WATCH, (eventType, filename) => {
  if (eventType === "rename" && filename.endsWith(".json")) {
    const jsonFilePath = path.join(DIRECTORY_TO_WATCH, filename);
    const wavFilePath = jsonFilePath.replace(".json", ".wav");

    // Ensure both files exist
    if (fs.existsSync(jsonFilePath) && fs.existsSync(wavFilePath)) {
      latestJsonFile = { jsonFilePath, wavFilePath };

      // Notify all WebSocket clients that a new file has been added
      if (wss.clients.size > 0) {
        const newAudioFile = `/audios/${path.basename(latestJsonFile.wavFilePath)}`;
        const jsonData = JSON.parse(fs.readFileSync(latestJsonFile.jsonFilePath, "utf-8"));

        // Send data only if the file is new (not the last one sent)
        if (newAudioFile !== lastSentFile) {
          wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
              client.send(JSON.stringify({
                audioFile: newAudioFile,
                jsonData,
              }));
            }
          });

          // Update the last sent file
          lastSentFile = newAudioFile;
        }
      }
    }
  }
});

// WebSocket connection handler
wss.on("connection", (ws) => {
  console.log("New client connected");

  // Send latest file data when a client connects, if it's not the same as the last sent file
  if (latestJsonFile && lastSentFile) {
    const newAudioFile = `/audios/${path.basename(latestJsonFile.wavFilePath)}`;
    if (newAudioFile !== lastSentFile) {
      ws.send(JSON.stringify({
        audioFile: newAudioFile,
        jsonData: JSON.parse(fs.readFileSync(latestJsonFile.jsonFilePath, "utf-8")),
      }));

      // Update the last sent file
      lastSentFile = newAudioFile;
    }
  }
});

// Integrate WebSocket with HTTP server
app.server = app.listen(5000, () => {
  console.log("Server is running on http://localhost:5000");
});

// Handle WebSocket upgrade
app.server.on("upgrade", (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, (ws) => {
    wss.emit("connection", ws, request);
  });
});

// Serve static audio files
app.use("/audios", express.static(DIRECTORY_TO_WATCH));

// Endpoint to run STT script
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
