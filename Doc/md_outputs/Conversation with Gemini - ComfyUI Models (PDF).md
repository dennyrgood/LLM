# Conversation with Gemini - ComfyUI Models (PDF)

Extracted from PDF: Conversation with Gemini - ComfyUI Models (PDF).pdf

---

Conversation with Gemini – ComfyUI
Models
So, i am not 'stuck' on using the 'flux' ... it what your cousin "claude" recommended ... what i
want is a set of models to be able to do background removal, person removal, restoration of old
photos, and maybe some toy things like turning people into puppets, what models should i be
looking at
That is an excellent set of goals. Since you are using ComfyUI, you have the flexibility to mix
and match specialized models and nodes, which is the key to achieving professional-grade results
for these tasks.
Your choice to move away from general generation models for specialized editing is smart. The
models below are recommended because they are efficient enough to run on an RTX 3060 12GB
card within ComfyUI, often by utilizing their dedicated smaller file versions (like FP8 or GGUF,
where available).
Here are the best models and techniques you should be looking at for each of your goals:

1. Background & Person Removal (Inpainting)
This is a two-step process: Masking (identifying the object) and Inpainting (filling the hole).
Task Step

Recommended
Model/Technique

Masking

RMBG (Remove
Background) Node

Object
Detection

GroundedSAM / SAM2

Inpainting

SDXL Inpainting
Checkpoint or SD 1.5
Inpainting Checkpoint

Alternative Qwen Image Edit

Notes for ComfyUI & 12GB VRAM
This is a highly effective node (ComfyUI-RMBG) for
generating a precise mask of a person or object
automatically. It's fast and works great for getting a
clean alpha channel.
Use these to automatically detect specific objects
(e.g., "person") with text prompts to create a mask.
More powerful than simple segmentation, but
slightly slower.
Use a model specifically trained for inpainting (e.g.,
a dedicated version of DreamShaper Inpainting).
These models are efficient at intelligently filling the
masked area.
A very powerful model that can handle complex
edits based on a prompt, like "remove the person"
or "change the background to white." It's a
great all-in-one option for editing.

Workflow Tip: Combine the mask output from RMBG/SAM with the VAE Encode (for
Inpainting) and SetNoiseMask nodes in ComfyUI, feeding the result into your preferred
Inpainting Model.

2. Restoration of Old Photos
Restoration is a pipeline of upscaling, de-noising, and face enhancement. You will need to use
multiple specialized models in sequence.
Restoration Task

Recommended
Model/Technique

Notes for ComfyUI & 12GB VRAM

These are the industry-standard models for fixing
blurry, damaged, or low-resolution faces. They are
Face
CodeFormer or
typically implemented as post-processing nodes in
Enhancement
GFPGAN
ComfyUI and are relatively fast. CodeFormer is often
considered to produce slightly more natural results.
A high-quality upscaling model. Use this to increase
4x-UltraSharp
Upscaling/Detail
the resolution of the restored image and sharpen fine
(ESRGAN)
details like clothing and background texture.
Use your inpainting model with a mask covering
Inpainting Model
Noise & Artifacts
scratches, tears, or heavy folds to generate clean,
(from section 1)
consistent content in those areas.
For black and white photos, search Civitai for an SD
Colorization
Model-Specific
1.5 or SDXL LoRA specifically trained for "natural
(Optional)
Colorization LoRA
colorization" to apply color in a realistic way.

3. Turning People into Puppets (Toy Styles)
This falls under Image-to-Image and Style Transfer. The best way to do this is by combining
an existing photo with a highly stylized model or LoRA, while maintaining the person's pose and
composition.
Task Step

Recommended
Model/Technique

Notes for ComfyUI & 12GB VRAM

Base
Generation

SDXL Checkpoint or
Juggernaut XL

SDXL base models are generally better at generating
high-quality stylistic details. Juggernaut is a popular
photorealistic model that handles styles well.

Specific LoRA (e.g.,
Style/Puppet
Claymation/Puppet
Look
LoRA)

Search communities like Civitai for LoRAs with
keywords like "Claymation," "Wool Puppet," "Stop-

Task Step

Recommended
Model/Technique

Notes for ComfyUI & 12GB VRAM

Motion," or "Pixar Style." You must load this LoRA
into your workflow.
This is crucial. Use ControlNet OpenPose to ensure
the generated "puppet" is in the exact same pose as the
Pose
ControlNet (OpenPose
person in the original photo. You can also use
Preservation or Canny)
ControlNet Canny to lock in the main outlines and
edges.
Workflow Tip: Use a low-to-medium Denoise Strength (around 0.5 - 0.7) in your KSampler.
This tells the model to keep the image composition and person's structure largely intact but to
apply the new puppet style heavily.

Gemini can make mistakes, including about people, so double-check it. Your privacy & Gemini
Opens in a new window

