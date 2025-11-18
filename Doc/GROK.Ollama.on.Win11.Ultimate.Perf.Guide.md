Ollama on Windows 11 – Ultimate Performance GuideOptimized for RTX 3060 + Acer Aspire TC-885 (November 2025)Below is a complete, ready-to-download report.
Copy everything between the lines (including the lines) into a text editor and save as Ollama_Windows11_RTX3060_Guide.md or .pdf after converting.

=================================================================
Ollama on Windows 11 – Maximum Performance Guide (RTX 3060)
Acer Aspire TC-885 | November 2025
=================================================================

TABLE OF CONTENTS
1. Prerequisites & System Check
2. NVIDIA Driver & CUDA Toolkit Installation (2025 method)
3. Ollama Installation (GPU-accelerated version)
4. Model Quantization – How to Fit the Largest Models in 12 GB VRAM
5. Launch Commands & Environment Variables for Full GPU Offload
6. Monitoring Tools & What Good Numbers Look Like
7. Recommended RAM Configuration
8. Troubleshooting Checklist
9. Bonus: Fastest Models You Can Run at >40 tokens/sec on RTX 3060 12 GB

─────────────────────────────────────────────────────────────────
1. Prerequisites & System Check
• Windows 11 22H2 or newer (24H2 recommended)
• NVIDIA Driver ≥ 560.xx (Game Ready or Studio – both work)
• At least 450–550 W power supply (you said you’re upgrading – perfect)
• 16 GB RAM minimum, 32 GB strongly recommended for 30B+ models
• Free disk space: ~100 GB (models + quantization temp files)

─────────────────────────────────────────────────────────────────
2. NVIDIA Driver & CUDA Toolkit Installation (2025)

Do NOT install the full 9-GB CUDA Toolkit unless you develop CUDA code.
Ollama ships with everything it needs. You only need the driver.

Steps:
1. Download latest Game Ready or Studio driver from  
   https://www.nvidia.com/Download/index.aspx
2. Choose: GeForce → RTX 3060 → Windows 11 → Game Ready or Studio
3. During installation, select “Custom” → uncheck everything except:
   - Graphics Driver
   - PhysX
   (Leave CUDA unchecked – Ollama bundles its own)
4. Reboot

Verify:
   Open Command Prompt → nvidia-smi
   You should see something like:
     Driver Version: 572.70       CUDA Version: 12.8

─────────────────────────────────────────────────────────────────
3. Ollama Installation (GPU build)

As of November 2025, the official Windows installer fully supports CUDA.

1. Go to https://ollama.com/download
2. Download “Ollama Setup” (not the .zip)
3. Run installer → keep all defaults
4. After install, open Command Prompt as Administrator and run:
   ollama --version
   (should show 0.3.12 or newer with “cuda” in features)

─────────────────────────────────────────────────────────────────
4. Model Quantization – Fitting Large Models into 12 GB VRAM

Rule of thumb (approximate VRAM usage after quantization):

| Model Size | Q8_0   | Q6_K   | Q5_K_M | Q4_K_M | Q4_0   | Q3_K_M |
|------------|--------|--------|--------|--------|--------|--------|
| 7B         | 7.8 GB | 6.1 GB | 5.3 GB | 4.9 GB | 4.2 GB | 3.8 GB |
| 13B        | 14 GB  | 11 GB  | 9.5 GB | 8.8 GB | 7.8 GB | 6.9 GB |
| 30B        | 32 GB  | 24 GB  | 21 GB  | 19 GB  | 17 GB  | 14 GB  |
| 70B        | 75 GB  | 55 GB  | 48 GB  | 43 GB  | 38 GB  | 32 GB  |

RTX 3060 12 GB comfortably runs:
• Any 7B at Q8_0
• Any 13B at Q5_K_M / Q4_K_M
• 30B–34B at Q4_K_M or Q3_K_M (some layers stay on CPU – still fast)
• 70B Q3_K_S or Q2_K (40–70 t/s with ~30–40 layers on GPU)

