Prime RL

https://github.com/PrimeIntellect-ai/prime-rl

curl -LsSf https://astral.sh/uv/install.sh | sh

 uv venv venv

source venv/bin/activate

uv sync && uv sync --all-extras


Test Environment

```bash
uv run python -V

uv run python -c "import flash_attn"

uv run sft @ configs/debug/sft/train.toml

uv run trainer @ configs/debug/rl/train.toml

uv run inference @ configs/debug/infer.toml

uv run orchestrator @ configs/debug/orch.toml


uv run eval @ configs/debug/eval.toml
```