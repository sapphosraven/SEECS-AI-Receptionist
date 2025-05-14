# Deployment Preparation Checklist for SEECS-AI-Receptionist

## 1. Clean Project Directory

- [x] Remove `node_modules` folders (will be reinstalled on target)
- [x] Remove `.venv` or `venv` folders (will be reinstalled on target)
- [x] Remove `__pycache__` folders
- [x] Remove unnecessary cache/temp files
- [x] Ensure only essential code, configs, and data are present

## 2. Ensure Dependency Files Are Up to Date

- [x] All Python dependencies listed in `requirements.txt`
- [x] All Node.js dependencies listed in `package.json` (and `GUI/backend/package.json`)

## 3. Ready for Transfer

- [x] Project folder is organized and ready for upload

---

## Deployment: Conda Environment Setup

To set up the environment using conda (recommended for supercomputer):

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda if not already available.
2. In your project root, run:

   ```powershell
   conda env create -f environment.yml
   conda activate seecs-ai-receptionist
   ```

This will install all dependencies, including faiss-gpu, and pip packages from requirements.txt.

---

## Ollama Installation (Required for LLM)

Ollama must be installed and running on the supercomputer for LLM features to work.

- On Linux, run the provided script:
  ```bash
  bash install_ollama.sh
  ```
- Or follow the official instructions: https://ollama.com/download
- After installation, start the Ollama server:
  ```bash
  ollama serve
  ```
- You may need admin assistance if you lack install permissions.

---

## Alternative: Manual Setup

If you cannot use conda, use the `setup_env.sh` script (Linux/macOS/WSL) or follow the steps in that script manually for Windows.

---

## Job Submission Scripts (SGE)

You can use the following scripts to run your project components on the supercomputer:

- `run_backend.sh`: Starts the backend server (Node.js)
- `run_frontend.sh`: Starts the frontend (Vite/React)
- `run_llm.sh`: Runs the LangGraph Adaptive RAG LLM script

Submit a job with:

```bash
qsub -V run_backend.sh
qsub -V run_frontend.sh
qsub -V run_llm.sh
```

Edit the scripts as needed for your specific entry points or arguments.

---

## SSH Tunneling for Web UI/API Access

If you need to access the web UI or backend API from your local machine, set up SSH port forwarding:

For PowerShell (replace <user>, <external_ip>, and <remote_port> as needed):

```
ssh -L 3000:localhost:3000 <user>@<external_ip> -p 2299
```

- This example forwards remote port 3000 (frontend) to your local port 3000.
- You can add more `-L` options for other services (e.g., backend on 5000).
- After connecting, open http://localhost:3000 in your browser.

You may need to adjust ports based on your app's configuration.

---

**Note:**

- Do not include large generated files, audio outputs, or cache folders unless needed for deployment/testing.
- You can use this checklist before every deployment.
