context reminder:

win11 machine, ollama, 1030 now, 3060 coming

pre-existing models before changes bewlow:

speaking of losing context, i told you at the beginning of this session
i had ollama installled with thse models: The list:

Found 20 ollama active LLMs:

1\. tinyllama:latest

2\. qwen2.5:1.5b

3\. gemma2:2b

4\. phi3:mini

5\. qwen2.5-coder:1.5b

6\. gpt-oss:120b-cloud

7\. qwen3-coder:480b-cloud

8\. deepseek-v3.1:671b-cloud

9\. llava:13b

10\. kimi-k2-thinking:cloud

11\. minimax-m2:cloud

12\. glm-4.6:cloud

13\. notus:latest

14\. alfred:latest

15\. firefunction-v2:latest

16\. deepseek-r1:latest

17\. qwen3-coder:latest

18\. mistral:latest

19\. gemma3:4b

20\. gemma3:1b

MODELS TO USE UNTIL RTX 3060

On your GT 1030 1GB (CPU-based):

Best local models for actual work:

1.  ✅ phi3:mini (3.8B) - Best quality for CPU

2.  ✅ gemma3:4b (4B) - Good balance

3.  ✅ qwen2.5-coder:1.5b (1.5B) - Fast coding help

Skip these (too big for GT 1030):

- ❌ llava:13b - 13GB VRAM needed

- ❌ mistral:latest - 7B will be very slow

- ❌ notus, alfred, firefunction-v2 - all \~7B

Delete these (redundant/useless):

- ❌ tinyllama - too weak

- ❌ gemma3:1b, gemma2:2b - redundant with gemma3:4b

- ❌ qwen2.5:1.5b - you have the coder version

YOUR ACTUAL SETUP

What you have:

- ✅ Ollama server running at ollama.ldmathes.cc (remote host)

- ✅ All 20 models on that remote server

- ✅ Continue configured to use that remote Ollama

- ✅ Both local models AND cloud models on same server

The models:

LOCAL models (on your Ollama server):

- llama3.1:latest (default)

- qwen2.5-coder:1.5b (autocomplete)

- phi3:mini

- gemma3:4b, gemma3:1b

- mistral:latest

- deepseek-r1:latest

- qwen3-coder:latest

- firefunction-v2:latest

- alfred:latest, notus:latest

- llava:13b

- gemma2:2b, tinyllama:latest, qwen2.5:1.5b

CLOUD models (proxied through your Ollama server):

- kimi-k2-thinking:cloud ← This is what timed out!

- glm-4.6:cloud

- minimax-m2:cloud

- gpt-oss:120b-cloud

- deepseek-v3.1:671b-cloud

- qwen3-coder:480b-cloud

prevous recommendation:

name: My Config

version: 0.0.2

schema: v1

models:

\# ===== PRIMARY MODELS (Use these) =====

\# Best for large context work (128K) - USE THIS AS DEFAULT

\- name: Phi3 (128K Context)

provider: ollama

model: \"phi3:mini\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

contextLength: 131072 \# 128K tokens

default: true \# ← DEFAULT FOR CHAT

roles:

\- chat

capabilities:

\- tool_use

requestOptions:

timeout: 600000

keepAlive: 600000

\# Fast autocomplete (small context is fine)

\- name: Qwen Autocomplete

provider: ollama

model: \"qwen2.5-coder:1.5b\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

contextLength: 32768

roles:

\- autocomplete

requestOptions:

timeout: 300000

keepAlive: 300000

\# For code-specific work (good quality, 32K context)

\- name: Qwen3 Coder

provider: ollama

model: \"qwen3-coder:latest\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

contextLength: 32768

roles:

\- chat

\- edit

requestOptions:

timeout: 300000

keepAlive: 300000

\# ===== EMERGENCY CLOUD MODELS (Quota limited) =====

\- name: Kimi K2 (Cloud - Save for emergencies)

provider: ollama

model: \"kimi-k2-thinking:cloud\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

roles:

\- chat

requestOptions:

timeout: 600000

keepAlive: 600000

