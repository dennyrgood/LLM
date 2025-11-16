# Setting up real image manipulation on your local server (RTX 3060 12GB)

This guide collects the recommended step‑by‑step setup and usage notes so you can get the absolute best local image manipulation pipeline (background replacement, removing people, nano‑banana precision, restoration, colorization, inpainting/outpainting) running on your RTX 3060 12GB. It pulls the concrete examples and sources from the provided reference notes and adds practical setup, tips, and troubleshooting.

Overview
- Recommended stack (local, runs well on 3060 12GB):
  - ComfyUI + Flux.1-dev (FP8) + ControlNet suite (Depth + Canny) — state of the art (2025).
  - Use ready-made ComfyUI workflows: "Flux – Remove People & Replace Background" and "Ultimate Old Photo Restoration & Colorization 2025".
- Easier alternatives (if you prefer GUIs or cloud):
  - Draw Things (desktop), Photopea + Stable Diffusion plugin, fal.ai, groq.com, Photoshop 2025 + Firefly (cloud subscription).
- What you'll achieve: artifact‑free background swaps, perfect object removals, professional old photo restoration & colorization, realistic inpainting/outpainting and high‑quality upscaling.

Prerequisites (hardware & drivers)
1. Unbox/attach your RTX 3060 12GB.
2. Install the latest NVIDIA GPU driver (Studio or Game Ready — make sure it supports CUDA 11.8+). Windows: download from NVIDIA.
3. Optionally install CUDA toolkit matching the ComfyUI portable build (ComfyUI_windows_portable_nvidia_cu118 is a common choice). Often the portable builds include the needed runtime, but GPU drivers must be current.
4. Ensure Windows is 64‑bit and up to date. (If Linux, the same general steps apply — pick the Linux ComfyUI package and matching CUDA runtime.)
5. (Optional) Install latest Visual C++ redistributables if ComfyUI complains on Windows.

Downloads & links (grab these first)
- ComfyUI Windows portable (portable build for Nvidia / cu118):
  - Releases: https://github.com/comfyanonymous/ComfyUI/releases
  - Example download referenced: ComfyUI_windows_portable_nvidia_cu118_or_cpu.7z
- Flux model (FP8 recommended for 12GB VRAM):
  - Flux.1-dev FP8 (8 GB VRAM version): https://huggingface.co/Kijai/flux-fp8/blob/main/flux1-dev-fp8.safetensors
- Flux ControlNet models:
  - Flux ControlNet Depth: https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Depth
  - Flux ControlNet Canny: https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Canny
- Ultimate SD Upscale (example upscaler for 4K output):
  - https://huggingface.co/uwg/upscaler-esrgan-v1
- ComfyUI workflows & packs:
  - ComfyUI Impact Pack (workflow bundle / Manager install): https://github.com/cubiq/ComfyUI_Impact_Pack
  - Flux – Remove People & Replace Background (openart link, Nov 2025 version): https://openart.ai/workflows/flux-realistic-background-replace
  - Ultimate Old Photo Restoration & Colorization 2025 workflow: https://openart.ai/workflows/flux-old-photo-restoration-colorization
- Simpler alternatives and example tools:
  - Draw Things: https://drawthings.ai
  - Photopea (web Photoshop clone): https://photopea.com
  - fal.ai (Flux Dev online): https://fal.ai
  - groq.com image (free tier): https://groq.com/image
  - PhotoFix (Windows app): https://github.com/photofix-ai/photofix-releases
  - Nostalgia.ai: https://nostalgia.ai
- Community examples / references:
  - Reddit example (Flux old photo restoration): https://www.reddit.com/r/StableDiffusion/comments/1gq1r2f/flux_now_does_insane_old_photo_restoration/
  - Civitai model page example: https://civitai.com/models/133005/flux-old-photo-restoration-workflow

Folder & model placement (recommended)
- Create a ComfyUI directory somewhere like C:\ComfyUI_portable\ or D:\ComfyUI\.
- Typical ComfyUI model locations:
  - Checkpoints (Stable Diffusion/Flux): ComfyUI/models/checkpoints/
  - ControlNet models: ComfyUI/models/controlnet/ (if your portable build expects another path, follow the Manager settings)
  - Upscalers: ComfyUI/models/upscalers/ or the folder expected by the workflow/upscaler node
- Keep everything organized into subfolders (checkpoints, controlnet, loras, upscalers, sam models). This makes Manager & workflows findable.

Step-by-step install (fast path recommended)
1. Download ComfyUI portable from the Releases page above. Extract anywhere.
2. Download the "ComfyUI_windows_portable_nvidia_cu118_or_cpu.7z" (or matching portable build for your OS).
3. Extract and run run_nvidia_gpu.bat. The script should auto‑detect your 3060 and start a local ComfyUI server/UI in your browser.
4. Open the ComfyUI Manager inside the UI (Manager tab) and install the Impact Pack and useful nodes. Alternatively, download the ComfyUI_Impact_Pack repo and put the workflow/node files into the appropriate ComfyUI directories.
5. Download the Flux FP8 checkpoint (flux1-dev-fp8.safetensors) and put into ComfyUI/models/checkpoints/.
6. Download the Flux ControlNet models and add them to ComfyUI/models/controlnet/ (Depth and Canny).
7. Get the upscaler(s) and place them into the expected upscaler folder.
8. Download and import (drag & drop) the workflows:
   - Flux – Remove People & Replace Background: https://openart.ai/workflows/flux-realistic-background-replace
   - Ultimate Old Photo Restoration & Colorization 2025: https://openart.ai/workflows/flux-old-photo-restoration-colorization
