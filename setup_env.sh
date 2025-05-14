#!/bin/bash
# setup_env.sh: Create Python venv, install pip packages, and install faiss-gpu with conda

# 1. Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install pip requirements
pip install -r requirements.txt

# 4. Install faiss-gpu using conda (if conda is available)
if command -v conda &> /dev/null; then
    echo "Installing faiss-gpu with conda..."
    conda install -y -c pytorch faiss-gpu
else
    echo "[WARNING] Conda not found. Please install faiss-gpu manually with conda:"
    echo "    conda install -c pytorch faiss-gpu"
fi

echo "Environment setup complete. Activate with: source venv/bin/activate"