\# ===== FUTURE: After RTX 3060 arrives =====

\# Uncomment these after downloading:

\# - name: DeepSeek Coder V2 (128K, GPU)

\# provider: ollama

\# model: \"deepseek-coder-v2:16b\"

\# apiBase: <https://ollama.ldmathes.cc>

\# baseUrl: <https://ollama.ldmathes.cc>

\# contextLength: 131072

\# default: true

\# roles:

\# - chat

\# - edit

\# - name: Qwen2.5 Coder 14B (GPU)

\# provider: ollama

\# model: \"qwen2.5-coder:14b\"

\# apiBase: <https://ollama.ldmathes.cc>

\# baseUrl: <https://ollama.ldmathes.cc>

\# contextLength: 32768

\# roles:

\# - chat

\# - edit

present state of my configure.yaml

cat /Users/dennishmathes/.continue/config.yaml

name: My Config

version: 0.0.1

schema: v1

models:

\- name: Llama 3.1

provider: ollama

model: llama3.1:latest

apiBase: <http://ollama.ldmathes.cc:11434>

\# FIX 1: Explicitly set the base URL

baseUrl: <http://ollama.ldmathes.cc:11434>

\# FIX 2: Set as the default chat model

default: false

roles:

\- chat

\- edit

capabilities:

\- tool_use

\# FIX 3: Increase timeout/keepAlive for remote stability

requestOptions:

timeout: 300000

keepAlive: 300000

\- name: GLM 4.6 (Cloud)

provider: ollama

model: \"glm-4.6:cloud\"

\# point to the HTTPS host you provided (use default HTTPS port)

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

roles:

\- chat

\- edit

capabilities:

\- tool_use

\# Increase timeout for cloud model

requestOptions:

timeout: 300000

keepAlive: 300000

\# If your host requires an Authorization header, add it under headers

\# headers:

\# Authorization: \"Bearer \<YOUR_TOKEN_HERE\>\"

\# \-\-- Additional models imported from LLM/config-ai.yaml \-\--

\- name: MiniMax M2 (Cloud)

provider: ollama

model: \"minimax-m2:cloud\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

roles:

\- chat

requestOptions:

timeout: 300000

keepAlive: 300000

\- name: DeepSeek R1 (Reasoning)

provider: ollama

model: \"deepseek-r1:latest\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

roles:

\- chat

requestOptions:

timeout: 300000

keepAlive: 300000

\# Best for large context work (128K) - USE THIS AS DEFAULT

\- name: Phi3 (128K Context)

provider: ollama

model: \"phi3:mini\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

contextLength: 131072 \# 128K tokens

default: true \# ← DEFAULT FOR CHAT

roles:

\- chat

capabilities:

\- tool_use

requestOptions:

timeout: 600000

keepAlive: 600000

\# Fast autocomplete (small context is fine)

\- name: Qwen Autocomplete

provider: ollama

model: \"qwen2.5-coder:1.5b\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

contextLength: 32768

roles:

\- autocomplete

requestOptions:

timeout: 300000

keepAlive: 300000

\# For code-specific work (good quality, 32K context)

\- name: Qwen3 Coder

provider: ollama

model: \"qwen3-coder:latest\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

contextLength: 32768

roles:

\- chat

\- edit

requestOptions:

timeout: 300000

keepAlive: 300000

\# ===== EMERGENCY CLOUD MODELS (Quota limited) =====

\- name: Kimi K2 (Cloud - Save for emergencies)

provider: ollama

model: \"kimi-k2-thinking:cloud\"

apiBase: <https://ollama.ldmathes.cc>

baseUrl: <https://ollama.ldmathes.cc>

roles:

\- chat

requestOptions:

timeout: 600000

keepAlive: 600000

\# ===== FUTURE: After RTX 3060 arrives =====

\# Uncomment these after downloading:

\# - name: DeepSeek Coder V2 (128K, GPU)

\# provider: ollama

\# model: \"deepseek-coder-v2:16b\"

\# apiBase: <https://ollama.ldmathes.cc>

\# baseUrl: <https://ollama.ldmathes.cc>

