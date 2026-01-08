---
id: 2
title: define-skills-and-subagents
stage: general
date: 2026-01-05
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.skills
labels: [skills, architecture, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/skills/skills-and-subagents.md
tests:
 -
---

## Prompt

```
Define reusable SKILLS and SUBAGENTS for this project under Spec-Kit.

The goal is to modularize responsibilities so that future phases can reuse them
without rewriting logic or specs.

Create the following SKILLS:

SKILL 1: Spec Authoring Skill
- Responsibility: Convert user intent into clear, testable specs
- Enforces spec structure (scope, rules, constraints, success criteria)
- Rejects vague or implementation-level instructions
- Output: Markdown spec files under /specs

SKILL 2: Code Generation Skill
- Responsibility: Generate code strictly from approved specs
- Must follow the active constitution
- Must not introduce features not defined in specs
- Must maintain clean architecture and separation of concerns

SKILL 3: Refactoring via Spec Skill
- Responsibility: Handle bugs or changes ONLY by modifying specs
- Must never directly patch code without a spec update
- Ensures backward compatibility with previous phases

SKILL 4: Review & Judge-Readability Skill
- Responsibility: Review repo structure, naming, and clarity
- Optimize for hackathon judges (clarity > cleverness)
- Suggest improvements ONLY through spec updates

---

Create the following SUBAGENTS:

SUBAGENT 1: CLI Architect Agent (Phase 1)
- Focus: Python CLI architecture
- Ensures business logic is decoupled from input/output
- Validates in-memory-only constraint

SUBAGENT 2: Backend API Agent (Phase 2)
- Focus: FastAPI, REST design, JWT authentication
- Ensures secure middleware and proper request validation
- Never mixes frontend or database concerns

SUBAGENT 3: Frontend UI Agent (Phase 2)
- Focus: Next.js components and UX
- Consumes APIs only (no direct DB access)
- Ensures clean, minimal, judge-friendly UI

SUBAGENT 4: AI Agent Designer (Phase 3)
- Focus: AI agent + MCP tools
- Ensures agent never accesses DB directly
- Maps natural language → tool calls correctly

SUBAGENT 5: Cloud & Kubernetes Agent (Phase 4)
- Focus: Docker, Helm, Minikube
- Ensures stateless services and scalability
- Infrastructure defined as configuration, not code hacks

SUBAGENT 6: Event-Driven Architect Agent (Phase 5)
- Focus: Kafka / Dapr event systems
- Ensures loose coupling and idempotent handlers
- Designs system for future extensibility

GLOBAL RULE FOR ALL SKILLS AND SUBAGENTS:

- MUST follow the active constitution
- MUST build on previous phases without breaking them
- MUST prioritize judge readability and clarity
- MUST maintain separation of concerns
- MUST be based on approved specs
```

## Response snapshot

I have successfully created a comprehensive skills and subagents definition for the 5-phase Hackathon Todo system. The definition is stored in `.specify/skills/skills-and-subagents.md` and includes:

- 4 core skills: Spec Authoring, Code Generation, Refactoring via Spec, and Review & Judge-Readability
- 6 subagents for each phase: CLI Architect, Backend API, Frontend UI, AI Agent Designer, Cloud & Kubernetes, and Event-Driven Architect
- A global rule set that applies to all skills and subagents

Each skill and subagent has clearly defined responsibilities, constraints, and usage patterns that align with the project's constitution and phase requirements.

## Outcome

- ✅ Impact: Comprehensive skills and subagents architecture defined
- 🧪 Tests: No tests required for architecture definition
- 📁 Files: Created .specify/skills/skills-and-subagents.md with complete definition
- 🔁 Next prompts: Ready to implement specific skills based on this architecture
- 🧠 Reflection: Clear separation of concerns established for all project phases

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A