SocialLens
Multimodal Social Media Content Intelligence Platform
Next.js TypeScript FastAPI Python Tailwind CSS Google Gemini Supabase PyMuPDF Tesseract

Overview
SocialLens is an AI-powered multimodal content intelligence platform that analyzes social media posts, marketing collateral, and documents to provide deterministic engagement scoring and AI-driven strategic recommendations. It helps marketers and content creators understand the hidden mechanics of their content to maximize audience engagement and conversion.

The platform combines a robust multimodal extraction engine (Native PDF, Scanned PDF, Images), deterministic rule-based engagement profiling, a specialized AI Strategist powered by Google Gemini, evidence-backed provenance tracking, and a seamless full-stack architecture into a single intelligence dashboard.

Built as a full-stack product prototype with a Next.js frontend, FastAPI backend, PyMuPDF/Tesseract extraction pipeline, and Supabase persistence.

Problem Statement
Marketers and content teams today rely on gut feeling or lagging indicators (likes, shares) to evaluate content quality. Existing platforms provide simple AI summaries, but they do not answer the critical pre-publishing question:

What specific elements of this content are helping or hurting its engagement potential, and how can it be optimized before it goes live?

Standard LLM wrappers provide generic advice without tracing their reasoning back to the source material, leading to hallucinations and unactionable feedback.

SocialLens solves this by combining deterministic rule-based analysis (Hook, CTA, Readability) with Gemini-powered generative strategy, all strictly grounded in exact bounding-box evidence from the original content.

Key Features
1. Multimodal Extraction Engine
A dynamic pipeline that automatically detects and extracts from various inputs:
Native PDFs: High-fidelity text and layout extraction using PyMuPDF.
Scanned PDFs & Images: Fallback to Tesseract OCR for text extraction.
Outputs precise `DocumentBlocks` with bounding boxes for exact provenance.

2. Dual-Layer Analysis Architecture
Layer	Purpose	Data Source
Deterministic Rules	Fast, verifiable engagement scoring	Extracted DocumentBlocks
AI Strategist	Nuanced, creative recommendations	Google Gemini 2.5 Flash

3. Engagement Profiling & Scoring
Four-metric composite scoring pipeline:
Emotion Score — Analyzes sentiment and emotional resonance.
Interaction Score — Evaluates the strength of Hooks and CTAs.
Readability Score — Measures clarity and cognitive load.
Overall Engagement Score — Normalized 0–100 composite metric.

4. Evidence Integrity & Provenance
Every recommendation and score is tied to exact evidence from the source file.
The dashboard traces recommendations back to specific `block_id`s, pages, and bounding boxes, ensuring zero hallucinated claims.

5. AI Strategist (Ask Gemini)
Gemini 2.5 Flash integration acting as a specialized content strategist.
Strict Critic Agent guardrails: A secondary pipeline step validates Gemini's output to ensure it doesn't invent facts or contradict the deterministic rules.
Fallback mechanism: If Gemini is unavailable or rate-limited, the system gracefully degrades to rule-based recommendations.

6. Security & Enterprise Readiness
Strict file size limits and MIME-type validation.
Complete isolation of environment variables—no secrets leak to the frontend.
Local-first processing capabilities for E2E verification.

System Architecture
SocialLens: Content Intelligence Platform
│
├── frontend/
│   ├── Next.js App Router
│   ├── TypeScript
│   ├── Tailwind CSS + shadcn/ui
│   ├── Interactive Score Breakdowns
│   └── File Upload & Validation
│
├── backend/
│   ├── FastAPI + Uvicorn
│   ├── Multimodal Extraction (PyMuPDF / Tesseract)
│   ├── Deterministic Rule Engine
│   ├── Critic Agent Validation
│   ├── Gemini AI Integration
│   └── Pytest E2E Suite
│
└── supabase/
    └── PostgreSQL persistence (Documents, Blocks, Profiles, Scores)

Tech Stack
Layer	Technology
Frontend	Next.js, React 19, TypeScript
UI	Tailwind CSS, shadcn/ui, Lucide Icons
Backend	FastAPI, Python 3.11
Extraction	PyMuPDF (fitz), Tesseract OCR
AI Layer	Google Gemini 2.5 Flash
Database	Supabase (PostgreSQL)
Testing	Pytest

Project Structure
SocialLens/
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js Routes
│   │   ├── components/       # UI (ScoreBreakdown, Recommendations, etc.)
│   │   └── lib/              # API clients & utilities
│   ├── package.json
│   └── .env.local
│
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI endpoints
│   │   ├── extraction/       # PDF/Image processors
│   │   ├── profiling/        # Engagement scoring
│   │   ├── agents/           # Gemini & Critic agents
│   │   └── db/               # Supabase session management
│   ├── tests/                # Pytest E2E fixtures and suites
│   ├── requirements.txt
│   └── .env
│
├── .gitignore
└── README.md

Getting Started

Prerequisites
Node.js 18+
Python 3.11+
Tesseract OCR installed locally
Google Gemini API key
Supabase URL and Key

Environment Variables
Backend (backend/.env):
DATABASE_URL=your_db_url
SUPABASE_URL=your_supabase_url
SUPABASE_PUBLISHABLE_KEY=your_key
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.5-flash
FRONTEND_URL=http://localhost:3000
MAX_FILE_SIZE_MB=10

Frontend Setup
cd frontend
npm install
npm run dev

Backend Setup
cd backend
conda create -n sociallens python=3.11
conda activate sociallens
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

Demo Flow
Upload → The user uploads a Native PDF, Scanned PDF, or Image.
Extraction → The backend routes it to PyMuPDF or Tesseract, returning DocumentBlocks.
Profiling → Rule-based engines compute Engagement, Readability, and Emotion scores.
AI Strategy → Gemini generates targeted recommendations, filtered by the Critic agent.
Dashboard → The frontend reconstructs the analysis with interactive evidence tracing.

Why This Project Matters
SocialLens transforms subjective content creation into a verifiable, data-driven process. 
By combining deterministic rules with generative AI and strict provenance tracking, it provides actionable insights without the hallucinations typical of basic LLM wrappers.

Author
Sparsh Taparia

GitHub: @Sparshtaparia
Email: sparshtaparia2005@gmail.com

License
This project is maintained as a prototype.
