# ResearchMate Formatter & Tagger

ResearchMate is an AI-powered tool that helps researchers format and tag their academic paper drafts. It automates section detection, keyword suggestion, and applies journal-standard formatting (IEEE/ACM style base).

## Features
- **Drag-and-Drop Upload**: Easy interface for `.docx` files.
- **AI Analysis**: Powered by Google Gemini, it suggests titles, keywords, and identifies formatting/referencing issues.
- **Auto-Formatting**: Rebuilds your document with consistent fonts (Times New Roman), headings, and layout.
- **Reference Checks**: Flags missing citations or format errors.

## Directory Structure (Refactored)
- `backend/`
    - `app/core`: Configuration (Env vars).
    - `app/services`: Logic for AI & Docx processing.
    - `app/routers`: API endpoints.
    - `app/schemas`: Pydantic models (implied).
    - `main.py`: Entry point.
- `frontend/`
    - `src/services`: API abstraction.
    - `src/components`: UI Components.

## Prerequisites
- Python 3.9+
- Node.js 16+
- Google Gemini API Key

## Getting Started

### 1. Backend Setup
Navigate to the `backend` folder:
```bash
cd backend
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
.\venv\Scripts\activate # Windows
# source venv/bin/activate # Mac/Linux

pip install -r requirements.txt
```

Rename `.env.example` to `.env` and add your API Key:
```bash
GEMINI_API_KEY=your_key
```

Run the server:
```bash
uvicorn main:app --reload
```
The backend will be available at `http://localhost:8000`.

### 2. Frontend Setup
Open a new terminal and navigate to the `frontend` folder:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the development server:
```bash
npm run dev
```
The frontend will be available at `http://localhost:5173`.
