# 🤖 Simple Groq App

A modern, production-ready full-stack application showcasing AI integration with FastAPI and Streamlit. Features a powerful backend API with Groq language models and an intuitive chat interface, all containerized with Docker.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-purple.svg)](https://github.com/astral-sh/uv)

## ✨ Features

🚀 **FastAPI Backend** - High-performance API with automatic OpenAPI documentation  
🤖 **Groq AI Integration** - Powerful language model capabilities with multiple model support  
💬 **Streamlit Frontend** - Interactive and responsive chat interface  
🐳 **Docker Support** - Fully containerized with optimized UV package management  
⚡ **UV Package Manager** - 10-100x faster dependency resolution than pip  
🔧 **Production Ready** - Comprehensive error handling, logging, and configuration management  
📚 **Educational Design** - Clean architecture demonstrating full-stack development patterns  

## 🎯 Live Demo

- **Frontend Chat Interface**: http://localhost:8501
- **Interactive API Documentation**: http://localhost:8000/docs  
- **Health Check**: http://localhost:8000/health

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (recommended: 3.10.17)
- **UV Package Manager** - [Installation Guide](https://github.com/astral-sh/uv#installation)
- **Docker & Docker Compose** - [Get Docker](https://docs.docker.com/get-docker/)
- **Groq API Key** - [Get one free here](https://console.groq.com/)

## 🚀 Quick Start

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/your-username/simple-groq-app.git
cd simple-groq-app

# Copy environment template
cp env.example .env
```

### 2️⃣ Configure Environment

Edit `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
APP_NAME=Simple Groq App
DEBUG=True
```

### 3️⃣ Choose Your Development Method

## 🐳 Method 1: Docker (Recommended)

**Fastest and most reliable way to run the application:**

```bash
# Start both backend and frontend
docker-compose up --build

# Or run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services  
docker-compose down
```

**Access your application:**
- 💬 **Chat Interface**: http://localhost:8501
- 📡 **Backend API**: http://localhost:8000
- 📖 **API Docs**: http://localhost:8000/docs

## 💻 Method 2: Local Development with UV

**For development and debugging:**

```bash
# Install dependencies (super fast with UV!)
uv sync

# Option A: Use the integrated runner
uv run python run_local.py

# Option B: Run services separately
# Terminal 1 - Backend
uv run python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend  
uv run streamlit run frontend/app.py --server.port 8501
```

## 🏗️ Architecture Overview

This project demonstrates clean architecture principles:

```
📁 Project Structure
├── 🔧 backend/                 # FastAPI Backend
│   ├── 📋 models/             # Pydantic data models  
│   ├── ⚙️ services/           # Business logic layer
│   ├── 🛠️ utils/              # Configuration & utilities
│   └── 🚪 main.py             # FastAPI application entry
├── 🎨 frontend/               # Streamlit Frontend  
│   ├── 🧩 components/         # Reusable UI components
│   └── 📱 app.py              # Main application
├── 🐳 Dockerfile             # Container definition
├── 🔧 docker-compose.yml     # Multi-service orchestration
├── 📦 pyproject.toml          # UV project configuration
├── 🔒 uv.lock                # Dependency lock file
└── 📖 README.md              # You are here!
```

## 🔗 API Documentation

The FastAPI backend provides comprehensive API documentation:

### Available Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/` | GET | Root endpoint | Basic app info |
| `/health` | GET | Health check | Service status |
| `/models` | GET | Available models | List Groq models |
| `/chat` | POST | Chat completion | Send message, get AI response |

### 💬 Chat API Example

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum computing in simple terms",
    "model": "llama-3.1-8b-instant", 
    "max_tokens": 1000,
    "temperature": 0.7
  }'
```

### 📱 Frontend Features

The Streamlit interface provides:

- **🎛️ Model Selection** - Choose from available Groq models
- **⚙️ Parameter Controls** - Adjust temperature and max tokens  
- **💾 Chat History** - Persistent conversation memory
- **📊 Real-time Status** - Backend connection monitoring
- **🎨 Modern UI** - Clean, responsive design

## ⚡ Why UV Package Manager?

This project uses [UV](https://github.com/astral-sh/uv) for superior Python package management:

### 🏆 Performance Benefits:
- **⚡ 10-100x faster** than pip for dependency resolution
- **🔒 Reproducible builds** with `uv.lock` 
- **📦 Smaller Docker images** with efficient caching
- **🚀 Faster CI/CD** with optimized dependency handling

### 🐳 Docker Optimizations:
```dockerfile
# UV cache mount for lightning-fast rebuilds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --compile-bytecode --no-dev
```

## 🧪 Testing Your Setup

### ✅ Quick Health Checks

```bash
# Test backend health
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'

# Frontend test: Open http://localhost:8501 and send a message
```

### 🔧 Troubleshooting

<details>
<summary>🚨 Common Issues & Solutions</summary>

**Port Already in Use:**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different ports in docker-compose.yml
```

**Groq API Key Issues:**
```bash
# Verify your API key is set
echo $GROQ_API_KEY

# Check if key has credits at https://console.groq.com/
```

**Docker Build Problems:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

**UV/Python Issues:**
```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reset virtual environment
rm -rf .venv && uv sync
```

</details>

## 🎓 Educational Value

This project demonstrates key software engineering concepts:

### 🏛️ **Architecture Patterns**
- **Clean Architecture** - Separation of concerns across layers
- **Dependency Injection** - Configuration and service management
- **Service Layer Pattern** - Business logic encapsulation
- **Component-Based UI** - Reusable frontend components

### 🔧 **Development Practices**  
- **Type Safety** - Pydantic models and Python type hints
- **API-First Design** - OpenAPI/Swagger documentation
- **Containerization** - Docker best practices
- **Modern Tooling** - UV package management

### 📊 **Production Readiness**
- **Error Handling** - Comprehensive exception management
- **Logging** - Structured application logging
- **Health Checks** - Service monitoring endpoints  
- **Environment Configuration** - 12-factor app principles

## 🚀 Deployment Options

### 🌊 Heroku (Simplest)
```bash
heroku create your-app-name
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

### ☁️ AWS (Recommended for Production)
- **AWS App Runner** - Containerized deployment
- **AWS ECS** - Full orchestration
- **AWS Lambda** - Serverless architecture

### 🔧 Manual Server
```bash
# Production Docker run
docker run -d \
  -p 80:8000 \
  -e GROQ_API_KEY=your_key \
  -e DEBUG=False \
  your-app:latest
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### 🔄 Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Groq](https://groq.com/)** - Lightning-fast AI inference
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework  
- **[Streamlit](https://streamlit.io/)** - Beautiful data apps
- **[UV](https://github.com/astral-sh/uv)** - Next-generation Python packaging

## 📞 Support & Community

- 🐛 **Bug Reports**: [Open an issue](https://github.com/your-username/simple-groq-app/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/your-username/simple-groq-app/discussions)
- 📧 **Contact**: [your-email@example.com](mailto:your-email@example.com)

---

<div align="center">

**⭐ Star this repo if you found it helpful! ⭐**

Built with ❤️ by developers, for developers

</div>
