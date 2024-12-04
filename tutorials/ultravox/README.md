UltraVox - Speech Language Model


- Small model - fixie-ai/ultravox-v0_3-llama-3_2-1b
  - huggingface-cli download fixie-ai/ultravox-v0_3-llama-3_2-1b
- 

Run with vLLM
 - just python -m vllm.entrypoints.openai.api_server  --model=fixie-ai/ultravox-v0_4  \
     --enable-chunked-prefill=False --max-model-len 8192  \
     --served-model-name fixie-ai/ultravox
     

llama3 + Whisper Small

- Reference

  - https://huggingface.co/fixie-ai/ultravox-v0_3

  - https://github.com/fixie-ai/ultravox

  - https://ai.town
  - https://github.com/vllm-project/vllm/blob/main/examples/offline_inference_audio_language.py

