#!/bin/bash
echo "Pulling required models for LISA..."
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b
ollama pull mistral-nemo
echo "All models pulled successfully."
