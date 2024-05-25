Function Calling with REST API

Get real time info by fetching details from REST API

- Create tools definition dynamically by parsing json from SwaggerUI
- Pass tools definition array to ChatCompletionRequest
- Create list of queries - LLM model for problem statement
- Pass queries to Model request as array.
- Write a parser for token output to get function calling params 

- Create AutoGen workflow to automate the above steps

- Future
    - With stable diffusion, create dashboards with interactive graphics ?