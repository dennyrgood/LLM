# Project Docs Index (human-maintained)

This is a curated Table of Contents for the Doc/ folder. It integrates original PDFs and converted, readable Markdown equivalents (Doc/md_outputs/) into the same high-level categories so you have both the searchable/quotable text and the authoritative source.

Notes
- When a PDF has a converted Markdown in `Doc/md_outputs/`, the MD is listed first (for quick searching/quoting) and the PDF is linked as the authoritative source.
- The DOCX file is treated as a Guide.
- Use `Doc/_autogen_index.md` for a machine-generated, up-to-date listing.

---

## High-level categories

### Guides (setup, long-form)
- [GROK.Ollama.on.Win11.Ultimate.Perf.Guide.md](./GROK.Ollama.on.Win11.Ultimate.Perf.Guide.md) — Ollama on Windows 11 – Ultimate Performance Guide (RTX 3060). Deep tuning: drivers, CUDA advice, Ollama GPU offload, quantization, monitoring and a model leaderboard for 12 GB VRAM.
- [New RTX 3060 Setup - SETTING_UP_REAL_IMAGE_MANIPULATION_LOCAL_SERVER.md](./New%20RTX%203060%20Setup%20-%20SETTING_UP_REAL_IMAGE_MANIPULATION_LOCAL_SERVER.md) — ComfyUI + Flux image pipeline: downloads, folder structure, workflows (background replace, old-photo restoration), and integration with Open WebUI.
- [Using 1040 until 3060 Gets Here](./Using%201040%20until%203060%20Gets%20Here) — Tactical guidance and default model choices while on CPU / GTX 1040 (timeouts, Continue config, quick model picks).
- [Claude session - started the whole rabbit trail of hosting my own LLM.md](./Claude%20session%20-%20started%20the%20whole%20rabbit%20trail%20of%20hosting%20my%20own%20LLM.md) — Notes from a Claude session: commit-message automation approaches, Ollama examples, local vs cloud tradeoffs, and a copilot-like script.
- [Prep for 3060 - in the mean time as well.docx](./Prep%20for%203060%20-%20in%20the%20mean%20time%20as%20well.docx) — DOCX guide with preparatory notes and checklist (treat as a long-form guide; convert to MD for search if desired).
- [md_outputs/RTX 3060 Setup Guide - Complete AI Coding Workflow.md](./md_outputs/RTX%203060%20Setup%20Guide%20-%20Complete%20AI%20Coding%20Workflow.md) — Converted from: [RTX 3060 Setup Guide - Complete AI Coding Workflow.pdf](./RTX%203060%20Setup%20Guide%20-%20Complete%20AI%20Coding%20Workflow.pdf) — Hardware & software phases, essential model pulls (qwen2.5-coder:14b, deepseek-coder-v2:16b), Continue config examples, benchmarks and troubleshooting.
- [md_outputs/Setting Up Real Image Manipulation on Your Local Server.md](./md_outputs/Setting%20Up%20Real%20Image%20Manipulation%20on%20Your%20Local%20Server.md) — Converted from: [Setting Up Real Image Manipulation on Your Local Server.pdf](./Setting%20Up%20Real%20Image%20Manipulation%20on%20Your%20Local%20Server.pdf) — ComfyUI + Flux installation, model placement, Manager/plugins, essential workflows, and ComfyUI <-> Open WebUI integration.
- [md_outputs/Open WebUI Management Guide.md](./md_outputs/Open%20WebUI%20Management%20Guide.md) — Converted from: [Open WebUI Management Guide.pdf](./Open%20WebUI%20Management%20Guide.pdf) — NSSM service commands, data directory locations (webui.db, uploads/, vector_db/), backups, and Cloudflare tunnel notes.
- [md_outputs/AIChat CLI_ Capabilities and User Guide Summary.md](./md_outputs/AIChat%20CLI_%20Capabilities%20and%20User%20Guide%20Summary.md) — Converted from: [AIChat CLI_ Capabilities and User Guide Summary.pdf](./AIChat%20CLI_%20Capabilities%20and%20User%20Guide%20Summary.pdf) — AIChat CLI overview: one-liner mode, Chat REPL, Shell Assistant, multi-file context (-f), roles (-r), RAG and local API serve mode.

### Quick references / cheat sheets
- [Quantization & Context Tokens — A One‑Page Practical Guide.md](./Quantization%20%26%20Context%20Tokens%20%E2%80%94%20A%20One%E2%80%91Page%20Practical%20Guide.md) — Token heuristics and concise quantization summary (Q4_K_M, Q4_0, BF16, FP8) and practical rules for CPU vs GPU.
- [Quantization and Context Tokens — One‑Page Guide.html](./Quantization%20and%20Context%20Tokens%20%E2%80%94%20One%E2%80%91Page%20Guide.html) — One-page HTML view for quick browser reading.
- [LLM QUICK SELECTION GUIDE.txt](./LLM%20QUICK%20SELECTION%20GUIDE.txt) — Short model-selection cheat sheet mapping tasks to model families.
- [Ollama Download Commands for Recommended LLMs.pdf](./Ollama%20Download%20Commands%20for%20Recommended%20LLMs.pdf) — Quick pull commands PDF (use converted MD for searchable commands where available).

