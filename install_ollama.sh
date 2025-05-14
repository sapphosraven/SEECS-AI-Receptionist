#!/bin/bash
# install_ollama.sh: Script to install Ollama on Linux (x86_64)
# Official instructions: https://ollama.com/download

set -e

# Download and install Ollama (Linux x86_64)
if [ "$(uname -s)" = "Linux" ]; then
    echo "Downloading and installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "Ollama installation complete."
else
    echo "This script is intended for Linux systems only."
fi

echo "To start Ollama, run: ollama serve"
