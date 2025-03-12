# Chat RAG Application

A modern Retrieval-Augmented Generation (RAG) system for enhanced conversational AI experiences.

## Overview

This project implements a RAG-based chat application that combines the power of large language models with information retrieval capabilities. By augmenting AI responses with relevant context from a knowledge base, the system provides more accurate, informative, and up-to-date answers.

## Features

- Contextual chat responses powered by RAG architecture
- API-based interface for easy integration
- Customizable prompt templates for different use cases
- Performance optimized for production environments

## Installation

```bash
# Clone the repository
git clone https://github.com/EngTnascimento/rag_chatbot.git
cd rag_chatbot

# Create environment files
# Create apps/api/.env.docker and frontend/.env.docker with appropriate values

# Set your OpenAI API key
export OPENAI_API_KEY=your_openai_api_key_here

# Build and start the services
docker-compose up -d

# To view logs
docker-compose logs -f

# To stop the services
docker-compose down
```

This will start three services:
- API backend on port 8080
- ChromaDB vector database on port 8000
- Frontend Streamlit application on port 8501

Access the frontend application by navigating to http://localhost:8501 in your browser.

## Usage

The application can be run as an API service:

```bash
# Start the API server
python -m apps.api.main
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
