
docker build -t stable-audio-container .

docker run --gpus all -v $(pwd)/output:/output stable-audio-container


- https://huggingface.co/spaces/facebook/MusicGen
- https://ai.honu.io/red/musicgen-colab
https://github.com/facebookresearch/audiocraft/blob/main/demos/audiogen_demo.ipynb


https://github.com/Alpha-VLLM/Lumina-T2X

https://github.com/Text-to-Audio/

https://huggingface.co/facebook/audio-magnet-small
