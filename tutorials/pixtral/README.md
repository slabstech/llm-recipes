Pixtral - Vision Language Model

- Setup 
  - pip install vllm

- pip install --upgrade mistral_common



- git clone https://github.com/patrickvonplaten/vllm.git
- cd vllm
- python3.10 -m venv venv
- source venv/bin/activate
- pip install -e .

- https://github.com/patrickvonplaten/vllm/tree/pixtral

- https://huggingface.co/spaces/gaganyatri/pixtral-demo

git clone git@hf.co:spaces/gaganyatri/pixtral-demo

- HF 
    - https://huggingface.co/mistralai/Pixtral-12B-2409

- vllm
    - vllm serve mistralai/Pixtral-12B-2409 --tokenizer_mode mistral --limit_mm_per_prompt 'image=4' --max_num_batched_tokens 16384

    - curl --location 'http://<your-node-url>:8000/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer token' \
--data '{
    "model": "mistralai/Pixtral-12B-2409",
    "messages": [
      {
        "role": "user",
        "content": [
            {"type" : "text", "text": "Describe this image in detail please."},
            {"type": "image_url", "image_url": {"url": "https://s3.amazonaws.com/cms.ipressroom.com/338/files/201808/5b894ee1a138352221103195_A680%7Ejogging-edit/A680%7Ejogging-edit_hero.jpg"}},
            {"type" : "text", "text": "and this one as well. Answer in French."},
            {"type": "image_url", "image_url": {"url": "https://www.wolframcloud.com/obj/resourcesystem/images/a0e/a0ee3983-46c6-4c92-b85d-059044639928/6af8cfb971db031b.png"}}
        ]
      }
    ]
  }'



- Reference
    - Magnet Link - magnet:?xt=urn:btih:7278e625de2b1da598b23954c13933047126238a&dn=pixtral-12b-240910&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.ipv6tracker.org%3A80%2Fannounce
    - Uploaded hugging face 
        - https://huggingface.co/gaganyatri/pixtral-12b
        -  huggingface-cli upload  gaganyatri/pixtral-12b pixtral-12b-240910/ --repo-type model
        - 
    - Announcement
        - https://github.com/mistralai/mistral-common/releases/tag/v1.4.0
        - https://github.com/vllm-project/vllm/pull/8377/files

    - https://docs.vllm.ai/en/latest/getting_started/installation.html

    - CUDA latest - 12.6 - https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local
    