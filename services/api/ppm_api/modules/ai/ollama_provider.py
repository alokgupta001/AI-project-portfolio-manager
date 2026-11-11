"""Ollama inference seam; no install, model-management or cloud endpoints exposed."""

from ppm_api.modules.ai.adapters import NativeAdapter

OllamaProvider = NativeAdapter
