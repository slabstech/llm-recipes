VLLM

 vllm serve google/gemma-3-4b-it     --served-model-name google/gemma-3-4b-it     --host 0.0.0.0     --port 7863     --gpu-memory-utilization 0.9     --tensor-parallel-size 1     --max-model-len 16384     --dtype bfloat16 



vllm serve google/gemma-3-12b-it     --served-model-name google/gemma-3-12b-it     --host 0.0.0.0     --port 7863     --gpu-memory-utilization 0.9     --tensor-parallel-size 1     --max-model-len 16384     --dtype bfloat16  


pip install bitsandbytes
vllm serve google/gemma-3-12b-it \
    --served-model-name google/gemma-3-12b-it \
    --host 0.0.0.0 \
    --port 7863 \
    --gpu-memory-utilization 0.9 \
    --tensor-parallel-size 1 \
    --max-model-len 16384 \
    --dtype half \
    --quantization bitsandbytes \
    --load-format bitsandbytes



https://blog.vllm.ai/2025/04/11/transformers-backend.html


https://blog.vllm.ai/2025/02/17/distributed-inference.html