# World Multi-Agent System for Healthcare

A production-grade, worldwide multi-agent AI system for healthcare — built on CrewAI, LangChain, FHIR R4, and Epic EHR integrations.

## Architecture Overview

```
┌────────────────────────────────────────────────────┐
│                 Coordinator Agent                   │
│           (Master Orchestrator / CrewAI)            │
└────────┬──────────┬──────────┬───────────┬──────────┘
         │          │          │           │
  Triage Agent  Clinical   Compliance   EHR Agent
               Agent       Agent      (Epic/FHIR)
```

## Agents

| Agent | Role |
|---|---|
| `coordinator_agent` | Master orchestrator — routes tasks across all agents |
| `triage_agent` | Intake, severity scoring, routing |
| `clinical_agent` | Clinical decision support, protocol lookup |
| `compliance_agent` | HIPAA, CMS, regulatory checks |
| `ehr_agent` | Read/write to Epic EHR via FHIR R4 |

## Tech Stack

- **Orchestration**: CrewAI + LangChain
- **LLM**: OpenAI GPT-4o (configurable)
- **EHR Integration**: Epic FHIR R4 API
- **Memory**: Shared in-memory context layer (Redis-ready)
- **Config**: Pydantic Settings + `.env`

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/jsfaulkner86/world-multi-agent-system-for-healthcare.git
cd world-multi-agent-system-for-healthcare

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run the system
python main.py
```

## Project Structure

```
world-multi-agent-system-for-healthcare/
├── main.py                  # Entry point
├── agents/                  # Agent definitions
├── tools/                   # Agent tools (FHIR, EHR, analytics)
├── memory/                  # Shared memory layer
├── config/                  # System configuration
└── tests/                   # Unit tests
```

## Author

**John Faulkner** — Agentic AI Architect | The Faulkner Group  
[thefaulknergroupadvisors.com](https://thefaulknergroupadvisors.com)
