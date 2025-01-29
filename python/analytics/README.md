Analytics

- Read [setup.md](setup.md) to build End-to-End platform for Notebook LLM

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


- Reference
  - NotebookLLM
  - NotebookLaama - https://github.com/meta-llama/llama-cookbook/tree/main/end-to-end-use-cases/NotebookLlama