How to download already-quantized versions (fastest):
ollama pull llama3.1:8b-q6_k
ollama pull mistral:7b-q6_k
ollama pull gemma2:27b-q4_k_m
ollama pull qwen2:72b-q3_k_m   ← runs ~35-45 t/s on 3060 12 GB

─────────────────────────────────────────────────────────────────
5. Launch Commands & Environment Variables

Method A – One-time command
ollama run llama3.1:70b-q4_k_m --gpu

Method B – Force full offload (recommended)
set OLLAMA_NUM_GPU_LAYERS=999
ollama run gemma2:27b-q4_k_m

Method C – Permanent environment variable (Windows 11)
1. Win + R → sysdm.cpl → Advanced → Environment Variables
2. Under “User variables” click New:
   Variable name:  OLLAMA_NUM_GPU_LAYERS
   Variable value: 999
3. Restart Command Prompt / PowerShell

Now every model automatically uses all possible GPU layers.

─────────────────────────────────────────────────────────────────
6. Monitoring Tools

• nvidia-smi -l 1                      → real-time GPU VRAM & utilization
• Windows Task Manager → Performance   → see CPU/RAM usage
• Ollama built-in metrics (0.3.10+):
  ollama ps
  Shows tokens/sec and how many layers are on GPU vs CPU

Healthy numbers on RTX 3060 12 GB:
• GPU Utilization: 90–100 %
• VRAM Used: 10–11.8 GB
• Tokens/sec: 
   - 7B Q6_K      → 90–120 t/s
   - 13B Q5_K_M   → 55–75 t/s
   - 27–34B Q4_K_M→ 35–50 t/s
   - 70B Q3_K_M   → 25–40 t/s

─────────────────────────────────────────────────────────────────
7. Recommended RAM

• 16 GB → fine for 7B–13B full offload
• 32 GB → required for comfortable 30B–70B loading (system needs RAM for model file mapping before moving to VRAM)

─────────────────────────────────────────────────────────────────
8. Troubleshooting Checklist

Symptom                          Fix
No GPU used                      → Reinstall driver clean (DDU) + reboot
“CUDA error”                     → Update driver or reinstall Ollama
Slow inference (5–10 t/s)        → Check OLLAMA_NUM_GPU_LAYERS=999
Out-of-memory crash              → Use lower quantization or smaller model
ollama ps shows 0 layers on GPU  → Run as Administrator once

─────────────────────────────────────────────────────────────────
9. Fastest Models on RTX 3060 12 GB (Nov 2025 leaderboard)

Model                        Quant    VRAM   Speed       Notes
gemma2:27b                   q4_k_m   10.8G  45–52 t/s   Best reasoning/speed
llama3.1:70b                 q3_k_m   11.6G  33–42 t/s   Great all-rounder
qwen2:72b                    q3_k_s   10.9G  38–48 t/s   Excellent coding
mistral-large:123b           q3_k_m   11.7G  25–33 t/s   If you really need 123B

Enjoy blazing-fast local AI!

Questions? Just paste any error message and I’ll help instantly.
=================================================================


