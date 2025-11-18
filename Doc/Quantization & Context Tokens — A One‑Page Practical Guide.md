# Quantization & Context Tokens — A One‑Page Practical Guide

This is a compact reference explaining context windows (tokens) and common quantization labels you’ll see in Ollama (`Q4_K_M`, `Q4_0`, `BF16`, `FP8`, `INT4`, etc.). Focus is on practical implications for running a home LLM server (CPU + occasional GPU) and how to pick models for tasks.

---

## Tokens & Context — what matters to you
- Token = model unit (not exactly a word). Quick heuristics:
  - 1 token ≈ 4 characters ≈ 0.75 words (English, rough).  
  - Example: "Hello world" → ~2–3 tokens.
- Context window = maximum number of tokens the model can see at once (prompt + conversation + files).
  - If model context = 32k, it can consider ~32,000 tokens of combined system+chat+files.
  - Larger context is useful for long documents, codebases, or multi-file summarization.
- Practical effects:
  - Hitting the context limit truncates older content (most models keep the most recent tokens).
  - For long documents, chunk into overlapping pieces (e.g., 2–5% overlap) and use retrieval + summarization or embeddings + retrieval.
  - Large context models (e.g., phi3:mini 131,072 tokens) are ideal for long-document summarization and multi-file context, but may lack capabilities like tool_use.
- How to measure your document's tokens:
  - Quick rule: tokens ≈ characters / 4. For exact counts use a tokenizer tool compatible with your model family.
- For Continue / cn workflows:
  - Be mindful of system + tool messages; they consume tokens too.
  - Keep prompts concise and push large data via file uploads or embeddings + retrieval.

---

## What “Q4_K_M”, “Q4_0”, etc. mean (practical summary)
- High-level: Quantization reduces model weight precision (FP16/FP32 → fewer bits), drastically lowering RAM/VRAM and disk footprint so models can run on CPU and smaller GPUs.
- 4‑bit quant (Q4_*) is common for local inference; it lets you run 7B/13B models on CPU where full-precision would be impossible.

Common labels you’ll encounter (and what to expect)
- Q4_K_M
  - A 4‑bit quant format (GPTQ-style) used widely for good quality/size tradeoffs.
  - Practical: small on disk and memory, reasonable fidelity to full‑precision, slightly more CPU work per token than the simplest 4‑bit formats.
  - Many of your local models (qwen2.5 variants, mistral, gemma3) use Q4_K_M.
- Q4_0
  - Another 4‑bit scheme that is simple and fast; used for models like phi3:mini.
  - Practical: very compact and often slightly faster to load/infer on CPU; quality may differ slightly vs Q4_K_M depending on model.
- BF16 / FP16 / FP32
  - Floating-point formats — BF16/FP16 common for GPU inference. FP32 is highest precision (largest).
  - Practical: GPU performance is best with BF16/FP16; CPU inference with FP32 is usually infeasible for large models.
- FP8 / INT4 / MXFP4 (cloud/server-side formats)
  - Advanced formats often used in cloud servers for higher efficiency. You’ll see these on proxied cloud models — they imply nothing about your local hardware.
- INT4 / 4-bit variants in cloud
  - Extremely small footprints, highly engineered for large model servers.

Practical takeaways about quant formats
- If a model is Q4_* it’s likely usable on CPU (with slower token rates), and will load with much smaller RAM/disk requirements than non‑quantized weights.
- Q4_K_M generally gives better quality than very simple 4-bit encodings at the cost of slightly more CPU work — a good default for local setups.
- If you need speed on GPU, prefer BF16/FP16 builds or GPU-optimized variants rather than CPU-quantized Q4_*.

---

## What this means for your home server (GTX 1040 today, 3060 coming)
- On CPU (GTX 1040 effectively unusable for modern LLMs):
  - Prefer Q4_* models — they’ll run (slowly) and won’t require massive RAM.
  - Use small/quantized coder models (qwen2.5-coder:1.5b) for tools/editor — fast to start and respond.
  - Use phi3:mini (Q4_0) for long-context tasks (128K context) but note it has no tool support.
  - Expect token rates of a few tokens/sec for 3–8B quantized models; 18–30B models will take minutes to load and run painfully slow.
- After you install RTX 3060 (12 GB VRAM):
  - You can run larger models on GPU (7B–14B) with acceptable speed if the model/weights are GPU-optimized or quantized for GPU.
  - Still check model VRAM requirements — many 14B/16B models are tight on 12 GB unless quantized/offload is supported.
  - For best GPU throughput, use BF16/FP16 or GPU-quantized builds rather than CPU-quantized Q4_*.

---

## How to use Ollama commands to read quant & context info
- `ollama show <model>` displays:
  - architecture, parameters (e.g., 7.6B), context length, quantization (e.g., Q4_K_M), capabilities (tools, completion, vision, thinking).
- `ollama ls` lists installed models and disk sizes (helps decide which to keep).
- `ollama run <model>` to test load time & latency (do this on the server to avoid network noise).

---

## Practical rules-of-thumb & recommendations
- Defaults while on CPU (your current setup):
  - Default tool model: `qwen2.5-coder:1.5b` (Q4_K_M) — small, tool-capable, fast.
  - Long-context chat: `phi3:mini` (Q4_0) — use for documents and summarization.
  - Higher-quality but slower: `qwen2.5:7b`, `mistral:latest` (Q4_K_M) — bump timeouts before using.
- Increase client/server timeouts (Continue `requestOptions.timeout`) to 600k–900k ms for heavy models on CPU.
- If a model shows `:cloud` or Remote URL in `ollama show`, it's proxied — using it will consume quota and network latency.
- Keep large models installed if you want them later, but avoid interactive use until the 3060 (or until you have quantized/offload builds).

---

## One-liner checklist (quick reference)
- Token heuristic: 1 token ≈ 4 chars ≈ 0.75 words.  
- Long-context model (phi3:mini) → use for big docs (no tools).  
- Tool workflows → use Q4_K_M small coder (qwen2.5-coder:1.5b).  
- Q4_* ⇒ small footprint, CPU-usable; Q4_K_M balances quality vs size.  
- Use `ollama show` and `ollama run` to verify quantization, context, load times.  
- When you get the 3060, test GPU runs with `nvidia-smi` + `ollama run <model>`.

---

If you want, I can:
- add this file to `Doc/` in your repo (create commit/branch/PR), or
- generate a one‑page PNG for desktop reference.
Which would you like next?
