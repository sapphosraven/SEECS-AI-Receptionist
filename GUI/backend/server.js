const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();

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

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