\# contextLength: 131072

\# default: true

\# roles:

\# - chat

\# - edit

\# - name: Qwen2.5 Coder 14B (GPU)

\# provider: ollama

\# model: \"qwen2.5-coder:14b\"

\# apiBase: <https://ollama.ldmathes.cc>

\# baseUrl: <https://ollama.ldmathes.cc>

\# contextLength: 32768

\# roles:

\# - chat

\# - edit

my (still active) ollama models:

Found 21 ollama active LLMs:

1\. qwen2.5:7b

2\. tinyllama:latest

3\. qwen2.5:1.5b

4\. gemma2:2b

5\. phi3:mini

6\. qwen2.5-coder:1.5b

7\. gpt-oss:120b-cloud

8\. qwen3-coder:480b-cloud

9\. deepseek-v3.1:671b-cloud

10\. llava:13b

11\. kimi-k2-thinking:cloud

12\. minimax-m2:cloud

13\. glm-4.6:cloud

14\. notus:latest

15\. alfred:latest

16\. firefunction-v2:latest

17\. deepseek-r1:latest

18\. qwen3-coder:latest

19\. mistral:latest

20\. gemma3:4b

21\. gemma3:1b

reminder, i am on an old 2gig 1040 for a few more days, then a 12 gig
3060 comes \... looking to get configured properly for now (1040) \...
preping for teh 3060

\-\--

Answer

**IMMEDIATE CONFIG FIX + 3060 PREP**

Looking at your current setup, here\'s what needs to happen:

**CURRENT PROBLEMS**

1.  ❌ Your config has Phi3 as default (good!) but doesn\'t include some
    useful models

2.  ❌ You still have models you should delete (tinyllama, gemma3:1b,
    gemma2:2b, qwen2.5:1.5b)

