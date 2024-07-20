/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_OLLAMA_BASE_URL: string;
    // more env variables...
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }