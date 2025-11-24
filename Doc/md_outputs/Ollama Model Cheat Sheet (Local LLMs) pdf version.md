# Ollama Model Cheat Sheet (Local LLMs) pdf version

Extracted from PDF: Ollama Model Cheat Sheet (Local LLMs) pdf version.pdf

---

🧠 Ollama Model Cheat Sheet (Local
LLMs)

This cheat sheet summarizes the most powerful and specialized models, focusing on
performance metrics like VRAM, size, and context window, which are critical for local
deployment.
Category
Model
Size
VRAM
Context
Speed
Primary Use
Name
(Approx)
(Approx)
(Tokens)
(tok/s)
& Notes
Primary
qwen2.5-cod ~9 GB
~9 GB
32K
25–30
Best overall
Coding
er:14b
balance for
coding tasks.
High
deepseek-co ~9 GB
~10 GB
128K
20–25
Massive
Context
der-v2:16b
context
Coding
window.
Excellent for
large
projects/rep
os.
Max
codestral:22 ~13 GB
~11 GB
128K
15–20
Largest
Context
b
coding
Coding
model listed.
Great for
context, but
slower and
VRAM-intens
ive.
Fast Coding qwen2.5-cod ~4.7 GB
~5 GB
32K
40–45
Extremely
Backup
er:7b
fast and
lightweight
coding
model.
General
qwen2.5:14b ~9 GB
~9 GB
32K
25–30
Excellent
Chat/Writin
general-purp
g
ose model
with strong
writing
capabilities.
Complex
deepseek-r1: ~9 GB
~9 GB
8K
20–25
Strong
Reasoning 14b
reasoning
model, good

Alternative phi4:14b
Reasoning

~9 GB

16K

25–30

llava-llama3: ~5.5 GB
8b

~6 GB

N/A

30–35

Specialized codellama:13 ~7.4 GB
Python
b-python

~8 GB

N/A

25–30

Vision
Model
(Fast)

~9 GB

🛠️ Quick Reference & Lightweight Models

upgrade
from 7B
versions.
Great
alternative
with a larger
context for
reasoning.
Faster, more
efficient
vision model
for image
understandin
g.
Specialized
model if you
heavily focus
on Python
development
.

These models are useful for quick checks, lightweight systems, or as alternative benchmarks.
Model Name
Purpose / Note
Ollama Pull Command
phi3:mini
Very fast (3.8B) for quick,
ollama pull phi3:mini
conversational queries.
gemma3:4b
Lightweight backup general
ollama pull gemma3:4b
model.
mistral:latest
Standard, good performance ollama pull mistral:latest
7B general model.
llava:13b
Older, but still functional Vision ollama pull llava:13b
model.
qwen3-coder:latest
Newer coding model (check
ollama pull qwen3-coder:latest
size, use if 14B or less).

