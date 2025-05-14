## Conda Environment Setup

If you have conda installed, you can set up the environment with one command:

```powershell
conda env create -f environment.yml
conda activate seecs-ai-receptionist
```

This will install all dependencies, including faiss-gpu and all pip requirements.

If you do not have conda, see the DEPLOYMENT_CHECKLIST.md for alternative setup instructions.

## Ollama Setup for LLM

Ollama is required for local LLM inference. It must be installed and running on the supercomputer.

- To install on Linux, run:
  ```bash
  bash install_ollama.sh
  ```
- Or see the official instructions: https://ollama.com/download
- Start the Ollama server with:
  ```bash
  ollama serve
  ```
- If you do not have install permissions, contact your system administrator.

## Running on the Supercomputer (SGE Job Scripts)

To run the project components, use the provided job scripts:

- `run_backend.sh` (Node.js backend)
- `run_frontend.sh` (React frontend)
- `run_llm.sh` (LangGraph LLM)

Submit jobs with:

```bash
qsub -V run_backend.sh
qsub -V run_frontend.sh
qsub -V run_llm.sh
```

Edit the scripts if your entry points or arguments change.
