GPUs Brrr

- Event - Berlin Harcore AI Hackathon 2025
- Date - 31-May - 1 June 2025

### Challenge 4: Benchmark Blitz: GPU Performance Testing with Qwen3

**Your Mission:**

Create a benchmark by running Qwen3 for 5 minutes. The output should be a number that makes the GPU comparable with other GPUs. The difficult part of the challenge is finding a way to use as many cores of the GPU as possible. In the end, no matter which NVIDIA GPU you choose, it should be possible to run this benchmark to see what the best GPU for a model is.

**The objective of the benchmark is twofold:**
- Model performance on a certain GPU type
- Check the GPU health

**What You’ll Build:**

You use vllm or other software to efficiently run Qwen3-0.6B (https://huggingface.co/Qwen/Qwen3-0.6B) in a benchmark. See the code here: https://github.com/yachty66/gpu-benchmark/blob/main/src/gpu_benchmark/benchmarks/qwen3_0_6b.py - yours could look similar. however keep in mind that the current code has issues since it doesnt use all the cores of a GPU and therefore is a not perfect benchmark.

**Evaluation Metrics:**

Compare the performance of the H200 and 5090. The H200 should perform better if you did it right. With the current implementation https://github.com/yachty66/gpu-benchmark/blob/main/src/gpu_benchmark/benchmarks/qwen3_0_6b.py, the 5090 outperforms the H200, which should not be the case.

**We Provide:**
- RTX 5090 via United Compute Cloud

- For the evaluation, i.e., the comparison between the 5090 and H200 for your benchmark, please reach out to the United Compute team. We will have access to an H200, but it's not supported on our cloud platform yet.