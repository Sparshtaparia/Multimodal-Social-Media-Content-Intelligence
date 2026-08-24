# SocialLens

### Multimodal Social Media Content Intelligence Platform

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-181717?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini%20AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

</div>

---

## Overview

**SocialLens** is an AI-powered multimodal content intelligence platform that analyzes social media posts, marketing collateral, and documents to provide deterministic engagement scoring and AI-driven strategic recommendations. It helps marketers and content creators understand the hidden mechanics of their content to maximize audience engagement and conversion.

The platform combines a **robust multimodal extraction engine** (Native PDF, Scanned PDF, Images), **deterministic rule-based engagement profiling**, a specialized **AI Strategist powered by Google Gemini**, **evidence-backed provenance tracking**, and a **seamless full-stack architecture** into a single intelligence dashboard.

Built as a full-stack product prototype with a **Next.js frontend**, **FastAPI backend**, **PyMuPDF/Tesseract extraction pipeline**, and **Supabase persistence**.

---

## Problem Statement

Marketers and content teams today rely on gut feeling or lagging indicators (likes, shares) to evaluate content quality. Existing platforms provide simple AI summaries, but they do not answer the critical pre-publishing question:

**What specific elements of this content are helping or hurting its engagement potential, and how can it be optimized before it goes live?**

Standard LLM wrappers provide generic advice without tracing their reasoning back to the source material, leading to hallucinations and unactionable feedback.

SocialLens solves this by combining deterministic rule-based analysis (Hook, CTA, Readability) with Gemini-powered generative strategy, all strictly grounded in exact bounding-box evidence from the original content.

---

## Key Features

### 1. Multimodal Extraction Engine

A dynamic pipeline that automatically detects and extracts from various inputs:
1. **Native PDFs:** High-fidelity text and layout extraction using PyMuPDF.
2. **Scanned PDFs & Images:** Fallback to Tesseract OCR for text extraction.
3. **Outputs:** Precise `DocumentBlocks` with bounding boxes for exact provenance.

### 2. Dual-Layer Analysis Architecture

| Layer | Purpose | Data Source |
|-------|---------|-------------|
| **Deterministic Rules** | Fast, verifiable engagement scoring | Extracted DocumentBlocks |
| **AI Strategist** | Nuanced, creative recommendations | Google Gemini 2.5 Flash |

### 3. Engagement Profiling & Scoring

Four-metric composite scoring pipeline:

| Metric | Analysis Focus | Impact |
|--------|---------------|--------|
| **Emotion Score** | Sentiment and emotional resonance | Drives sharing and virality |
| **Interaction Score** | Strength of Hooks and CTAs | Drives clicks and conversions |
| **Readability Score** | Clarity and cognitive load | Drives completion rate |
| **Overall Score** | Normalized 0–100 composite | Baseline quality metric |

### 4. Evidence Integrity & Provenance

Every recommendation and score is tied to exact evidence from the source file. The dashboard traces recommendations back to specific `block_id`s, pages, and bounding boxes, ensuring zero hallucinated claims.

### 5. AI Strategist (Ask Gemini)

- Gemini 2.5 Flash integration acting as a specialized content strategist.
- **Strict Critic Agent guardrails:** A secondary pipeline step validates Gemini's output to ensure it doesn't invent facts or contradict the deterministic rules.
- **Fallback mechanism:** If Gemini is unavailable or rate-limited, the system gracefully degrades to rule-based recommendations.

### 6. Security & Enterprise Readiness

- Strict file size limits and MIME-type validation.
- Complete isolation of environment variables—no secrets leak to the frontend.
- Local-first processing capabilities for E2E verification.

---

## System Architecture

```txt
SocialLens: Content Intelligence Platform
│
├── frontend/
│   ├── Next.js App Router (16)
│   ├── TypeScript
│   ├── Tailwind CSS + shadcn/ui
│   ├── Framer Motion animations
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
```

---

## Enterprise SaaS Architecture (Beyond Serverless MVP)

The current MVP is designed for rapid deployment. However, for a true Enterprise SaaS production environment, SocialLens shifts to a distributed Event-Driven Architecture:

1. **Object Storage (AWS S3 / GCP Cloud Storage):** Instead of uploading large PDFs and Images to the backend server directly, the frontend uploads securely to S3 via pre-signed URLs.
2. **Event-Driven Processing (Apache Kafka / AWS SQS):** Once the file hits S3, an event is triggered to a message queue, decoupling the upload from the heavy OCR and NLP analysis.
3. **Asynchronous Worker Nodes (Celery + AWS ECS / EKS):** Dedicated, long-running Python worker containers pull tasks from the queue, download the media from S3, run the heavy Tesseract/PyMuPDF extraction, and update a progress state via WebSocket.
4. **Persistent Database (PostgreSQL / TimescaleDB):** Analyzed document blocks, sentiment profiles, and scoring metrics are stored in a relational database optimized for text and analytics.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, TypeScript |
| UI | Tailwind CSS, shadcn/ui, Lucide Icons, Framer Motion |
| Backend | FastAPI, Uvicorn, Python 3.11 |
| Extraction Engine | PyMuPDF (fitz), Tesseract OCR |
| AI Layer | Google Gemini 2.5 Flash |
| Database | Supabase (PostgreSQL) |
| Testing | Pytest |

