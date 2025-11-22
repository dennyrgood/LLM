ollama rm qwen2.5-coder:7b
ollama rm qwen2.5:7b
ollama rm phi3:mini
ollama rm deepseek-r1:latest
ollama rm llama3.1:latest
```

**Why remove llama3.1 and the 7b models?** You have better options - phi4:14b is faster AND better quality than llama3.1:8b, and your 14b models are superior to the 7b versions.

---

## Your Final Optimized Lineup (8 Models)

After cleanup:
```
CODING (Quality Tier):
- codestral:22b          - Best quality coder
- deepseek-coder-v2:16b  - Complex algorithms
- qwen2.5-coder:14b      - Fast iterations

GENERAL CHAT:
- qwen2.5:14b           - Main chat model
- phi4:14b              - Fast all-rounder

SPECIALIZED:
- deepseek-r1:14b       - Reasoning/math
- llava-llama3:8b       - Vision/images

+ Cloud models (keep - they're free)
```

---

## Your Cheat Sheet (Simplified)

### 🔧 **CODING**
```
Default:    qwen2.5-coder:14b
Quality:    codestral:22b ← Use for your tkinter problem
Hard stuff: deepseek-coder-v2:16b
```

### 💬 **CHAT**
```
Default:    qwen2.5:14b
Faster:     phi4:14b
```

### 🧠 **SPECIAL**
```
Math/Logic: deepseek-r1:14b
Images:     llava-llama3:8b
```

---

## Disk Space Saved

After removing those 5 models: **~22GB freed up**

Total optimized collection: **~58GB** for 8 high-quality local models

---

## For Your Tkinter Problem - Do This Now:

**Model:** `ollama run codestral:22b`

**Prompt 1:**
```
I need to integrate a tkinter Help popup into my program. 
First, review this popup code for best practices:

[paste your popup function here]

Is this implementation solid? Any improvements before I integrate it?
```

**Prompt 2 (after it responds):**
```
Here's my menu creation section (lines 115-145):

[paste just the menu-building code, ~30 lines]

Show me EXACTLY how to:
1. Add Help menu item
2. Connect it to the popup function
3. Any imports needed

Give me the complete modified menu section.
