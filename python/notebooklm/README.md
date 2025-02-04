NotebookLM - Self-hosted 

- GoAudio 
  - [Challenge](docs/challenge.md)
  - [Solution](docs/solution.md)
  - How to [sync audio](docs/audio-sync.md)
- Read [setup.md](docs/setup.md) to build End-to-End platform for Notebook LLM

- Steps
  - PDF parser - temperature 0 ,
  - transcript writer - temperature 1 , large context


- Code security analysis
- Book Editor : Editor for manuscript
  - Parse PDFs and provide suggestions to improvement
  - Update PDF via markdown and self correct the manuscript
  - Use Online API and Offline modesl for evaluation

- Milestone for implementation
    - v0 - Use single shot parse via large context
    - v1 - Use multi-shot prompts 
    - v2 - Use embedding and chunking of data for improvement
    - v3 - Use reasoning model
- Build Agent to fix issues via evaluation loop


- v3 - Using reasoning model
  - Use deepseek reasoner for Chain of thoughts method to create synthetic data
  - Summarize the Chain of thoughts via summarizer for solution

- Extra - Notebookllama
  - Create on-demand audio for explaining topics via streaming
  - Make mini-steps to branch information when new question are requested/asked
  - Implement idea via python CLI first and beta testing
  - Add UX when user testing is completing


- Download models
  - huggingface-cli download parler-tts/parler-tts-mini-v1
  - huggingface-cli download  suno/bark

- Reference
  - NotebookLLM
  - NotebookLaama - https://github.com/meta-llama/llama-cookbook/tree/main/end-to-end-use-cases/NotebookLlama
  - code security
    - https://github.com/meta-llama/llama-cookbook/tree/main/end-to-end-use-cases/github_triage
