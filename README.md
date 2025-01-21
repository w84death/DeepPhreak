# DeepPhreak - Personal AI Companion

██████╗ ███████╗███████╗██████╗ ██████╗ ██╗  ██╗██████╗ ███████╗ █████╗ ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██║  ██║██╔══██╗██╔════╝██╔══██╗██║ ██╔╝
██║  ██║█████╗  █████╗  ██████╔╝██████╔╝███████║██████╔╝█████╗  ███████║█████╔╝ 
██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔═══╝ ██╔══██║██╔══██╗██╔══╝  ██╔══██║██╔═██╗ 
██████╔╝███████╗███████╗██║     ██║     ██║  ██║██║  ██║███████╗██║  ██║██║  ██╗
╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝

## Overview
A PyQt5-based chatbot UI powered by a local Ollama server running DeepSeek-R1. Conversations are logged daily, and each new day includes a scripted learning step for knowledge retention and improved responses.

## Requirements
- Python 3.9+
- PyQt5
- Ollama server with DeepSeek-R1 model
- Scripts for daily log parsing, embedding, and model retraining/RAG pipeline

## Plan
1. **UI**: 
   - PyQt5 main window with chat display and input box.
   - Log chat exchanges in date-based files.
2. **Server Integration**: 
   - Query Ollama via HTTP/WebSocket calls.
   - Display responses in the chat window.
3. **Daily Learning**: 
   - Scripts to parse the previous day’s chat logs.
   - Update embeddings and retrain or fine-tune model with user-specific knowledge.
4. **Next Steps**:
   - Add user profile management, improved context handling, and advanced data visualization for chat statistics.