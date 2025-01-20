# DeepSeek - R1

## Model

### Original
- **Model Name:** deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
- **Repository:** [deepseek-ai/DeepSeek-R1-Distill-Qwen-7B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)

### GGUF
- **Repository:** [unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF](https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/tree/main)

## Paper
- **GitHub Repository:** [deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)

## Ollama Setup
To pull the model using Ollama, run the following command:
```sh
ollama pull hf.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF:Q4_K_M
```

## Running the Model
To run the model, use the following command:
```sh
python main.py
```

## Example

### Question
What is 1+1?

### Response


```
    <think>
    To provide a clear and helpful answer to the user's question "What is 1 + 1?", I will start by stating that this is a fundamental arithmetic operation.

    Next, I'll explain that addition combines two numbers to produce their total sum.

    Then, I'll compute the result of adding one and one together, which equals two.

    Finally, I'll present the final answer in a boxed format to make it easy for the user to see.
    </think>

    Certainly! Let's solve the problem step by step.

    **Question:** What is \(1 + 1\)?

    **Solution:**

    Addition is the process of combining two numbers to find their total sum. 

    Here, we are adding the number **1** and the number **1**.

    \[
    1 + 1 = \boxed{2}
    \]

    So, \(1 + 1 = \boxed{2}\).
```