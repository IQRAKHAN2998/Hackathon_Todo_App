# Skills and Subagents for 5-Phase Hackathon Todo System

This document defines the reusable skills and subagents for the 5-phase Hackathon Todo system project under Spec-Kit.

## SKILLS

### SKILL 1: Spec Authoring Skill
- **Responsibility**: Convert user intent into clear, testable specs
- **Enforces**: Spec structure (scope, rules, constraints, success criteria)
- **Rejects**: Vague or implementation-level instructions
- **Output**: Markdown spec files under /specs
- **Usage**: `/sp.specify` - converts natural language to structured specs
- **Validation**: Ensures all user stories are independently testable
- **Constitution Compliance**: Verifies spec aligns with active constitution

### SKILL 2: Code Generation Skill
- **Responsibility**: Generate code strictly from approved specs
- **Must follow**: The active constitution
- **Must not introduce**: Features not defined in specs
- **Must maintain**: Clean architecture and separation of concerns
- **Usage**: `/sp.implement` - generates code from approved specs
- **Validation**: Ensures all code has corresponding spec requirements
- **Constitution Compliance**: Blocks code generation that violates constitution

### SKILL 3: Refactoring via Spec Skill
- **Responsibility**: Handle bugs or changes ONLY by modifying specs
- **Must never**: Directly patch code without a spec update
- **Ensures**: Backward compatibility with previous phases
- **Usage**: `/sp.update-spec` - updates specs to fix issues
- **Validation**: Requires spec change before code change
- **Constitution Compliance**: Enforces spec-first bug fixes

### SKILL 4: Review & Judge-Readability Skill
- **Responsibility**: Review repo structure, naming, and clarity
- **Optimize for**: Hackathon judges (clarity > cleverness)
- **Suggest improvements**: ONLY through spec updates
- **Usage**: `/sp.review` - evaluates codebase for judge-readability
- **Validation**: Checks for clean architecture and clear documentation
- **Constitution Compliance**: Ensures code clarity principles are met

## SUBAGENTS

### SUBAGENT 1: CLI Architect Agent (Phase 1)
- **Focus**: Python CLI architecture
- **Ensures**: Business logic is decoupled from input/output
- **Validates**: In-memory-only constraint
- **Usage**: `/sp.phase1` - handles Phase 1 CLI requirements
- **Constraints**: No external libraries beyond Python standard library
- **Architecture**: Separates models, services, and CLI interface

### SUBAGENT 2: Backend API Agent (Phase 2)
- **Focus**: FastAPI, REST design, JWT authentication
- **Ensures**: Secure middleware and proper request validation
- **Never mixes**: Frontend or database concerns
- **Usage**: `/sp.phase2-backend` - handles Phase 2 backend requirements
- **Constraints**: Proper REST API design with JWT authentication
- **Architecture**: API layer, service layer, model layer separation

### SUBAGENT 3: Frontend UI Agent (Phase 2)
- **Focus**: Next.js components and UX
- **Consumes APIs only**: No direct DB access
- **Ensures**: Clean, minimal, judge-friendly UI
- **Usage**: `/sp.phase2-frontend` - handles Phase 2 frontend requirements
- **Constraints**: Frontend must never access database directly
- **Architecture**: Component-based UI with proper API integration

### SUBAGENT 4: AI Agent Designer (Phase 3)
- **Focus**: AI agent + MCP tools
- **Ensures**: Agent never accesses DB directly
- **Maps**: Natural language → tool calls correctly
- **Usage**: `/sp.phase3` - handles Phase 3 AI requirements
- **Constraints**: All actions must go through MCP tools
- **Architecture**: Natural language processing → MCP tools → backend services

### SUBAGENT 5: Cloud & Kubernetes Agent (Phase 4)
- **Focus**: Docker, Helm, Minikube
- **Ensures**: Stateless services and scalability
- **Infrastructure**: Defined as configuration, not code hacks
- **Usage**: `/sp.phase4` - handles Phase 4 deployment requirements
- **Constraints**: Containerized deployment with Helm charts
- **Architecture**: Container-first design with environment variables

### SUBAGENT 6: Event-Driven Architect Agent (Phase 5)
- **Focus**: Kafka / Dapr event systems
- **Ensures**: Loose coupling and idempotent handlers
- **Designs**: System for future extensibility
- **Usage**: `/sp.phase5` - handles Phase 5 event requirements
- **Constraints**: Task operations must emit events
- **Architecture**: Event-driven design with idempotent handlers

## GLOBAL RULE FOR ALL SKILLS AND SUBAGENTS

- **Spec Compliance**: All work must be based on approved specs
- **Constitution Adherence**: All activities must follow the active constitution
- **Phase Compatibility**: Each phase must build on previous phases without breaking them
- **Judge Readability**: Code and documentation must be clear and understandable
- **Separation of Concerns**: Maintain clean architectural boundaries