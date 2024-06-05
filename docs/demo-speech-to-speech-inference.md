Speech to Spech inference

Hello, Everyone. 
My project is llm-recipes. 

The project page is at slabstech.com/llm-recipes and setup details with code is available at github.com/slabstech/llm-recipes.

I am happy to present my experiments with Generative AI with focus on local/on-premise deployment for data security. 

We will demo an Alexa/Siri like service with end to end processing done locally.


With Open-weights release of LLM models with persmissive license,  models capable of GPT-3 level intelligence can deployed on a personal computer. GPT3.5 level model's are available but require server/workstation with multiple GPU for inference.

Coming back to the project. The program flow can be split into 3 modules.
1. Automatic Speech recognition using whisper 
2. Natural language query based API request using Mistral7b-v3 with function calling 
3. Text to Speech using XYZ to provide the result in voice format.

The demo is narrowed to PetStore query and can be extended to other data stores. 


We plan to further optimize the project to run with lower latency. For better speeds, it is suggested to run on a multi-gpu system, with each module running in a dedicated GPU card for inference. This project would require minimum 3 GPU's .

We have experimented the project with the following configuration for deployment testing, we have not made any bechmarks yet due to time constraints. 

1. Laptop with 16GB RAM , no gpu
2. Laptop with 32GB RAM, no gpu
3. Laptop wirh 32GB RAM, 12 GB gpu
4. Workstation with xx RAM, 1x 24GB gpu
5. Workstation with xx RAM, 3x 24GB gpu 

The project experiments are open sourced, you're encouraged to run the project on your systems. You can raise an issue on the GitHub project for any problems and queries. Also we would be happy to accept contributions to the code,documentation and feature request. 

Add - System diagram here
