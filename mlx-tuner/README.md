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

### 🤔 "What does rank mean?"

Think of LoRA rank as the "resolution" of your correction sheet:

| Rank | Size | Quality | Memory |
|------|------|---------|--------|
| 4 | Tiny | Basic | ~0.8 MB |
| 8 | Small | Good | ~1.6 MB |
| 16 | Medium | Better | ~3.2 MB |
| 64 | Large | Best | ~13 MB |

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

---

## Quick Start (I promise it's easy!)

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

That's it! 🎉

---

## What Just Happened?

Let me walk through what the code does:

### Step 1: Load model
```python
from mlx_lm import load
model, tokenizer = load("microsoft/Phi-3-mini-4k-instruct")
```
Downloads a 3.8GB model from HuggingFace.

### Step 2: Convert to LoRA
```python
from mlx_lm.tuner import linear_to_lora_layers

linear_to_lora_layers(
    model, 
    num_layers=4,  # Only convert 4 layers
    lora_params={"rank": 4, "scale": 8}
)
```
Adds small matrices to only 4 attention layers.

NOW your model has:
- 3,821,080,000 frozen parameters (original)
- 786,432 NEW trainable parameters (LoRA)
- Total: 0.78M trainable (0.021%) ✅

### Step 3: Train
```python
from mlx_lm.tuner import train

train(
    model=model,
    tokenizer=tokenizer,
    args=TrainingArgs(iters=10),
    train_data=[("./data/train.jsonl",)]
)
```
Runs 10 iterations of training. Updates only the 0.78M LoRA weights!

### Step 4: Save
```python
model.save_adapters("./adapters/adapter.safetensors")
```
Saves your tiny LoRA weights. To use later:

```python
model.load_adapters("./adapters/adapter.safetensors")
```

---

## Common Questions

### "Can I train on my MacBook Air?"
- ✅ M1/M2/M3/M4 (any Apple Silicon): Yes!
- ❌ Intel Mac: No (no GPU cores)
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

### "How do I use the trained model?"
```python
from mlx_lm import load, generate

model, tokenizer = load("microsoft/Phi-3-mini-4k-instruct")
model.load_adapters("./adapters/adapter.safetensors")

response = generate(model, tokenizer, "What's machine learning?")
print(response)
```

---

## Why This Matters for Your Career

If you want to work at companies like **OpenChip**, **Anthropic**, or **OpenAI** on the AI infrastructure side:

1. ✅ This shows you understand the FULL ML stack (not just API calls)
2. ✅ You know how to optimize memory (critical for custom silicon)
3. ✅ You've worked with low-level GPU frameworks (Metal, CUDA)
4. ✅ You've dealt with real training pipelines (not just demos)

Companies building custom AI chips NEED people who understand:
- How models are trained
- Where the bottlenecks are
- How to reduce memory footprint
- How quantization works

This repo proves you can do all of that!

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
  rank: 4  # instead of 8
```

### "Model not found"

Make sure you're logged into HuggingFace (for gated models):
```bash
huggingface-cli login
```

---

## Project Structure

```
mlx-tuner/
├── src/mlx_tuner/
│   ├── __init__.py
│   ├── config.py              # Settings
│   ├── logging.py             # Structured logging
│   ├── protocols.py           # For testing
│   ├── cli/                   # Command line
│   │   ├── train.py
│   │   ├── fuse.py
│   │   └── convert.py
│   ├── data/                  # Data loading
│   ├── models/                 # Model loading
│   │   └── loader.py          # mlx_lm.load
│   ├── training/
│   │   ├── lora.py            # LoRA implementation
│   │   └── trainer.py         # Training loop
│   └── convert/                # GGUF export
├── data/                       # Your training data
├── adapters/                   # Saved LoRA weights
├── train_config.yaml          # Your config
├── Makefile
└── README.md
```

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

*"The best way to understand AI is to build AI."* - Actually, I just made that up, but it's true!