3.  ⚠️ You added qwen2.5:7b (new model #1) - this is actually GOOD for
    CPU work!

4.  ✅ Config structure is correct

5.  ✅ Phi3 128K as default is perfect

**STEP 1: CLEAN UP MODELS (Do this now on Windows 11)**

powershell

*\# SSH to Windows 11 or run locally*

*\# Delete useless/redundant models:*

ollama rm tinyllama:latest

ollama rm qwen2.5:1.5b

ollama rm gemma2:2b

ollama rm gemma3:1b

ollama rm notus:latest

ollama rm alfred:latest

ollama rm firefunction-v2:latest

*\# Keep these (they\'re actually useful):*

*\# - qwen2.5:7b (NEW - good for CPU work!)*

*\# - phi3:mini (128K context)*

*\# - gemma3:4b (backup)*

*\# - qwen2.5-coder:1.5b (autocomplete)*

*\# - qwen3-coder:latest (if it\'s 14B or smaller)*

*\# - mistral:latest (7B backup)*

*\# - deepseek-r1:latest (reasoning)*

*\# - llava:13b (vision - will work after 3060)*

**STEP 2: UPDATED CONFIG FOR NOW (Use this immediately)**

Replace your entire \~/.continue/config.yaml with this:

yaml

name: My Config

version: 0.0.2

schema: v1

models:

*\# ========================================*

*\# PRIMARY MODELS (Current - GT 1040)*

*\# ========================================*

*\# Best for large context work (128K) - DEFAULT*

\- name: Phi3 (128K Context)

provider: ollama

model: \"phi3:mini\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 131072 *\# 128K tokens*

default: true *\# ← DEFAULT FOR CHAT*

roles:

\- chat

capabilities:

\- tool_use

requestOptions:

timeout: 600000

keepAlive: 600000

*\# Good quality 7B for general use (NEW!)*

\- name: Qwen2.5 7B (CPU)

provider: ollama

model: \"qwen2.5:7b\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 32768

roles:

\- chat

requestOptions:

timeout: 300000

keepAlive: 300000

*\# For code-specific work (good quality, 32K context)*

\- name: Qwen3 Coder

provider: ollama

model: \"qwen3-coder:latest\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 32768

roles:

\- chat

\- edit

requestOptions:

timeout: 300000

keepAlive: 300000

*\# Reasoning model*

\- name: DeepSeek R1 (Reasoning)

provider: ollama

model: \"deepseek-r1:latest\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 8192

roles:

\- chat

requestOptions:

timeout: 300000

keepAlive: 300000

*\# Backup models*

\- name: Mistral 7B

provider: ollama

model: \"mistral:latest\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 32768

roles:

\- chat

requestOptions:

timeout: 300000

keepAlive: 300000

\- name: Gemma3 4B

provider: ollama

model: \"gemma3:4b\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 8192

roles:

\- chat

requestOptions:

timeout: 300000

keepAlive: 300000

*\# ========================================*

*\# AUTOCOMPLETE (Fast, Small)*

*\# ========================================*

\- name: Qwen Autocomplete

provider: ollama

model: \"qwen2.5-coder:1.5b\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 32768

roles:

\- autocomplete

requestOptions:

timeout: 60000

keepAlive: 60000

*\# ========================================*

*\# CLOUD MODELS (Emergency Use Only)*

*\# ========================================*

\- name: Kimi K2 (Cloud - Quota Limited)

provider: ollama

model: \"kimi-k2-thinking:cloud\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

roles:

\- chat

requestOptions:

timeout: 600000

keepAlive: 600000

\- name: DeepSeek V3.1 (Cloud - Quota Limited)

provider: ollama

model: \"deepseek-v3.1:671b-cloud\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

roles:

\- chat

requestOptions:

timeout: 600000

keepAlive: 600000

\- name: Qwen3 Coder (Cloud - Quota Limited)

provider: ollama

model: \"qwen3-coder:480b-cloud\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

roles:

\- chat

\- edit

requestOptions:

timeout: 600000

keepAlive: 600000

\- name: GLM 4.6 (Cloud - Quota Limited)

provider: ollama

model: \"glm-4.6:cloud\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

roles:

\- chat

requestOptions:

timeout: 600000

keepAlive: 600000

*\# ========================================*

*\# FUTURE: After RTX 3060 arrives*

*\# ========================================*

*\# Uncomment these after downloading on Windows 11:*

*\# - name: Qwen2.5 Coder 14B (Primary GPU)*

*\# provider: ollama*

*\# model: \"qwen2.5-coder:14b\"*

*\# apiBase: https://ollama.ldmathes.cc*

*\# baseUrl: https://ollama.ldmathes.cc*

*\# contextLength: 32768*

*\# default: true \# ← Make this default after 3060*

*\# roles:*

*\# - chat*

*\# - edit*

*\# requestOptions:*

*\# timeout: 300000*

*\# keepAlive: 300000*

*\# - name: DeepSeek Coder V2 16B (Large Context GPU)*

*\# provider: ollama*

*\# model: \"deepseek-coder-v2:16b\"*

*\# apiBase: https://ollama.ldmathes.cc*

*\# baseUrl: https://ollama.ldmathes.cc*

*\# contextLength: 131072 \# 128K tokens*

*\# roles:*

*\# - chat*

*\# - edit*

*\# requestOptions:*

*\# timeout: 600000*

*\# keepAlive: 600000*

*\# - name: Qwen2.5 14B (General GPU)*

*\# provider: ollama*

*\# model: \"qwen2.5:14b\"*

*\# apiBase: https://ollama.ldmathes.cc*

*\# baseUrl: https://ollama.ldmathes.cc*

*\# contextLength: 32768*

*\# roles:*

*\# - chat*

*\# requestOptions:*

*\# timeout: 300000*

*\# keepAlive: 300000*

*\# - name: DeepSeek R1 14B (Reasoning GPU)*

*\# provider: ollama*

*\# model: \"deepseek-r1:14b\"*

*\# apiBase: https://ollama.ldmathes.cc*

*\# baseUrl: https://ollama.ldmathes.cc*

*\# contextLength: 8192*

*\# roles:*

*\# - chat*

*\# requestOptions:*

*\# timeout: 300000*

*\# keepAlive: 300000*

*\# - name: Qwen2.5 Coder 7B (Fast GPU)*

*\# provider: ollama*

*\# model: \"qwen2.5-coder:7b\"*

*\# apiBase: https://ollama.ldmathes.cc*

*\# baseUrl: https://ollama.ldmathes.cc*

*\# contextLength: 32768*

*\# roles:*

*\# - chat*

*\# - edit*

*\# requestOptions:*

*\# timeout: 300000*

*\# keepAlive: 300000*

**STEP 3: TEST YOUR CURRENT SETUP**

bash

*\# On MacBook Air*

cn

*\# Should show: \"Agent: My Config Model: Phi3 (128K Context)\"*

*\# Test it*

\> Hello, what\'s your context window?

*\# Should respond with 128K tokens*

*\# Test with files*

\> \@ui_components.py

\> Summarize this file

*\# Should work without timeout*

**STEP 4: AFTER RTX 3060 ARRIVES (Day 1)**

**On Windows 11:**

powershell

*\# 1. Install RTX 3060, drivers, CUDA (per the guide)*

*\# 2. Verify GPU is working*

nvidia-smi

*\# 3. Download 14B models (Priority order)*

ollama pull qwen2.5-coder:14b *\# PRIMARY - Best for coding*

ollama pull deepseek-coder-v2:16b *\# SECONDARY - Large context*

ollama pull qwen2.5:14b *\# TERTIARY - General use*

ollama pull deepseek-r1:14b *\# REASONING - Complex problems*

ollama pull qwen2.5-coder:7b *\# FAST - Quick queries*

*\# 4. Test they work*

ollama run qwen2.5-coder:14b

\> Write a Python function to sort a list

\> exit

*\# 5. Check GPU usage while running*

nvidia-smi

*\# Should show 8-9GB VRAM used, high GPU utilization*

**On MacBook Air:**

bash

*\# Edit config*

nano \~/.continue/config.yaml

*\# Uncomment the RTX 3060 section*

*\# Change default from Phi3 to Qwen2.5 Coder 14B:*

*\# Find this line:*

*\# default: true \# ← Make this default after 3060*

*\# Uncomment it*

*\# Comment out Phi3 as default:*

*\# - name: Phi3 (128K Context)*

*\# default: false \# ← Change to false*

*\# Save and restart Continue*

cn

*\# Should now show: \"Agent: My Config Model: Qwen2.5 Coder 14B
(Primary GPU)\"*

*\# Test speed*

\> Write a Python function to calculate fibonacci

*\# Should stream FAST (25-30 tok/s vs 3-5 tok/s before)*

**YOUR MODEL LINEUP SUMMARY**

**NOW (GT 1040 - CPU):**

1.  **Default:** Phi3:mini (128K context, 3.8B)

2.  **Coding:** Qwen3-coder:latest (check size)

3.  **General:** Qwen2.5:7b (good quality)

4.  **Reasoning:** DeepSeek-R1:latest

5.  **Backup:** Mistral:latest, Gemma3:4b

6.  **Autocomplete:** qwen2.5-coder:1.5b

7.  **Emergency:** Cloud models (quota limited)

**AFTER 3060 (GPU):**

1.  **Default:** qwen2.5-coder:14b (PRIMARY)

2.  **Large context:** deepseek-coder-v2:16b (128K tokens)

3.  **Fast:** qwen2.5-coder:7b (40+ tok/s)

4.  **General:** qwen2.5:14b

5.  **Reasoning:** deepseek-r1:14b

6.  **Vision:** llava:13b (will finally work!)

7.  **Backup:** Phi3, Mistral, Gemma3:4b

8.  **Autocomplete:** qwen2.5-coder:1.5b

9.  **Emergency:** Cloud models (rarely needed)

**PERFORMANCE EXPECTATIONS**

**Current (GT 1040 CPU):**

- Phi3:mini: 3-5 tok/s

- Qwen2.5:7b: 2-4 tok/s (slower, better quality)

- Qwen3-coder: 3-5 tok/s

- Response time: 20-40 seconds

**After RTX 3060:**

- Qwen2.5-coder:14b: 25-30 tok/s

- DeepSeek-coder-v2:16b: 20-25 tok/s

- Qwen2.5-coder:7b: 40-45 tok/s

- Response time: 3-6 seconds

- **8-10x faster!**

**FINAL CHECKLIST**

**Do NOW (before 3060):**

- Delete useless models (tinyllama, gemma3:1b, etc.)

- Update config.yaml with version above

- Test cn shows Phi3 as default

- Test \@files work without timeout

- Save config backup

**Do DAY 1 (after 3060 install):**

- Install RTX 3060 hardware

- Install NVIDIA drivers

- Verify nvidia-smi works

- Download qwen2.5-coder:14b

- Download deepseek-coder-v2:16b

- Download qwen2.5:14b

- Download deepseek-r1:14b

- Uncomment GPU models in config.yaml

- Change default to qwen2.5-coder:14b

- Test speed improvement

- Verify GPU usage with nvidia-smi

**QUICK REFERENCE**

**Current usage pattern:**

bash

cn

*\# Uses: Phi3 (128K context)*

*\# Speed: 3-5 tok/s*

*\# Quality: Good (3.8B)*

*\# Quota: Unlimited*

**After 3060 usage pattern:**

bash

cn

*\# Uses: Qwen2.5-coder:14b*

*\# Speed: 25-30 tok/s (8x faster!)*

*\# Quality: Excellent (14B)*

*\# Quota: Unlimited*

**ANSWER**

**IMMEDIATE CONFIG FIX + 3060 PREP**

Looking at your current setup, here\'s what needs to happen:

**CURRENT PROBLEMS**

1.  ❌ Your config has Phi3 as default (good!) but doesn\'t include some
    useful models

2.  ❌ You still have models you should delete (tinyllama, gemma3:1b,
    gemma2:2b, qwen2.5:1.5b)

3.  ⚠️ You added qwen2.5:7b (new model #1) - this is actually GOOD for
    CPU work!

4.  ✅ Config structure is correct

5.  ✅ Phi3 128K as default is perfect

**STEP 1: CLEAN UP MODELS (Do this now on Windows 11)**

\# SSH to Windows 11 or run locally

\# Delete useless/redundant models:

ollama rm tinyllama:latest

ollama rm qwen2.5:1.5b

ollama rm gemma2:2b

ollama rm gemma3:1b

ollama rm notus:latest

ollama rm alfred:latest

ollama rm firefunction-v2:latest

\# Keep these (they\'re actually useful):

\# - qwen2.5:7b (NEW - good for CPU work!)

\# - phi3:mini (128K context)

\# - gemma3:4b (backup)

\# - qwen2.5-coder:1.5b (autocomplete)

\# - qwen3-coder:latest (if it\'s 14B or smaller)

\# - mistral:latest (7B backup)

\# - deepseek-r1:latest (reasoning)

\# - llava:13b (vision - will work after 3060)

**STEP 2: UPDATED CONFIG FOR NOW (Use this immediately)**

Replace your entire \~/.continue/config.yaml with this:

(redacted, updated later)

**AH! The Phi3 tool_use capability bug!**

This is a common issue - Phi3:mini doesn\'t actually support the
tool_use capability, but your config declares it does.

**IMMEDIATE FIX**

Edit your \~/.continue/config.yaml and find the Phi3 section:

\# Make Qwen3-coder the default instead

\- name: Qwen3 Coder

provider: ollama

model: \"qwen3-coder:latest\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 32768

default: true \# ← ADD THIS

roles:

\- chat

\- edit

capabilities:

\- tool_use \# Qwen DOES support tools

requestOptions:

timeout: 300000

keepAlive: 300000

\# Keep Phi3 but not as default

\- name: Phi3 (128K Context)

provider: ollama

model: \"phi3:mini\"

apiBase: https://ollama.ldmathes.cc

baseUrl: https://ollama.ldmathes.cc

contextLength: 131072

default: false \# ← CHANGE THIS

roles:

\- chat

\# No capabilities section

requestOptions:

timeout: 600000

keepAlive: 600000

TEST

**STEP 4: AFTER RTX 3060 ARRIVES (Day 1)**

**On Windows 11:**

\# 1. Install RTX 3060, drivers, CUDA (per the guide)

\# 2. Verify GPU is working

nvidia-smi

\# 3. Download 14B models (Priority order)

ollama pull qwen2.5-coder:14b \# PRIMARY - Best for coding

ollama pull deepseek-coder-v2:16b \# SECONDARY - Large context

ollama pull qwen2.5:14b \# TERTIARY - General use

ollama pull deepseek-r1:14b \# REASONING - Complex problems

ollama pull qwen2.5-coder:7b \# FAST - Quick queries

\# 4. Test they work

ollama run qwen2.5-coder:14b

\> Write a Python function to sort a list

\> exit

\# 5. Check GPU usage while running

nvidia-smi

\# Should show 8-9GB VRAM used, high GPU utilization

On MacBook Air:

\# Edit config

nano \~/.continue/config.yaml

\# Uncomment the RTX 3060 section

\# Change default from Phi3 to Qwen2.5 Coder 14B:

\# Find this line:

\# default: true \# ← Make this default after 3060

\# Uncomment it

\# Comment out Phi3 as default:

\# - name: Phi3 (128K Context)

\# default: false \# ← Change to false

\# Save and restart Continue

cn

\# Should now show: \"Agent: My Config Model: Qwen2.5 Coder 14B (Primary
GPU)\"

\# Test speed

\> Write a Python function to calculate fibonacci

\# Should stream FAST (25-30 tok/s vs 3-5 tok/s before)

**YOUR MODEL LINEUP SUMMARY**

**NOW (GT 1040 - CPU):**

1.  **Default:** Phi3:mini (128K context, 3.8B)

2.  **Coding:** Qwen3-coder:latest (check size)

3.  **General:** Qwen2.5:7b (good quality)

4.  **Reasoning:** DeepSeek-R1:latest

5.  **Backup:** Mistral:latest, Gemma3:4b

6.  **Autocomplete:** qwen2.5-coder:1.5b

7.  **Emergency:** Cloud models (quota limited)

**AFTER 3060 (GPU):**

1.  **Default:** qwen2.5-coder:14b (PRIMARY)

2.  **Large context:** deepseek-coder-v2:16b (128K tokens)

3.  **Fast:** qwen2.5-coder:7b (40+ tok/s)

4.  **General:** qwen2.5:14b

5.  **Reasoning:** deepseek-r1:14b

6.  **Vision:** llava:13b (will finally work!)

7.  **Backup:** Phi3, Mistral, Gemma3:4b

8.  **Autocomplete:** qwen2.5-coder:1.5b

9.  **Emergency:** Cloud models (rarely needed)

**PERFORMANCE EXPECTATIONS**

**Current (GT 1040 CPU):**

- Phi3:mini: 3-5 tok/s

- Qwen2.5:7b: 2-4 tok/s (slower, better quality)

- Qwen3-coder: 3-5 tok/s

- Response time: 20-40 seconds

**After RTX 3060:**

- Qwen2.5-coder:14b: 25-30 tok/s

- DeepSeek-coder-v2:16b: 20-25 tok/s

- Qwen2.5-coder:7b: 40-45 tok/s

- Response time: 3-6 seconds

- **8-10x faster!**

**FINAL CHECKLIST**

**Do NOW (before 3060):**

- Delete useless models (tinyllama, gemma3:1b, etc.)

- Update config.yaml with version above

- Test cn shows Phi3 as default

- Test \@files work without timeout

- Save config backup

**Do DAY 1 (after 3060 install):**

- Install RTX 3060 hardware

- Install NVIDIA drivers

- Verify nvidia-smi works

- Download qwen2.5-coder:14b

- Download deepseek-coder-v2:16b

- Download qwen2.5:14b

- Download deepseek-r1:14b

- Uncomment GPU models in config.yaml

- Change default to qwen2.5-coder:14b

- Test speed improvement

- Verify GPU usage with nvidia-smi
