Spirit LM


 git clone https://huggingface.co/spaces/gaganyatri/spirit-lm

mkdir checkpoints

python3.10 -m venv venv

source venv/bin/activate

pip install huggingface_hub

huggingface-cli download spirit-lm/Meta-spirit-lm  --local-dir checkpoints/



Research Paper - https://arxiv.org/pdf/2402.05755.pdf

Source - https://github.com/facebookresearch/spiritlm

Website - https://speechbot.github.io/spiritlm/

pip install git+https://github.com/facebookresearch/spiritlm.git

HF - Space - https://huggingface.co/spaces/gaganyatri/spirit-lm
