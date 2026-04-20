# MLX Tuner

**Train your own AI models on Apple Silicon!**

If you've used OpenAI's API or wrote agents with LangChain, this repo shows you the OTHER side of AI - how to actually TRAIN a model instead of just calling one.

## TL;DR - Why Should I Care?

As an AI developer, you probably do stuff like:
```python
response = openai.chat.completions.create(
    model="gpt-4", 
    messages=[{"role": "user", "content": "Explain ML"}]
)
```

This repo shows what happens **BEFORE** that model exists. It's like going from "using a pre-made app" to "building the app from scratch."

**Real training result:**
```
Model: Phi-3-mini (3.8 billion parameters)
LoRA: We trained only 0.786 MILLION parameters (0.021% of the model!)
Memory: 7.9 GB (fits on your M4 Pro!)
Speed: 164 tokens/second
```

---

## The Concepts You Need to Know

### 🤔 "What is fine-tuning?"

**Analogy:** Think of a pre-trained model like a student who already learned grammar in school. Fine-tuning is like giving that student specialized training - maybe to be a doctor, lawyer, or pirate.

You START with a model that already knows language. You TEACH it your specific task (like answering questions about your code, or speaking in your company's style).

### 🤔 "Why can't I just train from scratch?"

**Math:** A 3.8 BILLION parameter model has 3.8 billion numbers. Changing all of them requires:
- Massive GPU memory
- Weeks of training time
- Thousands of dollars in cloud computing

**LoRA solution:** We freeze the 3.8B numbers and add ONLY 0.78M new numbers. It's 99.98% cheaper!

### 🤔 "What is LoRA actually doing?"

Pretend the model is a big lookup table:

```
Original: "Machine learning is ____"
We want it to say: "Machine learning is AWESOME"
```

Instead of rewriting every entry in the table, LoRA adds a small "correction sheet" on top:

```
Base table:      "Machine learning is [unchanged]"
Correction:     + "AWESOME" (our tiny LoRA weights)
```

During inference, the system adds them together. Magic!

### 🤔 "What is LoRA rank?"

Think of LoRA rank as the "resolution" of your correction sheet:

| Rank | Size | Quality | Memory |
|------|------|---------|--------|
| 4 | Tiny | Basic | ~0.8 MB |
| 8 | Small | Good | ~1.6 MB |
| 16 | Medium | Better | ~3.2 MB |
| 64 | Large | Best | ~13 MB |

**How rank affects parameters:**
For a model with hidden dimension `d = 3072` (Phi-3-mini):
- Full matrix: d × d = 3072 × 3072 = 9.4M parameters
- LoRA with rank=4: A(d×4) + B(4×d) = 3072×4 + 4×3072 = 24.5K parameters
- Reduction: 99.7%

### 🤔 "What is Apple Silicon's Unified Memory?"

Normal computers: CPU RAM (for programs) is SEPARATE from GPU VRAM (for graphics) = slow transfer

Apple Silicon: CPU and GPU SHARE the same RAM = zero transfer time

It's like having one notebook instead of two separate books - no copying needed!

### 🤔 "What is a tokenizer?"

Computers don't understand words. They understand numbers.

```
Your text:    "Hello world"
Tokenizer:  [987, 2341, 1022, 5503]
```

It's like assigning each word a dictionary index number. The tokenizer does this translation.

### 🤔 "What is a chat template?"

Different AI models expect messages in different formats:

```
OpenAI style:
    [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hi!"}]

Llama style:
    [INST]Hi[/INST] Hi! [/SA]

Meta style:
    <|user|>Hi<|assistant|>Hi!<|end|>
```

Chat template normalizes all these to one format. Some models (like SmolLM) don't have one defined!

### 🤔 "What are Attention Layers?"

In a transformer model, "attention" is how the model decides what to focus on when processing each word. It uses three special matrices:

- **Query (Q)**: "What am I looking for?"
- **Key (K)**: "What do I contain?"
- **Value (V)**: "What actual information do I have?"

LoRA saves MOSTLY by adding small matrices to Q and V projections. These are usually called:
- `q_proj` (Query projection)
- `k_proj` (Key projection)  
- `v_proj` (Value projection)
- `o_proj` (Output projection)

When we say `num_layers: 4`, we mean "add LoRA to the Q and V projections of the first 4 attention layers."

---

## The LoRA Math Explained

### The Problem
A full linear layer has weight matrix W of shape (d_in, d_out). For Phi-3-mini:
- d_in = 3072, d_out = 3072
- W has 9,437,184 parameters (3072 × 3072)

### The LoRA Solution
We decompose W into two smaller matrices:
- **A** of shape (d_in, r) where r is the rank
- **B** of shape (r, d_out)

During forward pass:
```
output = W • x + A • B • x
       = W • x + (A • B) • x
```

The key insight: we only train A and B. W stays frozen.

### Parameter Count
For r = 4:
- A: 3072 × 4 = 12,288 parameters
- B: 4 × 3072 = 12,288 parameters  
- Total LoRA: 24,576 parameters

Vs original: 9,437,184 parameters

**Reduction: 99.74%**

### The Scaling Factor
The output from A•B is scaled by (alpha/rank). With alpha=8, rank=4:
- scale = 8/4 = 2

This ensures the LoRA contribution is normalized regardless of rank.

---

## Quick Start

### 1. Install
```bash
cd mlx-tuner
make install
```

### 2. Create training data
Make a file called `data/train.jsonl`:

```json
{"text": "Instruction: What is ML?\n\nResponse: Machine learning is..."}
{"text": "Instruction: Explain neural networks\n\nResponse: Neural networks are..."}
```
(Add 10+ examples)

### 3. Create config
Make `train_config.yaml`:

```yaml
model: microsoft/Phi-3-mini-4k-instruct
train: true
fine_tune_type: lora
data: ./data
num_layers: 4
batch_size: 1
iters: 10
lora_parameters:
  rank: 4
  scale: 8
adapter_path: ./adapters
```

### 4. Train!
```bash
mlx_lm.lora -c train_config.yaml
```

---

## What Actually Happens (Real Code Flow)

The README examples show simplified Python, but here's what actually runs:

### Actual Flow via CLI:
```bash
mlx_lm.lora -c train_config.yaml
```

This internally calls:
1. **Load**: `mlx_lm.load(model_name)` - downloads model from HuggingFace
2. **Convert**: `linear_to_lora_layers(model, num_layers, lora_params)` - adds LoRA matrices
3. **Train**: `mlx_lm.tuner.train()` - runs training loop
4. **Save**: Saves adapters to `./adapters/adapters.safetensors`

### What Each File Does

| File in src/ | Purpose | Key Functions |
|--------------|---------|---------------|
| `training/lora.py` | LoRA utilities | `setup_lora_model()`, `save_adapters()`, `load_adapters()` |
| `training/trainer.py` | Training orchestration | Uses mlx-lm's `train()` and `evaluate()` |
| `models/loader.py` | Model loading | Wraps `mlx_lm.load()` |
| `cli/train.py` | CLI entry point | Parses YAML, calls mlx_lm.lora subprocess |
| `data/loaders.py` | Data loading | JSONL format handling |
| `convert/gguf_converter.py` | Model export | Converts to GGUF format |

### What the YAML Config Does:
```yaml
model: microsoft/Phi-3-mini-4k-instruct  # Which model to load
train: true                               # Enable training mode
fine_tune_type: lora                    # Use LoRA (not full fine-tune)
data: ./data                              # Training data directory
num_layers: 4                            # Apply LoRA to 4 attention layers
lora_parameters:
  rank: 4                                 # LoRA rank (r)
  scale: 8                                # Scaling factor (alpha)
iters: 10                                 # Training iterations
```

---

## Using the Trained Model

### With CLI (Easiest!)
```bash
# With your trained LoRA adapters
mlx_lm.generate \
    --model microsoft/Phi-3-mini-4k-instruct \
    --adapter-path ./adapters \
    --prompt "What is machine learning?" \
    --max-tokens 50

# Without adapters (original model)
mlx_lm.generate \
    --model microsoft/Phi-3-mini-4k-instruct \
    --prompt "What is machine learning?"
```

### With Python
```python
from mlx_lm import load, generate

# Load model with adapters
model, tokenizer = load(
    "microsoft/Phi-3-mini-4k-instruct",
    adapter_path="./adapters"
)

# Generate!
response = generate(model, tokenizer, "What's machine learning?")
print(response)
```

### What IS in adapters.safetensors?

The file contains:
- Matrix A (shape: [num_layers, d_in, rank]) - one per layer
- Matrix B (shape: [num_layers, rank, d_out])
- Scaling factors

For our Phi-3-mini with rank=4, num_layers=4:
- ~24KB total (tiny!)

This is why LoRA is amazing - you can store and share tiny adapter files instead of entire models.

---

## Post-Training: GGUF Conversion

After training, you might want to convert to GGUF format for C++ inference.

### What is GGUF?
GGUF (GPT-Generated Unified Format) is a binary file format that packs:
- Model weights (in quantized format)
- Tokenizer configuration
- Model architecture details

It's optimized for fast loading by inference engines.

### How to Convert (Basic)
```python
# Currently requires llama.cpp or mlx export tools
# This is a roadmap item for the project

# The concept:
from mlx_lm import convert

# Would convert to GGUF with quantization
convert.to_gguf("./adapters", "./model.gguf", quantization="Q4_K_M")
```

### Quantization Types

| Type | Bits | Memory Reduction | Quality |
|------|------|------------------|---------|
| Q8_0 | 8-bit | ~75% | Excellent |
| Q6_K | 6-bit | ~85% | Very Good |
| Q5_K_M | 5-bit | ~90% | Good |
| Q4_K_M | 4-bit | ~95% | Acceptable |

Q4_K_M means:
- 4-bit quantization
- K-means quantization with median threshold
- Most significant 2 bits preserved

---

## Fusing LoRA (Advanced)

Sometimes you want to MERGE the LoRA weights into the base model permanently:

```bash
# Using mlx-lm fuse command
mlx_lm.lora \
    --model microsoft/Phi-3-mini-4k-instruct \
    --adapter-path ./adapters \
    --fuse \
    --output ./fused_model
```

This creates a new model file with LoRA weights baked in. No more adapter file needed!

---

## Benchmark Results

### Training Performance (Phi-3-mini on M4 Pro):
```
Trainable parameters: 0.021% (0.786M/3821.080M)
Starting training..., iters: 10
Iter 1: Val loss 2.484
Iter 10: Val loss 2.436
Tokens/sec: 164
Peak memory: 7.886 GB
```

### Inference Performance:
```
=== With LoRA adapters ===
Generation: 25 tokens, 31.6 tokens-per-sec
Peak memory: 7.77 GB

=== Without LoRA ===
Generation: 25 tokens, 32.9 tokens-per-sec  
Peak memory: 7.75 GB
```

The LoRA overhead is ~4% - essentially negligible!

---

## Common Questions

### "Can I train on my MacBook Air?"
- YES: M1/M2/M3/M4 (any Apple Silicon)
- NO: Intel Mac (no GPU cores)
- RAM: 16GB works for small models, 24GB+ recommended

### "What models work?"
| Model | Size | Best For |
|-------|------|----------|
| SmolLM-135M | 135M | Learning/demos |
| Phi-3-mini | 3.8B | Production |
| Llama-3.2-1B | 1B | Balanced |

### "How long does training take?"
- 10 iterations: ~30 seconds
- 100 iterations: ~5 minutes
- 1000 iterations: ~30 minutes

---

## Troubleshooting

### "Tokenizer doesn't have chat_template"
Solution 1: Use text format instead of messages:
```json
{"text": "User: Hi\nAssistant: Hello!"}
```

Solution 2: Use a model with chat template:
```yaml
model: microsoft/Phi-3-mini-4k-instruct
```

### "Out of memory"
Solution: Reduce batch size or rank:
```yaml
batch_size: 1
lora_parameters:
  rank: 4
```

### "Model not found"
Make sure you're logged into HuggingFace:
```bash
huggingface-cli login
```

---

## Project Structure

```
mlx-tuner/
├── src/mlx_tuner/
│   ├── __init__.py
│   ├── config.py              # Pydantic settings
│   ├── logging.py             # structlog setup
│   ├── protocols.py           # For testing DI
│   ├── cli/                   # CLI commands
│   │   ├── train.py           # Training entry point
│   │   ├── fuse.py            # Model fusion
│   │   └── convert.py         # GGUF export
│   ├── data/                  # Dataset loading
│   │   └── loaders.py
│   ├── models/                # Model loading
│   │   └── loader.py          # mlx_lm.load wrapper
│   ├── training/
│   │   ├── lora.py            # LoRA implementation & utilities
│   │   └── trainer.py         # Training orchestration
│   └── convert/               # GGUF export
│       └── gguf_converter.py
├── data/                      # Training data (train.jsonl)
├── adapters/                   # Saved LoRA weights
│   └── adapters.safetensors    # ~24KB file with A and B matrices
├── train_config.yaml          # Training config
├── Makefile
└── README.md
```

---

## Requirements

- Python 3.11+
- Apple Silicon Mac (M1/M2/M3/M4)
- 24GB+ memory recommended
- macOS 15+

## Dependencies

```bash
pip install mlx mlx-lm transformers peft pydantic-settings structlog
```

## License

MIT

*"The best way to understand AI is to build AI."*