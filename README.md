<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=21&duration=3400&pause=900&color=2F81F7&center=true&vCenter=true&width=620&height=42&lines=AI%20agents%20that%20survive%20production%3BFail%20loudly%2C%20never%20corrupt%20silently%3BAnswers%20that%20cite%20their%20source%2C%20or%20admit%20they%20can%27t" alt="AI agents that survive production" />

<br />

<img src="https://img.shields.io/badge/Available_for_new_projects-2EA043?style=flat-square&labelColor=2EA043&color=2EA043" alt="Available for new projects" />

</div>

## Amir K.

**AI agents and automation that survive contact with real data.**

I build the parts most automation skips: retries, caching, idempotency and
resume-on-failure — so a bad API response at 3am degrades loudly instead of
corrupting a pipeline silently.

---

### What I can build for you

**Webhook and pipeline automation** — inbound events turned into reliable work.
Signed, idempotent, retry-safe, so a retry never double-bills a model call or
writes the same record twice.

**Retrieval and document Q&A** — answers that cite the passage they came from,
so a wrong answer surfaces as *unsupported* instead of confident and wrong.

**LLM agents with guardrails** — scoring, extraction and classification where the
model supplies evidence and code computes the result, never the other way around.

**Backend services** — FastAPI, PostgreSQL, Docker, Linux. The unglamorous half
that decides whether the clever half is still running a month from now.

---

### Stack

**Languages and backend**

<img src="https://skillicons.dev/icons?i=python,fastapi,flask,nodejs,typescript" alt="Python, FastAPI, Flask, Node.js, TypeScript" height="42" />

**AI and agents**

![Claude](https://img.shields.io/badge/Claude-D97757?style=flat-square&logo=anthropic&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square) ![MCP](https://img.shields.io/badge/MCP-1E1E1E?style=flat-square) ![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat-square&logo=n8n&logoColor=white)

**Data**

<img src="https://skillicons.dev/icons?i=postgres,sqlite,redis" alt="PostgreSQL, SQLite, Redis" height="42" />

**Infrastructure**

<img src="https://skillicons.dev/icons?i=docker,linux,nginx,git,githubactions" alt="Docker, Linux, nginx, Git, GitHub Actions" height="42" />

---

### Selected projects

<a href="https://github.com/amirk-dev/docqa">
  <img src="https://socialify.git.ci/amirk-dev/docqa/image?description=1&font=Inter&language=1&name=1&owner=1&pattern=Solid&theme=Auto" alt="docqa" width="640" />
</a>

Ask questions against your own documents and get answers that cite the exact
passage. The anti-hallucination guarantee is structural, not a prompt: the model
must return the IDs of the passages it used, and any ID that wasn't in the
retrieved context is stripped and the answer flagged unsupported — so an invented
source shows up as a *visibly unsupported answer* instead of a confident wrong one.
A content-addressed embedding cache makes re-indexing an unchanged corpus a 100%
cache hit and ~8x faster on a 4,669-chunk index.

<a href="https://github.com/amirk-dev/leadqual">
  <img src="https://socialify.git.ci/amirk-dev/leadqual/image?description=1&font=Inter&language=1&name=1&owner=1&pattern=Solid&theme=Auto" alt="leadqual" width="640" />
</a>

n8n posts an inbound lead, Claude scores it against a rubric, hot leads land in
Slack with a reason and a next step. The model never picks the score: five criteria
with fixed point ceilings, evidence quoted per criterion, total computed in code
and clamped. The webhook is HMAC-signed with a replay window, and `external_id` is
an idempotency key — so n8n retries never double-bill a model call.

<a href="https://github.com/amirk-dev/agentic-course">
  <img src="https://socialify.git.ci/amirk-dev/agentic-course/image?description=1&font=Inter&language=1&name=1&owner=1&pattern=Solid&theme=Auto" alt="agentic-course" width="640" />
</a>

A twenty-day course on agentic systems, built as a static Next.js app —
[read it here](https://amirk-dev.github.io/agentic-course/). The argument is that
the agent loop is one layer out of nine, and the other eight decide whether the
thing holds up: harness, rules, skills, MCP and memory all treated as one scale of
*when does this enter the context*. Includes a design method, a topology catalogue
and a twenty-day practice track. **Course content is in Russian.**

---

### How I work

I start from the process you actually run, not from the tool. First call: I map
your steps and tell you which parts are worth automating, which aren't, and where
it will break. Then I ship the smallest version that works, prove it on your real
data, and expand.

---

📫 policedepartments154@gmail.com · Almaty, Kazakhstan (UTC+5), remote · English (fluent), Russian (native)
