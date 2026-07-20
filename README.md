# Amir K.

**AI agents and automation that survive contact with real data.**

I build the parts most automation skips: retries, caching, idempotency and
resume-on-failure — so a bad API response at 3am degrades loudly instead of
corrupting a pipeline silently.

Python · FastAPI · n8n · Claude / OpenAI · PostgreSQL · Docker · Linux

---

### Selected projects

**[docqa](https://github.com/amirk-dev/docqa)** — grounded document Q&A with citations
Ask questions against your own documents and get answers that cite the exact
passage. The anti-hallucination guarantee is structural, not a prompt: the model
must return the IDs of the passages it used, and any ID that wasn't in the
retrieved context is stripped and the answer flagged unsupported — so an invented
source shows up as a *visibly unsupported answer* instead of a confident wrong one.
A content-addressed embedding cache makes re-indexing an unchanged corpus a 100%
cache hit and ~8x faster on a 4,669-chunk index.

**[leadqual](https://github.com/amirk-dev/leadqual)** — webhook lead qualification agent
n8n posts an inbound lead, Claude scores it against a rubric, hot leads land in
Slack with a reason and a next step. The model never picks the score: five criteria
with fixed point ceilings, evidence quoted per criterion, total computed in code
and clamped. The webhook is HMAC-signed with a replay window, and `external_id` is
an idempotency key — so n8n retries never double-bill a model call.

---

### How I work

I start from the process you actually run, not from the tool. First call: I map
your steps and tell you which parts are worth automating, which aren't, and where
it will break. Then I ship the smallest version that works, prove it on your real
data, and expand.

📫 [Upwork](https://www.upwork.com/freelancers/~019c7aed624039e00f) · English (fluent), Russian (native)
