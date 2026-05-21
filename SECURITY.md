# Security Policy

> **Project:** W.O.R.L.D. — Multi-Agent System for Healthcare  
> **Maintainer:** The Faulkner Group  
> **Effective Date:** 2026-05-20  
> **Scope:** All code, agent definitions, memory layer implementations, tool integrations, orchestration configs, and healthcare workflow modules in this repository.

---

## ⚠️ Healthcare & PHI Notice

This project orchestrates **multiple AI agents across clinical healthcare workflows** in women's health environments. The multi-agent architecture — including agent memory layers, tool integrations, and inter-agent communication channels — may process, route, or temporarily hold PHI at multiple points in the pipeline.

- **Do not include real patient data, PHI, or PII in any issue, pull request, commit, or bug report.**
- All reproduction steps, agent traces, memory snapshots, and tool call payloads in vulnerability reports must use **fully synthetic or de-identified data**.
- Any vulnerability that allows PHI to be exposed, persisted improperly, or routed to an unauthorized agent or tool is automatically **Critical severity** and triggers HIPAA breach assessment.

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| `main` branch (latest) | ✅ Active |
| Tagged releases (`v1.x`) | ✅ Patch support for 12 months post-release |
| All prior versions | ❌ No longer supported |

---

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

### Preferred Channel

Use **GitHub's private Security Advisory** feature:

1. Navigate to the [Security tab](https://github.com/jsfaulkner86/world-multi-agent-system-for-healthcare/security/advisories/new).
2. Click **"Report a vulnerability"**.
3. Complete the advisory form using the template below.

### Backup Channel

```
security@thefaulknergroupadvisors.com
```

Encrypt sensitive disclosures with the maintainer's GPG key (published at `https://thefaulknergroupadvisors.com/.well-known/security.txt`).

---

## Response SLA

| Severity | Initial Acknowledgment | Triage Complete | Target Patch |
|----------|----------------------|-----------------|--------------|
| Critical (CVSS ≥ 9.0 or PHI exposure) | 24 hours | 48 hours | 7 days |
| High (CVSS 7.0–8.9) | 48 hours | 5 business days | 30 days |
| Medium (CVSS 4.0–6.9) | 5 business days | 10 business days | 60 days |
| Low (CVSS < 4.0) | 10 business days | 20 business days | Next release cycle |

**Any vulnerability with a PHI exposure path is automatically Critical**, regardless of CVSS score.

---

## Vulnerability Report Template

```
### Summary
[One-paragraph description of the vulnerability]

### Affected Component
[ ] Agent definition (agents/)     [ ] Memory layer (memory/)
[ ] Tool integration (tools/)       [ ] Orchestration config (config/)
[ ] Inter-agent communication       [ ] Healthcare workflow module
[ ] Dependency (name + CVE)

### Severity Estimate
CVSS Score (if known): ___
PHI Exposure Risk: [ ] Yes  [ ] No  [ ] Unknown
Agent Privilege Escalation Risk: [ ] Yes  [ ] No  [ ] Unknown

### Steps to Reproduce
1.
2.
3.

### Proof of Concept
[Code snippet, agent trace, or description — synthetic data only, no real PHI]

### Suggested Fix (optional)

### Environment
- Python version:
- LLM provider(s) and models:
- Orchestration framework (LangGraph / CrewAI / other):
- Deployment context (local / staging / production):
- Dependency snapshot (requirements.txt):
```

---

## Scope

### In Scope

- **Agent privilege escalation** — mechanisms that allow a lower-trust agent to assume capabilities or data access of a higher-trust clinical agent
- **Memory layer PHI leakage** — patient context persisting in episodic, semantic, or scratchpad memory beyond its authorized retention window
- **Tool access control bypass** — agents invoking tools (EHR, FHIR, external APIs) outside their authorized scope
- **Inter-agent prompt injection** — malicious content in one agent's output that hijacks the behavior of a downstream agent in the pipeline
- **Credential/secret exposure** — LLM API keys, EHR credentials, or integration tokens leaked in logs, agent traces, or memory snapshots
- **Orchestration logic manipulation** — inputs that subvert the intended agent routing, task decomposition, or handoff sequence
- **Config injection** — malformed `config/` files that alter agent permissions, tool access, or memory retention policies at runtime
- **Dependency CVEs** with exploitable attack surfaces in the multi-agent orchestration context

### Out of Scope

- Inherent hallucination or reasoning errors in upstream LLMs — report to the respective LLM provider
- Vulnerabilities in LLM provider infrastructure (OpenAI, Anthropic, etc.)
- Social engineering attacks against The Faulkner Group staff
- Theoretical vulnerabilities without a realistic attack path
- Issues in forked or derivative works not maintained by this repository

---

## Security Design Principles

Reports demonstrating a violation of these invariants are treated as high priority:

1. **Agent least-privilege** — each agent is scoped to the minimum tools, memory access, and data context required for its defined role; no agent inherits capabilities from peer agents.
2. **Memory isolation by agent role** — clinical agents (e.g., risk assessment, triage) operate in isolated memory contexts; cross-agent memory sharing requires explicit configuration and audit logging.
3. **No PHI in inter-agent messages by default** — patient identifiers are tokenized before entering any agent-to-agent communication channel.
4. **Audit trail on all clinical tool calls** — every tool invocation in a clinical workflow is logged with agent ID, tool name, input hash, output hash, and timestamp.
5. **Human-in-the-loop for high-stakes actions** — any agent action that could result in a clinical recommendation, EHR write, or patient notification requires explicit human approval in production.
6. **Deterministic orchestration fallback** — if the orchestrator cannot resolve an agent routing decision within defined constraints, it must escalate to a human operator, never default to an unconstrained action.

---

## Coordinated Disclosure Policy

- The Faulkner Group follows a **90-day coordinated disclosure** window from initial report to public advisory.
- Agent privilege escalation or inter-agent prompt injection vulnerabilities in clinical contexts may warrant accelerated timelines given patient safety implications.
- Reporters who follow this policy in good faith will be credited (with consent) and are protected from legal action related to good-faith research.

---

## Dependency & Supply Chain Security

- Dependencies are pinned in `requirements.txt`.
- Maintainers run `pip-audit` and `safety check` before every release tag.
- GitHub Dependabot alerts are enabled.
- New dependencies require documented rationale in the PR description.

---

## Secret Scanning & CI Enforcement

- GitHub Secret Scanning is enabled on this repository.
- `.env` files are gitignored; `.env.example` is the only committed config template.
- Any committed secret (even in a branch) must be rotated immediately.
- Pre-commit hooks enforce `detect-secrets` scanning before remote push.

---

## Contact

| Role | Contact |
|------|---------|
| Security Disclosure | security@thefaulknergroupadvisors.com |
| General Maintainer | John Faulkner — github.com/jsfaulkner86 |
| Organization | [The Faulkner Group](https://thefaulknergroupadvisors.com) |

---

*This policy is reviewed quarterly and updated with each major release. Last reviewed: 2026-05-20.*