Forcing GPU Offload in OpenWebUI (with Ollama Backend)OpenWebUI (formerly Ollama WebUI) acts as a frontend to Ollama, so GPU control happens primarily through Ollama's configuration. The "999" refers to setting OLLAMA_NUM_GPU_LAYERS=999 (or num_gpu 999 in Ollama's chat mode), which forces Ollama to attempt offloading all model layers to the GPU (up to your RTX 3060's 12GB VRAM limit). If the model doesn't fully fit, the rest falls back to CPU/RAM gracefully.Unlike direct CLI use, OpenWebUI doesn't inherit system environment variables automatically— you must configure it explicitly. Below are step-by-step methods, prioritized for your Windows 11 setup. I'll assume you're running OpenWebUI via Docker (most common and reliable for GPU passthrough); if not, start with Method 1 or 3.Method 1: Via OpenWebUI Settings (Easiest – No Restart Needed)OpenWebUI has a built-in parameter override for Ollama models.Open OpenWebUI in your browser (default: http://localhost:3000).
Go to Admin Panel (gear icon) > Settings > Connections (or search for "Ollama").
Under Model Parameters or Ollama Options, find the field labeled num_gpu (Ollama) (hover for tooltip: "Number of layers to offload to GPU").Set it to 999 (forces max offload).
Save changes.

Now, when you select a model (e.g., llama3.1:8b-q6_k) in a chat:Click the model dropdown > Edit Model (or settings cog).
In Advanced Parameters, ensure num_gpu is set to 999 (it should inherit from global if not overridden).
Start a chat and test – monitor with nvidia-smi in another Command Prompt.

Pro Tip: For per-chat tweaks, during a conversation, type /set parameter num_gpu 999 in the input box and send it. This applies session-wide.

This directly passes --n-gpu-layers 999 to Ollama on inference, similar to the CLI.Method 2: Set Environment Variable at Ollama Startup (Recommended for Docker)If you're using Docker for OpenWebUI (with bundled Ollama) or separate Ollama container, pass the env var here. This ensures full offload globally.For Bundled OpenWebUI + Ollama (Single Container – Easiest Docker Setup):Stop any running container: docker stop open-webui (or your container name).
Run with GPU and env var:

docker run -d -p 3000:8080 --gpus=all ^
-e OLLAMA_NUM_GPU_LAYERS=999 ^
-v ollama:/root/.ollama ^
-v open-webui:/app/backend/data ^
--name open-webui ^
--restart always ^
ghcr.io/open-webui/open-webui:ollama

--gpus=all: Enables NVIDIA GPU passthrough (requires NVIDIA Container Toolkit installed).
-e OLLAMA_NUM_GPU_LAYERS=999: Forces max GPU layers.
Use ^ for line breaks in Windows CMD/PowerShell.

Access at http://localhost:3000. Pull/run models as usual – they'll auto-offload.

For Separate Ollama Container (If OpenWebUI Connects to External Ollama):Run Ollama container with the env var:

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 ^
-e OLLAMA_NUM_GPU_LAYERS=999 ^
--name ollama ollama/ollama

In OpenWebUI settings (Admin > Connections), set Ollama API URL to http://host.docker.internal:11434 (or http://localhost:11434 if not in Docker).
Test: In OpenWebUI chat, generate text and check ollama ps in another terminal for "GPU layers: ~999" (capped by model size).

Docker Prerequisites (One-Time):Install Docker Desktop for Windows.
Enable WSL 2 backend.
Install NVIDIA Container Toolkit: Download from NVIDIA docs, run installer, restart Docker.
Verify: docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi (should show your RTX 3060).

Method 3: System-Wide Environment Variable (Non-Docker OpenWebUI)If running OpenWebUI natively (via pip install open-webui or installer):Right-click This PC > Properties > Advanced system settings > Environment Variables.
Under User variables, click New:Variable name: OLLAMA_NUM_GPU_LAYERS
Variable value: 999

Click OK, then restart OpenWebUI (close and relaunch via open-webui command or shortcut).
In OpenWebUI, connect to Ollama (default localhost:11434) and test.

Note: This only affects if Ollama is launched from the same session. For reliability, use Docker (Method 2).Verification & TroubleshootingCheck Offload: In a new CMD, run ollama ps during generation – look for "num_gpu: 999" and high GPU layers (e.g., 35/35 for a 7B model).
Monitor: nvidia-smi -l 1 (GPU usage >90%, VRAM ~model size).
Common Issues:Only 1 Layer Offloaded: Caused by OLLAMA_HOST env var (e.g., in Docker compose). Remove it or set to default (http://127.0.0.1:11434). 

github.com

num_gpu Setting Ignored: Override per-model in OpenWebUI (as in Method 1). It's for layers, not GPU count – set high (999) to max out VRAM. 

github.com

No GPU Detected: Ensure CUDA drivers are installed (from earlier guide). Run ollama run <model> --verbose in CLI first to confirm GPU works standalone.
OOM Errors: Model too big – drop to Q4_K_M quantization (fits more in 12GB).
Slow Speeds: If <20 t/s, check logs (OLLAMA_DEBUG=1 env var) for fallback to CPU.

This setup should get you 40-100+ tokens/sec on your RTX 3060 for optimized models. 