### Models & inventory
- [Ollama Models as of 2025 11 18](./Ollama%20Models%20as%20of%202025%2011%2018) — Model-by-model notes, default choices, quantization and CPU/GPU guidance.
- [GROK.recommended.llms.w.RTX.3060.txt](./GROK.recommended.llms.w.RTX.3060.txt) — Recommended pulls and suggested first-models for RTX 3060 12GB.
- [GROK.recommended.nano.banana.replacement.txt](./GROK.recommended.nano.banana.replacement.txt) — Image model recommendations (ComfyUI + Flux), workflows and restoration tool choices.
- [ollama-ls.txt](./ollama-ls.txt) — Raw `ollama ls` listing for installed models, sizes and modified timestamps.
- [ollama-show-out.txt](./ollama-show-out.txt) — `ollama show` outputs for many models (context length, quantization, capabilities).
- [ollama website list - LLM.txt](./ollama%20website%20list%20-%20LLM.txt) — Catalog of model families and sizes for planning.

### Workflows & automation
- [OpenWebUI — Task Scheduler CLI Reference.txt](./OpenWebUI%20%E2%80%94%20Task%20Scheduler%20CLI%20Reference.txt) — Run OpenWebUI at startup using Task Scheduler (SYSTEM): run script example, schtasks commands, firewall and logging tips.
- [Open WebUI Installation Guide for Windows 11.pdf](./Open%20WebUI%20Installation%20Guide%20for%20Windows%2011.pdf) — Installation and service notes; refer to converted MD for management commands.
- [md_outputs/Open WebUI Management Guide.md](./md_outputs/Open%20WebUI%20Management%20Guide.md) — Management and troubleshooting notes (see above).
- [ollama-show.bat](./ollama-show.bat) — Batch helper script for multiple `ollama show` commands.
- [ollama.help](./ollama.help) — Short helper text for the Ollama runner in this repo.

### Converted PDF → Markdown (Doc/md_outputs/)
(Readable MD files produced from PDFs — use these for searching and quoting; the original PDFs remain in Doc/.)
- [md_outputs/AIChat CLI_ Capabilities and User Guide Summary.md](./md_outputs/AIChat%20CLI_%20Capabilities%20and%20User%20Guide%20Summary.md) — (Guide) AIChat CLI: modes, REPL, Shell Assistant, multi-file context, roles, RAG and serve mode.
- [md_outputs/Setting Up Real Image Manipulation on Your Local Server.md](./md_outputs/Setting%20Up%20Real%20Image%20Manipulation%20on%20Your%20Local%20Server.md) — (Guide) ComfyUI + Flux installation and workflows.
- [md_outputs/RTX 3060 Setup Guide - Complete AI Coding Workflow.md](./md_outputs/RTX%203060%20Setup%20Guide%20-%20Complete%20AI%20Coding%20Workflow.md) — (Guide) Hardware + software phases, model pulls, Continue config and benchmarks.
- [md_outputs/Open WebUI Management Guide.md](./md_outputs/Open%20WebUI%20Management%20Guide.md) — (Workflow) NSSM commands, data location, backups and Cloudflare tunnel integration.

### Scripts & small artifacts
- [What to Try Next.txt](./What%20to%20Try%20Next.txt) — Short experiments and model suggestions.
- [a](./a) — Small file containing a list of `ollama show` commands.
- [ollama-show.bat](./ollama-show.bat) — Batch helper.

### Binary / Office files
- [Prep for 3060 - in the mean time as well.docx](./Prep%20for%203060%20-%20in%20the%20mean%20time%20as%20well.docx) — DOCX guide (moved into Guides above). Convert to MD for indexing/search if you want.

---

## How links are organized in this index
- If a PDF has a converted Markdown in `Doc/md_outputs/`, the MD is listed first (for searchability) with the PDF shown as the authoritative source. Example:
  - `md_outputs/SomeDoc.md` — Converted from: `SomeDoc.pdf`

## Recommended tiny housekeeping
- Option A (recommended): Move all original PDFs into `Doc/PDFs/` and keep converted MD in `Doc/md_outputs/`; I can create a branch/PR that does this and fixes links.
- Option B: Add YAML frontmatter to every MD in `Doc/md_outputs/` (title, source_pdf, page_count) — I can automatically add frontmatter in a PR.
- Option C: Generate a JSON search index (title, excerpt, path) from `Doc/md_outputs/` for fast programmatic search.

---

End of curated index.