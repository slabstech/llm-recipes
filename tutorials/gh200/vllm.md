Vllm

python -m venv venv
source venv/bin/activate
pip install torch==2.7.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

pip install 

 vllm serve google/gemma-3-4b-it     --served-model-name google/gemma-3-4b-it     --host 0.0.0.0     --port 7863     --gpu-memory-utilization 0.9     --tensor-parallel-size 1     --max-model-len 16384     --dtype bfloat16 


 vllm serve google/gemma-3-4b-it     --served-model-name gemma3     --host 0.0.0.0     --port 7890     --gpu-memory-utilization 0.9     --tensor-parallel-size 1     --max-model-len 16384     --dtype bfloat16 
