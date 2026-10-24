# AML Alert Triage — Multi-Agent (Semantic Kernel · AutoGen · Microsoft Agent Framework)

The same 3-agent sanctions-alert triage use case built three ways:
**Screener** (fetch hit) → **Investigator** (KYC + policy evidence) → **Decision** (close/escalate with policy citation).

| Day | Framework | File | Key idea |
|---|---|---|---|
| 1 | Semantic Kernel 1.x | `day1_semantic_kernel/sk_triage.py` | Plugins + auto function calling |
| 2 | AutoGen agentchat 0.7 | `day2_autogen/autogen_triage.py` | Multi-agent group chat, LLM speaker selection |
| 3 | Microsoft Agent Framework 1.x | `day3_agent_framework/maf_triage.py` | Unified successor; agents + workflow orchestration |

## Setup
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                     # fill Azure OpenAI values
python -m day1_semantic_kernel.sk_triage
python -m day2_autogen.autogen_triage
python -m day3_agent_framework.maf_triage
```
Expected: ALT-1001 → close as false positive (POL-02); ALT-1002 → escalate (POL-01, POL-03).

---
## Day 1 — Semantic Kernel (study 1.5h, build 1.5h)
- **Kernel**: DI container holding AI services (chat, embeddings), plugins, filters.
- **Plugin**: class of functions; `@kernel_function` exposes a method to the LLM (schema from type hints + description).
- **Function calling**: `FunctionChoiceBehavior.Auto()` — model decides which plugin to call; SK executes and loops.
- **Filters**: function-invocation / prompt-render filters = hooks for guardrails, PII masking, audit logging.
- **Agents**: `ChatCompletionAgent`, `AzureAIAgent`; `AgentThread` holds conversation state.
- **Memory**: vector-store connectors (Azure AI Search, Qdrant, Redis…) for RAG.
- **Languages**: C#, Python, **Java** (your bridge).

**Exercise:** add a `FunctionInvocationFilter` that logs every tool call (audit trail).

**Quiz:** 1) What does a plugin contain? 2) Who executes the function — model or SK? 3) Where would you mask PII? 4) What holds conversation state for an agent? 5) Name two vector stores SK supports.

## Day 2 — AutoGen (study 1.5h, build 1.5h)
- **Layers**: `autogen-core` (event-driven actor runtime), `autogen-agentchat` (high-level), `autogen-ext` (model clients, tools, code exec).
- **AssistantAgent**: LLM agent with tools, system message, `description` (used by selector).
- **Teams**: `RoundRobinGroupChat` (fixed order), `SelectorGroupChat` (LLM picks next speaker), `Swarm` (handoffs), `MagenticOneGroupChat` (orchestrator plans).
- **Termination**: `TextMentionTermination`, `MaxMessageTermination`, combine with `|` / `&`.
- **Human-in-the-loop**: `UserProxyAgent`.
- **Status**: maintenance mode since Oct 2025; ideas live on in Agent Framework.

**Exercise:** swap to `RoundRobinGroupChat`, then add a `UserProxyAgent` that must approve ESCALATE.

**Quiz:** 1) Selector vs RoundRobin? 2) Why does `description` matter? 3) Two ways a team stops? 4) Which package has the runtime? 5) How do you add human approval?

## Day 3 — Microsoft Agent Framework (study 1.5h, build 1.5h)
- **What**: GA April 2026; merges SK enterprise features (state, type safety, middleware, telemetry) with AutoGen orchestration.
- **Agent**: `Agent(client, instructions, name=, tools=[...])`; `.run()` / streaming; `AgentSession` for state.
- **Tools**: plain Python functions, `@tool` (with `approval_mode` for human approval), MCP tools, OpenAPI.
- **Middleware**: agent / function middleware → guardrails, audit, PII redaction.
- **Workflows**: graph of executors (`WorkflowBuilder`, edges, fan-out/fan-in, switch-case), checkpointing.
- **Orchestrations**: Sequential, Concurrent, GroupChat, Handoff, Magentic.
- **Migration**: SK `ChatCompletionAgent` → `Agent`; AutoGen teams → orchestrations.

**Exercise:** mark `get_customer_profile` with `@tool(approval_mode=...)`, then try `ConcurrentBuilder` for parallel KYC + policy lookup.

**Quiz:** 1) What did MAF take from SK vs AutoGen? 2) Workflow vs orchestration? 3) Where do guardrails go? 4) How is human approval enforced? 5) Why is checkpointing important in banking?

---
## Interview talking points
- "SK and AutoGen have converged into Microsoft Agent Framework; I build new work on MAF and can migrate SK/AutoGen code."
- Governance: every tool call audited (filters/middleware), human approval on high-risk actions, policy-cited decisions.
- Next: replace `search_policy` with Azure AI Search vector RAG; add eval set (expected decision per alert) as a CI quality gate.