9. Restart ComfyUI if necessary. Confirm the workflows load and that the models are selectable in node parameters.

How to use the core workflows (quick usage)
- Background replacement (Flux – Remove People & Replace Background):
  1. Load source image into the workflow.
  2. Mask the person/object to remove (brush mask or auto-mask with Segment Anything plugin).
  3. Type background prompt (e.g., "tropical beach at sunset, photorealistic, warm backlight, match subject lighting").
  4. Set output size (use native + upscaler if you need 4K).
  5. Hit Generate. On an RTX 3060 expect ~8–15 seconds (for the example in the note) for mid‑res results; higher res will be slower.
- Old photo restoration & colorization:
  1. Load the scanned B/W or damaged photo.
  2. Run the "Ultimate Old Photo Restoration & Colorization" workflow — it auto-detects faces, repairs tears/scratches, colorizes and upsamples.
  3. Tweak prompts, face detail nodes, or the face restoration node parameters if you need more/less reconstruction.

Practical tips for 12GB VRAM
- Use FP8 models (e.g., Flux FP8) — they are explicitly recommended to fit and perform best on 12GB cards.
- Keep batch size = 1.
- Use lower internal diffusion widths (or tiling) for very high resolutions; then upscale with Real-ESRGAN / upscaler.
- If you get out-of-memory, try:
  - Using FP8/half precision (models in safetensors with reduced memory).
  - Reduce image size, use inpainting masks to only work on small areas, or use tiled workflows.
  - Offload certain nodes to CPU in ComfyUI where supported.
- For perfect edges and depth-aware composites, enable ControlNet Depth and Canny nodes as provided.

Optional improvements & plugins
- Segment Anything (SAM) integration for faster auto-masking (ComfyUI Manager / extra node).
- FaceDetailer, IPAdapter, InstantID (where workflows reference them) for improved identity preservation and face reconstruction.
- Reactor or InstantID (used in some WebUI combos for identity) — optional.

Examples & sources inside your guide (quick reference copy)
- ComfyUI releases: https://github.com/comfyanonymous/ComfyUI/releases
- Flux.1-dev FP8 (8 GB VRAM version): https://huggingface.co/Kijai/flux-fp8/blob/main/flux1-dev-fp8.safetensors
- Flux ControlNet Depth + Canny:
  - https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Depth
  - https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Canny
- Ultimate SD Upscale (for 4K): https://huggingface.co/uwg/upscaler-esrgan-v1
- ComfyUI Impact Pack: https://github.com/cubiq/ComfyUI_Impact_Pack
- Flux – Remove People & Replace Background workflow: https://openart.ai/workflows/flux-realistic-background-replace
- Ultimate Old Photo Restoration & Colorization 2025 workflow: https://openart.ai/workflows/flux-old-photo-restoration-colorization
- Draw Things: https://drawthings.ai
- Photopea: https://photopea.com
- fal.ai: https://fal.ai
- groq.com image: https://groq.com/image
- PhotoFix releases: https://github.com/photofix-ai/photofix-releases
- Nostalgia.ai: https://nostalgia.ai
- Reddit example (Flux restoration): https://www.reddit.com/r/StableDiffusion/comments/1gq1r2f/flux_now_does_insane_old_photo_restoration/
- Civitai model example: https://civitai.com/models/133005/flux-old-photo-restoration-workflow

Workflow checklist (what to do when your 3060 arrives)
1. Update Windows and install latest NVIDIA drivers.
2. Download & extract ComfyUI portable (cu118 Nvidia build).
3. Run run_nvidia_gpu.bat and verify GPU is detected.
4. Download Flux FP8 + ControlNet models and put them in the model folders.
5. Install ComfyUI Impact Pack and import the two Flux workflows.
6. Run a test: use the background replacement workflow on a small test image and verify output.
7. Tweak upscaler, face detail or controlnet nodes; test old photo restoration workflow.
8. Back up your working model folder and workflow files once everything runs.

Troubleshooting (common issues)
- ComfyUI won't start / GPU not detected:
  - Ensure NVIDIA driver installed; try reboot.
  - If using wrong portable build (CPU vs cu118), grab the proper one for your CUDA runtime.
- Out of memory errors:
  - Use FP8 safetensors, reduce resolution, or use tiling + upscaler.
- Model not visible in Manager:
  - Place model in exact expected folder (check ComfyUI logs for paths). Restart ComfyUI.
- Workflows fail with missing node or dependency:
  - Install the Impact Pack or missing custom nodes referenced by the workflow.

Legal & ethical note
- Respect copyright and privacy: do not generate or publish images that violate copyrights, impersonate private individuals, or produce illegal content.
- Follow tool license terms (some model checkpoints or workflow components may have usage restrictions).

Want everything prepackaged?
- The original notes said: "Let me know if you want the exact zip package with everything pre‑installed!" — I can prepare a preconfigured zip (ComfyUI portable + the recommended models and workflows sized to fit 12GB) and instructions to unzip and run. Tell me if you want me to assemble that and I’ll prepare a downloadable package (or a script + checklist you can run locally).

If you want, I can also:
- Produce a one‑click checklist script (PowerShell/Batch) to automate the download & placement of the specific models and workflows.
- Create a lean "beginner" quickstart (screenshots + exact UI steps).
- Build the preconfigured zip for you.

Good luck — when the 3060 arrives, say the word and I’ll either build that package or give the exact script/one‑click commands to make setup truly painless.
