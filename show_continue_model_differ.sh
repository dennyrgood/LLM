#!/bin/bash

# Normal mode (no debug output)
#./generate_missing_models.sh

# With debug output
#./generate_missing_models.sh --debug

# With custom config and debug
#./generate_missing_models.sh /path/to/config.yaml https://ollama.example.com --debug

# Debug flag works in any position
#./generate_missing_models.sh --debug /path/to/config.yaml



# Script to generate config.yaml entries for LLMs not already in the config
# Uses the Ollama API to fetch available models and compares with config.yaml
# Usage: ./generate_missing_models.sh [config_file] [ollama_base] [--debug]

set -e

CONFIG_FILE="${1:-$HOME/.continue/config.yaml}"
OLLAMA_BASE="${2:-https://ollama.ldmathes.cc}"
DEBUG=false

# Check for --debug flag in any position
for arg in "$@"; do
    if [ "$arg" = "--debug" ]; then
        DEBUG=true
    fi
done

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file '$CONFIG_FILE' not found"
    exit 1
fi

echo "Fetching available models from $OLLAMA_BASE..."

# Try native Ollama API first, fall back to OpenAI-compatible API
AVAILABLE_MODELS=$(curl -s "$OLLAMA_BASE/api/tags" | jq -r '.models[].name' 2>/dev/null | sort)

# If that fails, try OpenAI-compatible endpoint
if [ -z "$AVAILABLE_MODELS" ]; then
    AVAILABLE_MODELS=$(curl -s "$OLLAMA_BASE/v1/models" | jq -r '.data[].id' 2>/dev/null | sort)
fi

if [ -z "$AVAILABLE_MODELS" ]; then
    echo "Error: No models found or unable to connect to Ollama server"
    echo "Tried both /api/tags and /v1/models endpoints"
    exit 1
fi

echo "Found $(echo "$AVAILABLE_MODELS" | wc -l) models on server"
echo ""

# Extract model names from config.yaml (look for 'model:' entries)
# Handle both quoted ("model:latest") and unquoted (model:latest) formats
CONFIGURED_MODELS=$(grep -E '^\s+model:\s*' "$CONFIG_FILE" | sed -E 's/.*model:[[:space:]]*"?([^"[:space:]]+)"?.*/\1/' | sort)

echo "Found $(echo "$CONFIGURED_MODELS" | wc -l) models in config"
echo ""

if [ "$DEBUG" = true ]; then
    # Debug: show what we're comparing
    echo "=== DEBUG: Configured models ==="
    echo "$CONFIGURED_MODELS" | sed -n l
    echo ""
    echo "=== DEBUG: Available models ==="
    echo "$AVAILABLE_MODELS" | sed -n l
    echo ""
fi

# Find models that are available but not configured
# Use process substitution with proper sorting
MISSING_MODELS=$(comm -23 <(echo "$AVAILABLE_MODELS" | sort -u) <(echo "$CONFIGURED_MODELS" | sort -u))

if [ -z "$MISSING_MODELS" ]; then
    echo "All available models are already configured!"
    exit 0
fi

echo "Found $(echo "$MISSING_MODELS" | wc -l) unconfigured models:"
if [ "$DEBUG" = true ]; then
    echo "$MISSING_MODELS"
fi
echo ""
echo "# ========================================="
echo "# Generated config entries for missing models"
echo "# Add these to your config.yaml models section"
echo "# ========================================="
echo ""

# Generate config entries for missing models
while IFS= read -r model; do
    # Skip empty lines
    [ -z "$model" ] && continue
    
    # Create a friendly name (capitalize, remove special chars)
    friendly_name=$(echo "$model" | sed 's/:/ /g; s/-/ /g; s/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')
    
    # Determine if it's likely a cloud model
    is_cloud=""
    if echo "$model" | grep -q "cloud"; then
        is_cloud=" (Cloud)"
    fi
    
    # Quote model name if it contains special characters
    quoted_model="\"$model\""
    
    cat << EOF
  - name: $friendly_name$is_cloud
    provider: ollama
    model: $quoted_model
    apiBase: $OLLAMA_BASE
    baseUrl: $OLLAMA_BASE
    roles:
      - chat
EOF

    # Add 'edit' role for models with 'coder' or 'code' in the name
    # These models are typically optimized for code generation/editing
    if echo "$model" | grep -qiE "coder|code|codestral|starcoder|wizardcoder"; then
        echo "      - edit"
    fi
    
    # Add tool_use capability for larger/smarter models
    # Pattern matches common LLM families known to support function calling:
    # - llama: Meta's Llama series
    # - qwen: Alibaba's Qwen series  
    # - deepseek: DeepSeek models
    # - gpt: GPT-style models
    # - glm: ChatGLM series
    # - mistral: Mistral AI models
    # - mixtral: Mistral's MoE models
    # - phi: Microsoft's Phi series
    # - gemma: Google's Gemma series
    # - command: Cohere's Command models
    # - claude: Anthropic's Claude (if proxied)
    # - yi: 01.AI's Yi series
    # - falcon: TII's Falcon models
    # - vicuna: LMSYS Vicuna
    # - orca: Microsoft's Orca series
    # - openchat: OpenChat models
    # - nous: Nous Research models (hermes, etc)
    # - solar: Upstage's Solar models
    # - starling: Starling models
    if echo "$model" | grep -qiE "llama|qwen|deepseek|gpt|glm|mistral|mixtral|phi|gemma|command|claude|yi|falcon|vicuna|orca|openchat|nous|hermes|solar|starling|wizard"; then
        cat << EOF
    capabilities:
      - tool_use
EOF
    fi
    
    cat << EOF
    requestOptions:
      timeout: 300000
      keepAlive: 300000

EOF

done <<< "$MISSING_MODELS"

echo "# ========================================="
echo "# End of generated entries"
echo "# ========================================="
