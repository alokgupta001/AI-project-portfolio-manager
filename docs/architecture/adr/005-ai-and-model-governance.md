# ADR 005 AI evidence tools and model eligibility

Status: proposed baseline. Sources: W1, W2, W4, W5, WT, S4.2, S4.3, S5M, S5D. Decision date: 2026-10-05.

Use provider adapters for completion/embedding/transcription/TTS, one configured provider implementation initially, typed orchestration and LangChain retrieval/tools where useful. OpenAI/Gemini/Ollama/HuggingFace are alternatives to evaluate against actual availability, privacy and budget; no model name or external credentials are assumed. LlamaIndex is an alternative, not a second mandatory framework.

Every output has validated structure, source references, snapshot/model/prompt/rule versions, limitations and status. Validation rejects malformed data but does not prove truth. Agents use read-only allowlisted tools and propose actions for workflow approval. Retrieval text cannot override authorization or tool policy. Progress streaming means observable stages and concise evidence summaries, not hidden reasoning.

Use scikit-learn/pandas, baseline models, XGBoost/Random Forest and MLflow first. LightGBM, LSTM, time-series models and DistilBERT/PyTorch are candidates evaluated only when data fits. Freeze temporal/entity-separated holdouts and promotion criteria before experiments. Synthetic/public data may prove reproducibility without proving enterprise prediction validity. Risk score and failure probability are different quantities.

Team overload/sentiment indicators are advisory, not diagnoses or individual rankings. Default suppression is fewer than five team resources; production policy may require stricter controls. Missing features, out-of-domain inputs and low evidence coverage produce abstention or labeled rules-based output. Consequence: model-dependent requirements may remain incomplete even when a demo UI works.
