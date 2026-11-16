# 🚀 AI Code Review Platform

> A production-grade, full-stack AI-powered code review platform that
> analyzes GitHub repositories and Pull Requests using a local LLM,
> provides repository-aware RAG chat, and publishes AI-generated reviews
> directly to GitHub.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Queue%2FCache-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC244C)](https://qdrant.tech/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black)](https://ollama.com/)
[![GitHub
API](https://img.shields.io/badge/GitHub-API-181717?logo=github&logoColor=white)](https://docs.github.com/en/rest)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

------------------------------------------------------------------------

## 🎯 Why This Project

Modern development teams spend significant time reviewing Pull Requests,
understanding unfamiliar repositories, and identifying bugs and security
risks.

This project explores how an AI-assisted engineering platform can
automate parts of that workflow while keeping the infrastructure
developer-friendly and locally runnable.

The platform combines:

-   Microservice-based backend architecture
-   GitHub API integration
-   Local LLM-powered code analysis
-   Retrieval-Augmented Generation (RAG)
-   Vector search
-   Async task processing
-   Structured AI review output
-   Automated GitHub Pull Request reviews
-   Modern React frontend

The goal is not just to generate text about code, but to build an
**end-to-end engineering system** around AI-assisted software
development.

------------------------------------------------------------------------

## ✨ Key Features

### 🤖 AI Code Review

Analyze source code using a locally running LLM.

The review engine produces structured feedback including:

-   Overall quality score
-   Security issues
-   Bugs and logic problems
-   Style problems
-   Maintainability concerns
-   Line-level feedback
-   Improvement suggestions

The system uses a local Ollama model rather than requiring a paid
external LLM API.

------------------------------------------------------------------------

### 🔀 GitHub Pull Request AI Review

Provide:

``` text
Repository Owner
Repository Name
Pull Request Number
```

The platform:

1.  Fetches the Pull Request from GitHub
2.  Retrieves changed files
3.  Extracts available patches
4.  Detects the programming language
5.  Sends the code to the local AI review engine
6.  Generates structured review results
7.  Publishes the review directly to GitHub
8.  Displays the results in the web application

Example flow:

``` text
GitHub Pull Request
        ↓
Changed Files
        ↓
Patch Extraction
        ↓
Local AI Review
        ↓
Structured Findings
        ↓
GitHub Review Publication
        ↓
Frontend Results
```

------------------------------------------------------------------------

### 💬 Repository Chat with RAG

Developers can ask questions about a repository using
Retrieval-Augmented Generation.

Pipeline:

``` text
Repository
    ↓
Clone
    ↓
Code Chunking
    ↓
Embeddings
    ↓
Qdrant Vector Database
    ↓
Semantic Retrieval
    ↓
Relevant Repository Context
    ↓
Local LLM
    ↓
AI Answer
```

This allows developers to ask repository-aware questions instead of
relying only on a general-purpose LLM.

------------------------------------------------------------------------

### 🔗 GitHub Webhooks

GitHub webhook events can trigger backend workflows automatically.

Supported Pull Request events include:

-   `opened`
-   `reopened`
-   `synchronize`

Webhook processing can queue asynchronous repository/PR tasks through
Celery and Redis.

------------------------------------------------------------------------

### ⚡ Asynchronous Processing

Long-running operations are designed around:

-   Celery
-   Redis
-   Background task execution

This helps separate API request handling from heavier AI and repository
workloads.

------------------------------------------------------------------------

### 🔐 Authentication

The platform includes:

-   User registration
-   User login
-   JWT-based authentication
-   Protected backend operations

------------------------------------------------------------------------

### 🗄️ Data & Infrastructure

The backend integrates with:

-   PostgreSQL
-   SQLAlchemy
-   Alembic
-   Redis
-   Qdrant
-   Ollama

------------------------------------------------------------------------

## 🏗️ System Architecture

``` text
                         ┌───────────────────────┐
                         │      React UI         │
                         │   TypeScript / Vite   │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │     API Gateway       │
                         │       FastAPI         │
                         │        :8000          │
                         └───────────┬───────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 │                   │                   │
                 ▼                   ▼                   ▼
        ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
        │ Auth Service   │  │ Repository     │  │ API / Chat     │
        │     :8001      │  │ Service :8000  │  │    Routes      │
        └────────────────┘  └───────┬────────┘  └────────────────┘
                                    │
                       ┌────────────┼─────────────┐
                       │            │             │
                       ▼            ▼             ▼
                    GitHub       Qdrant        Ollama
                     API        Vector DB        LLM

                       │
                       ▼
                  PostgreSQL

                       │
                       ▼
                    Redis
                 Celery Broker
                       │
                       ▼
                Celery Worker
              Async AI/Repo Tasks
```

------------------------------------------------------------------------

## 🧰 Technology Stack

### Frontend

-   React
-   TypeScript
-   Vite
-   Tailwind CSS
-   React Router
-   Zustand
-   TanStack React Query
-   Axios
-   Monaco Editor
-   Socket.IO

### Backend

-   Python 3.12
-   FastAPI
-   Pydantic
-   SQLAlchemy
-   Alembic
-   Uvicorn
-   JWT Authentication

### AI / RAG

-   Ollama
-   Local LLM
-   Structured AI review
-   Retrieval-Augmented Generation
-   BAAI BGE Small embeddings
-   Qdrant vector database

### Data / Infrastructure

-   PostgreSQL
-   Redis
-   Celery

### GitHub Integration

-   GitHub REST API
-   GitHub Pull Requests
-   GitHub Webhooks
-   GitHub App integration

> Docker / Docker Compose is planned as the next engineering milestone
> and is not required for the current local development workflow.

------------------------------------------------------------------------

## 📁 Project Structure

``` text
Production-Grade-Full-Stack-AI-Code-Review-Platform/
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── routes/
│   │   └── store/
│   └── package.json
│
├── gateway/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── middleware/
│   │   ├── schemas/
│   │   └── utils/
│   └── requirements.txt
│
├── services/
│   ├── auth-service/
│   │   └── app/
│   │
│   └── repository-service/
│       └── app/
│           ├── api/
│           ├── core/
│           ├── schemas/
│           ├── services/
│           └── tasks/
│
├── readme.md
└── LICENSE
```

------------------------------------------------------------------------

## 🚀 Getting Started

### Prerequisites

Install:

-   Git
-   Python 3.12+
-   Node.js 18+
-   npm
-   Docker Desktop
-   Ollama

You will also need:

-   A GitHub account
-   GitHub API credentials/configuration for GitHub integration

------------------------------------------------------------------------

## 📥 Clone the Repository

``` powershell
git clone https://github.com/soumyanh07/Full-Stack-AI-Code-Review-Platform.git
cd Full-Stack-AI-Code-Review-Platform
```

------------------------------------------------------------------------

## ⚙️ Environment Configuration

Each service uses environment variables. For Docker Compose, copy the safe template
and replace its placeholders before starting the services:

```sh
cp .env.example .env
# Edit .env and replace the database password, JWT secret, and GitHub credentials.
docker compose up --build
```

Set `ENVIRONMENT=production` only after replacing all placeholders with real
deployment values. Production startup rejects a missing, weak, or placeholder JWT
secret. The gateway and auth service receive the same `SECRET_KEY` and `ALGORITHM`
from this file.

Typical configuration includes:

``` text
DATABASE_URL
GITHUB_TOKEN
GITHUB_APP_ID
GITHUB_APP_PRIVATE_KEY_PATH
GITHUB_APP_INSTALLATION_ID
GITHUB_WEBHOOK_SECRET
OLLAMA_URL
OLLAMA_MODEL
QDRANT_HOST
QDRANT_PORT
REDIS_URL
```

### Security

Never commit:

``` text
.env
*.pem
private keys
GitHub tokens
database passwords
JWT secrets
webhook secrets
```

Use your own credentials when configuring GitHub integration.

------------------------------------------------------------------------

## 🧠 Ollama Setup

Install Ollama and download the local model configured for your
environment.

Example:

``` powershell
ollama pull phi3:mini
```

Start Ollama if it is not already running:

``` powershell
ollama serve
```

Verify:

``` powershell
ollama list
```

The repository service reads the configured model through:

``` text
OLLAMA_URL
OLLAMA_MODEL
```

> The exact model can be changed through environment configuration. This
> project is designed to work with a locally available Ollama model
> rather than a paid hosted LLM API.

------------------------------------------------------------------------

## 💻 Local Development

For development without Docker, start the services independently.

### 1. Repository Service

``` powershell
cd services\repository-service
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8002
```

### 2. Gateway

Open another PowerShell terminal:

``` powershell
cd gateway
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### 3. Auth Service

Open another PowerShell terminal:

``` powershell
cd services\auth-service
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8001
```

### 4. Celery Worker

Open another PowerShell terminal:

``` powershell
cd services\repository-service
.\.venv\Scripts\Activate.ps1
celery -A app.core.celery_app:celery_app worker --loglevel=info --pool=solo
```

### 5. Frontend

Open another PowerShell terminal:

``` powershell
cd frontend
npm install
npm run dev
```

------------------------------------------------------------------------

## 🌐 Local Service URLs

These URLs are for services started directly on the host. Docker Compose publishes
the gateway on `8000`, auth on `8001`, AI on `8002`, repository on `8003`, and
review on `8004`; the repository, AI, and review containers listen on port `8000`.
Gateway-to-service traffic uses Docker service names and container ports, including
`repository-service:8000` for repository and chat requests.

  Service              URL
  -------------------- ------------------------------
  Frontend             `http://localhost:5173`
  API Gateway          `http://localhost:8000`
  Gateway Swagger      `http://localhost:8000/docs`
  Auth Service         `http://localhost:8001`
  Repository Service   `http://localhost:8002`
  Repository Swagger   `http://localhost:8002/docs`
  Ollama               `http://localhost:11434`
  Qdrant               `http://localhost:6333`
  Redis                `localhost:6379`
  PostgreSQL           `localhost:5432`

------------------------------------------------------------------------

## 🧪 Verification

After starting the services, verify the gateway:

``` text
http://localhost:8000/docs
```

Verify the repository service:

``` text
http://localhost:8002/docs
```

Verify the frontend:

``` text
http://localhost:5173
```

A successful Pull Request review follows this flow:

``` text
Frontend
   ↓
Gateway
   ↓
Repository Service
   ↓
GitHub
   ↓
Changed PR Files
   ↓
Local Ollama Model
   ↓
Structured AI Review
   ↓
GitHub Review
   ↓
Frontend
```

------------------------------------------------------------------------

## 📊 Project Progress

  Module                          Status
  ------------------------------- -------------------------------
  API Gateway                     ✅ Complete
  Authentication / JWT            ✅ Complete
  PostgreSQL + SQLAlchemy         ✅ Complete
  Alembic                         ✅ Complete
  Repository Service              ✅ Complete
  Repository Cloning              ✅ Complete
  Code Chunking                   ✅ Complete
  Embeddings                      ✅ Complete
  Qdrant Vector Search            ✅ Complete
  Redis / Celery                  ✅ Complete
  Local Ollama LLM                ✅ Complete
  Structured AI Code Review       ✅ Complete
  Repository Chat / RAG           ✅ Complete
  GitHub API Integration          ✅ Complete
  GitHub Pull Request AI Review   ✅ Complete
  GitHub Review Publication       ✅ Complete
  GitHub Webhooks                 ✅ Complete
  Frontend                        ✅ Complete
  Full-System Integration Test    ✅ Complete
  Docker Compose                  🔄 Next Engineering Milestone
  Production Deployment           🔄 Future

------------------------------------------------------------------------

## 🧪 End-to-End Validation

The platform has been validated through a real GitHub Pull Request
workflow.

Example:

``` text
Pull Request #19
       ↓
1 changed Python file
       ↓
AI analysis
       ↓
Overall score: 2/10
       ↓
3 issues identified
       ↓
Security
Style
Maintainability
       ↓
GitHub review published
       ↓
Frontend displayed the result
```

This validates the complete application flow from the frontend through
the backend services, local AI review engine, and GitHub integration.

------------------------------------------------------------------------

## 🔒 Security Notes

For local development:

-   Keep secrets in `.env`
-   Never commit GitHub tokens
-   Never commit private keys
-   Never expose database passwords
-   Never expose webhook secrets
-   Use separate credentials for development and production

For production deployment, credentials should be managed through a
proper secrets-management system.

------------------------------------------------------------------------

## 🤝 Contributing

Contributions are welcome.

### Development Workflow

1.  Fork the repository
2.  Create a feature branch

``` powershell
git checkout -b feature/your-feature
```

3.  Make your changes
4.  Run tests and validation
5.  Commit your changes

``` powershell
git add .
git commit -m "feat: describe your change"
```

6.  Push your branch

``` powershell
git push origin feature/your-feature
```

7.  Open a Pull Request

### Before Submitting a PR

Please make sure:

-   The application still starts
-   Backend APIs are working
-   Frontend builds successfully
-   Linting passes
-   No secrets are committed
-   New functionality is documented
-   Existing functionality is not unnecessarily broken

------------------------------------------------------------------------

## 🛠️ Engineering Principles

This project focuses on:

-   Modular architecture
-   Separation of concerns
-   API-driven communication
-   Asynchronous processing
-   Structured AI outputs
-   Local-first AI experimentation
-   Secure configuration
-   Reproducible development
-   Maintainable code
-   Developer experience
-   Collaboration through GitHub workflows

------------------------------------------------------------------------

## 📌 Roadmap

Future improvements may include:

-   GitHub Checks API with GitHub App permissions
-   More advanced multi-language analysis
-   Improved review ranking
-   Team collaboration
-   Code-quality analytics
-   Automated test generation
-   AI-generated documentation
-   Production deployment
-   Kubernetes deployment
-   CI/CD pipelines
-   Improved observability
-   Multi-tenant architecture

------------------------------------------------------------------------

## 👨‍💻 Author

**Soumya**

B.Tech --- Artificial Intelligence & Machine Learning

Interested in:

-   Software Engineering
-   AI / ML
-   Backend Engineering
-   Distributed Systems
-   Developer Tools
-   AI-assisted Software Development

GitHub:

https://github.com/soumyanh07

------------------------------------------------------------------------

## ⭐ Support

If you find this project useful or interesting:

-   ⭐ Star the repository
-   🍴 Fork the project
-   🐛 Open an issue
-   💡 Suggest an improvement
-   🔀 Submit a Pull Request

Contributions and technical discussions are welcome.

------------------------------------------------------------------------

## 📄 License

This project is licensed under the MIT License.
