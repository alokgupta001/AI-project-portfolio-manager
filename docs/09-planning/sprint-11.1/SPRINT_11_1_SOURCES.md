# External technical verification

Public primary sources checked 17 October 2026. These are capability/terms observations, not account verification or benchmark results. Model catalogs and quotas can change; recheck at activation or version change. No live inference, authenticated account inspection or model download occurred.

| Source | Observation used / implementation consequence |
| --- | --- |
| [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs) | JSON schema can constrain output; validate again in Pydantic. Schema mode does not establish factual support. |
| [Ollama chat API](https://docs.ollama.com/api/chat) | Chat accepts model/messages/format/options/stream and exposes completion/timing/token metadata; adapter contract must preserve it. |
| [Ollama embeddings API](https://docs.ollama.com/api/embed) | Has dimensions and truncate flag; set truncate=false and verify actual dimension support, do not assume every model supports 256. |
| [Ollama FAQ](https://docs.ollama.com/faq) | Documents context/concurrency/model-residency controls, cloud disable setting and local networking. The design explicitly configures 4096 context and one generation instead of relying on defaults. |
| [Ollama Windows](https://docs.ollama.com/windows) | Native Windows install/API and model storage are supported. Integrated graphics performance is not established by this page. |
| [Ollama installed model list](https://docs.ollama.com/api/tags) | `/api/tags` returns installed model digest and metadata; bind profile to actual digest. |
| [Ollama source API documentation](https://github.com/ollama/ollama/blob/main/docs/api.md) | `/api/show` exposes model details. The newer `/api/show` documentation URL returned 404 during this audit; verify installed API behavior in T05. |
| [Qwen3 4B](https://ollama.com/library/qwen3:4b) | Observed Q4_K_M, about 2.5 GB download, Apache 2.0 model license listing. Candidate only, not a RAM/latency guarantee. |
| [Qwen3 1.7B](https://ollama.com/library/qwen3:1.7b) | Observed about 1.4 GB Q4_K_M download; smaller candidate. Pin actual installed digest rather than interpreting the tag as immutable. |
| [Gemma3 4B](https://ollama.com/library/gemma3:4b) | Observed about 3.4 GB package with associated projector information and Gemma terms. Text-only task does not require multimodal benefit; compare measured overhead/quality. |
| [EmbeddingGemma](https://ollama.com/library/embeddinggemma) | Observed 300m tag, 622 MB package, 2K context, Ollama version prerequisite. Keep local embeddings optional and benchmark dimensional/profile compatibility. |
| [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) | Current page lists repository IDs gemini-3.5-flash-lite and gemini-embedding-2 with free-tier offerings. Free-tier data-use terms differ from paid terms. This does not establish this account's no-billing state. |
| [Gemini limits](https://ai.google.dev/gemini-api/docs/rate-limits) | Limits depend on active tier/project and are viewed in AI Studio; capacity not guaranteed. Do not invent static universal RPM/RPD or count keys as new quota. |
| [Groq rate limits](https://console.groq.com/docs/rate-limits) | Limits apply at organization scope; account-specific limits and rate-limit headers inform cooldown. Candidate adapter remains disabled until configured. |
| [Groq billing](https://console.groq.com/docs/billing-faqs) | Free and paid Developer tiers differ; upgrading adds usage-based billing. A key alone does not indicate a non-billable account. |
| [Groq structured outputs](https://console.groq.com/docs/structured-outputs) | Model-specific support must be verified; OpenAI-compatible request shape is not proof of all required capabilities. |
| [HTTPX async client](https://www.python-httpx.org/async/) | AsyncClient supports asynchronous outgoing HTTP and explicit close; proposed v2 transport uses it to avoid urllib thread lifetime controlling cancellation. Disconnect still cannot guarantee upstream compute stopped. |

Official defaults, advertised context and package size are observations from these sources. Architecture limits, memory margins, quality thresholds, per-task selection, concurrency one and deferred scope policy are **our design choices**, not claims made by the model vendors. Account-specific authorization, real output quality and measured hardware results remain T12/T13 gates.