---

## Project Structure

```txt
SocialLens/
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js Routes
│   │   ├── components/       # UI (ScoreBreakdown, Recommendations, etc.)
│   │   └── lib/              # API clients & utilities
│   ├── next.config.ts
│   ├── package.json
│   └── .env.local
│
├── backend/
│   ├── main.py               # FastAPI entry point
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
```

---

## Getting Started

### Prerequisites

```txt
Node.js 18+
Python 3.11+
Git
Tesseract OCR installed locally
Google Gemini API key
Supabase URL and Key
```

---

## Environment Variables

Create `frontend/.env.local` and `backend/.env` using the examples as reference:

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (`backend/.env`)

```env
DATABASE_URL=your_db_url
SUPABASE_URL=your_supabase_url
SUPABASE_PUBLISHABLE_KEY=your_key
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.5-flash
FRONTEND_URL=http://localhost:3000
MAX_FILE_SIZE_MB=10
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at:

```txt
http://localhost:3000
```

---

## Backend Setup

```bash
cd backend
conda create -n sociallens python=3.11
```

### Activate Conda Env

```bash
conda activate sociallens
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend runs at:

```txt
http://localhost:8000
```

---

## Production Deployment

### 1. Backend (Railway)
The backend is designed to be deployed on **Railway** (or Render) due to the need for persistent memory for heavy PDF extraction and OCR processes.
1. Connect your GitHub repository to a new Railway project.
2. In the Service Settings, set the **Root Directory** to `/backend`.
3. Go to the **Variables** tab for your backend service in Railway and paste all the Backend environment variables. Click **Deploy Changes**.

### 2. Frontend (Vercel)
1. Import your GitHub repository to Vercel.
2. Set the **Framework Preset** to Next.js.
3. Set the **Root Directory** to `frontend`.
4. Add the Frontend environment variables. **Crucially**, ensure your API URL is set to the full HTTPS URL of your Railway backend.
5. Deploy.

---

## Demo Flow

```txt
Landing Page
  → Upload a Social Media Post (Native PDF, Scanned PDF, Image)

Extraction Mode:
  → System detects file type (PDF vs Image)
    → PyMuPDF or Tesseract OCR extracts text and layout data
      → DocumentBlocks are generated with precise bounding boxes

Profiling & Strategy:
  → Rule-based engines compute Engagement, Readability, and Emotion scores
    → Gemini generates targeted recommendations
      → Critic Agent filters and maps recommendations to exact evidence
        → Dashboard opens with interactive Score Breakdowns and AI Strategist insights
```

---

## Core Modules

### Multimodal Extraction Engine
Automatically switches between PyMuPDF (fast, high-fidelity) and Tesseract OCR depending on whether the document is digitally native or scanned.

### Score Breakdown Dashboard
Visualizes engagement components (Hook, CTA, Emotion) with interactive evidence tracing that highlights exact sections of the original document.

### Ask Gemini (AI Strategist)
Generates high-level content strategy and rewriting suggestions based on extracted data, while strictly adhering to provenance guidelines.

### Critic Agent
Acts as an automated auditor for the AI Strategist. Rejects any AI-generated recommendations that hallucinate facts or fail to map back to actual DocumentBlocks.

---

## Example Use Cases

- Pre-publishing social media post optimization
- Marketing collateral engagement audits
- A/B testing hook and CTA variations
- Verifiable AI-assisted content strategy

---

## Why This Project Matters

SocialLens transforms subjective content creation into a verifiable, data-driven process. 

The project brings together:

- **Research novelty** through deterministic scoring of subjective metrics (Hooks, CTA).
- **Product thinking** through visual evidence mapping and provenance tracking.
- **Full-stack engineering** through Next.js, FastAPI, and Supabase integration.
- **AI integration** through a Gemini-powered Strategist paired with a strict Critic Agent.

**Standard LLM wrappers hallucinate generic advice. SocialLens provides strategic intelligence grounded in mathematical evidence.**

---

## Current Status

Working product prototype built for architecture validation and automated E2E testing.

**Implemented:**
- Full Multimodal Extraction (Native PDF, Scanned PDF, Images)
- Deterministic Profiling and Scoring 
- Critic Agent & Gemini Integration
- Evidence Provenance Tracking
- Next.js UI with Interactive Dashboards
- Pytest E2E Test Suite (21/21 Passing)
- Complete GitHub Actions / Deployment Readiness

---

## Author

**Sparsh Taparia**

- GitHub: [@Sparshtaparia](https://github.com/Sparshtaparia)
- Email: [sparshtaparia2005@gmail.com](mailto:sparshtaparia2005@gmail.com)

---

## License

This project is maintained as a prototype.

---

## Acknowledgement

Built to bring intelligence and verifiable provenance to social media marketing and content strategy.

**SocialLens: Know your engagement potential before you hit publish.**
