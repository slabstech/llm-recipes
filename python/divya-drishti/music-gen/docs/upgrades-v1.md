
Inference Upgrade 


- Chunking Strategy : context length 

Implement chunking logic in generation.
10 secs audio max / 
Small text size .

Implement for both batch generation and single generation. 

Reduce cycles per call of image. 

Speed improvement with narrator/ long text .

-- 

Quality improvement 
Test audio with parler-tts-large for quality and speed .


-- 


analysis after solution

batch inference added unintended latency with large text arrarys.

Next step, chunking input arrays 
For batch inference. 

Latency is down by another multiple 

Chunking adds quality issues. 
Need to build an eval,
To identify any problem data and update chunk size.