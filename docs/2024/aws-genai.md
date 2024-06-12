AWS GenAi workshop - June 5

Code Samples - https://github.com/aws-samples/amazon-bedrock-workshop

Amazon Bedrock
1. Curated dataset
2. Evaluation
3. Reviewers
4. Customer metric
5. Get Results


Customzing Foundation models

1. Prompt Engineering
2. Retrieval Augemented Generation (RAG)
3. Fine tuning
4. Continued Pre Training


RAG = Retrieval Augemented Generation


Vector Embeddings

Source Data -> Tokenization -> Vectorization -> Store in vector data store
-> Perform semantic similarity search -> Include semantically similar context in prompt


How to build Knowledge bases - Automatic



Vector Database - Enabling semantic search


Agents for Amazon Bedrock
	- Chain of thought/ chain executiion
Enable GenAI to execute multi step tasks using ompany systems and data sources


Guardrails for Amazon Bedrock
- content moderation as bedrock 
- 

Inference Consumption options
- On demand 
- Provisioned throughput 

Batch mode / load large dataset

Bedrock Studio / Sagemaker studio

Organizer 
lilzheng AT amazon DOT de

--

https://aws.amazon.com/blogs/aws/tackle-complex-reasoning-tasks-with-mistral-large-now-available-on-amazon-bedrock/


- postgresl + pg_vector extension : RAG
Document extractor : 

==

Go to Model access and enable the required mistral model
https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess


Get AWS CLI credentials

copy the parameters

export AWS_DEFAULT_REGION="us-west-2"
export AWS_ACCESS_KEY_ID="KEYIDASDASD"
export AWS_SECRET_ACCESS_KEY="SECREATEACESASDASKEY"
export AWS_SESSION_TOKEN="sesioandateoadlkalsda"

add to bash and execute the notebook


--