<div align="center">

<!-- БАННЕР. Когда пришлёте арт (1600x400, имя "Amir K." вписано внутрь):
     положите файл в assets/banner.png и замените строку ниже на
     <img src="assets/banner.png" width="100%" alt="Amir K." />          -->
<img src="https://capsule-render.vercel.app/api?type=soft&color=0:FFC0D9,50:C8A2E0,100:9AD5E8&height=190&section=header&text=Amir%20K.&fontSize=54&fontColor=4A2E5C&fontAlignY=38&desc=AI%20agents%20%C2%B7%20automation%20%C2%B7%20integrations&descAlignY=58&descSize=18" alt="Amir K." width="100%" />


<br />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3400&pause=900&color=FF8FB1&center=true&vCenter=true&width=600&height=40&lines=AI%20agents%20that%20survive%20production%3BFail%20loudly%2C%20never%20corrupt%20silently%3BRetries%2C%20caching%2C%20idempotency" alt="AI agents that survive production" />

<br />

<img src="https://img.shields.io/badge/Available_for_new_projects-FF8FB1?style=for-the-badge&labelColor=C8A2E0" alt="Available for new projects" />
<img src="https://komarev.com/ghpvc/?username=amirk-dev&color=FF8FB1&style=for-the-badge&label=VISITORS" alt="Visitors" />

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF8FB1,33:C8A2E0,66:7FD1B9,100:9AD5E8&height=5&section=header" width="100%" alt="" />

## 🌸 Hi, I'm Amir

**AI agents and automation that survive contact with real data.**

I build the parts most automation skips: retries, caching, idempotency and
resume-on-failure — so a bad API response at 3am degrades loudly instead of
corrupting a pipeline silently.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF8FB1,33:C8A2E0,66:7FD1B9,100:9AD5E8&height=5&section=header" width="100%" alt="" />

## 🚀 Now Building

<!--START_SECTION:now-building-->
- **[bc-rent-demo](https://github.com/amirk-dev/bc-rent-demo)** &mdash; Business-centre lease management: an interactive demo of the tenant, contract and billi... `2026-09-02`
- **[agentic-course](https://github.com/amirk-dev/agentic-course)** &mdash; A twenty-day course on agentic systems: nine architectural layers, a design method, and... `2026-09-02`
- **[leadqual](https://github.com/amirk-dev/leadqual)** &mdash; Webhook lead qualification agent: n8n posts a lead, Claude scores it against a rubric,... `2026-07-20`

<sub>Refreshed automatically on 2026-09-02 (UTC).</sub>
<!--END_SECTION:now-building-->

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF8FB1,33:C8A2E0,66:7FD1B9,100:9AD5E8&height=5&section=header" width="100%" alt="" />

## 💗 What I can build for you

| | |
|---|---|
| **Webhook and pipeline automation** | Inbound events turned into reliable work. Signed, idempotent, retry-safe, so a retry never double-bills a model call or writes the same record twice. |
| **Retrieval and document Q&A** | Answers that cite the passage they came from, so a wrong answer surfaces as *unsupported* instead of confident and wrong. |
| **LLM agents with guardrails** | Scoring, extraction and classification where the model supplies evidence and code computes the result, never the other way around. |
| **Backend services** | FastAPI, PostgreSQL, Docker, Linux. The unglamorous half that decides whether the clever half is still running a month from now. |

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF8FB1,33:C8A2E0,66:7FD1B9,100:9AD5E8&height=5&section=header" width="100%" alt="" />

## 🧰 Stack

**Languages and backend**

<img src="https://skillicons.dev/icons?i=python,fastapi,flask,nodejs,typescript" alt="Python, FastAPI, Flask, Node.js, TypeScript" height="42" />

**AI and agents**

![Claude](https://img.shields.io/badge/Claude-FF8FB1?style=for-the-badge&logo=anthropic&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-C8A2E0?style=for-the-badge) ![MCP](https://img.shields.io/badge/MCP-B98BD9?style=for-the-badge) ![n8n](https://img.shields.io/badge/n8n-FFC49B?style=for-the-badge&logo=n8n&logoColor=white)

**Data and infrastructure**

<img src="https://skillicons.dev/icons?i=postgres,sqlite,redis,docker,linux,nginx,git,githubactions" alt="PostgreSQL, SQLite, Redis, Docker, Linux, nginx, Git, GitHub Actions" height="42" />

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF8FB1,33:C8A2E0,66:7FD1B9,100:9AD5E8&height=5&section=header" width="100%" alt="" />

## 📦 Selected projects

<a href="https://github.com/amirk-dev/docqa">
  <img src="https://socialify.git.ci/amirk-dev/docqa/image?description=1&font=Inter&language=1&name=1&owner=1&pattern=Solid&theme=Auto" alt="docqa" width="640" />
</a>

Ask questions against your own documents and get answers that cite the exact
passage. The anti-hallucination guarantee is structural, not a prompt: the model
must return the IDs of the passages it used, and any ID that wasn't in the
retrieved context is stripped and the answer flagged unsupported. A
content-addressed embedding cache makes re-indexing an unchanged corpus a 100%
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
*when does this enter the context*. **Course content is in Russian.**

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF8FB1,33:C8A2E0,66:7FD1B9,100:9AD5E8&height=5&section=header" width="100%" alt="" />

## 📊 Snapshot

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/languages-dark.svg" />
  <img src="assets/languages.svg" alt="Languages" width="480" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/activity-dark.svg" />
  <img src="assets/activity.svg" alt="Activity" width="480" />
</picture>

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF8FB1,33:C8A2E0,66:7FD1B9,100:9AD5E8&height=5&section=header" width="100%" alt="" />

## 🎐 Quote of the day

<!--START_SECTION:quote-->
<table><tr><td>

> *Games are not boring. Games purify our souls and leave room for new development that challenges the mind! They are the products of human wisdom!*
>
> **Seto Kaiba** &mdash; Yu-Gi-Oh!

</td></tr></table>
<!--END_SECTION:quote-->

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF8FB1,33:C8A2E0,66:7FD1B9,100:9AD5E8&height=5&section=header" width="100%" alt="" />

## 🍵 How I work

I start from the process you actually run, not from the tool. First call: I map
your steps and tell you which parts are worth automating, which aren't, and where
it will break. Then I ship the smallest version that works, prove it on your real
data, and expand.

<div align="center">

<br />

📫 **policedepartments154@gmail.com** &nbsp;·&nbsp; Almaty, Kazakhstan (UTC+5), remote &nbsp;·&nbsp; English (fluent), Russian (native)

<br />

<sub>Language and activity cards are generated by <a href="scripts/gen_stats.py">a script in this repo</a> and committed daily — no third-party uptime involved.</sub>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:9AD5E8,50:C8A2E0,100:FFC0D9&height=110&section=footer" alt="" width="100%" />

</div>
