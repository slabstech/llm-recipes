gpt-oss


pip install -U transformers kernels torch accelerate

python run_model.py



transformers serve
transformers chat localhost:8000 --model-name-or-path openai/gpt-oss-20b



