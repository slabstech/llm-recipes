from vllm import LLM
from vllm.sampling_params import SamplingParams

from mistral_common.protocol.instruct.messages import (
    UserMessage,
    TextChunk,
    ImageURLChunk,
    ImageChunk,
)
from PIL import Image
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer


def encode_images():

    tokenizer = MistralTokenizer.from_model("pixtral")

    image = Image.new('RGB', (64, 64))

    # tokenize images and text
    tokenized = tokenizer.encode_chat_completion(
        ChatCompletionRequest(
            messages=[
                UserMessage(
                    content=[
                        TextChunk(text="Describe this image"),
                        ImageChunk(image=image),
                    ]
                )
            ],
            model="pixtral",
        )
    )
    tokens, text, images = tokenized.tokens, tokenized.text, tokenized.images

    # Count the number of tokens
    print("# tokens", len(tokens))
    print("# images", len(images))



def image_urls():
    url_dog = "https://picsum.photos/id/237/200/300"
    url_mountain = "https://picsum.photos/seed/picsum/200/300"

    # tokenize image urls and text
    tokenized = tokenizer.encode_chat_completion(
        ChatCompletionRequest(
            messages=[
                UserMessage(
                    content=[
                        TextChunk(text="Can this animal"),
                        ImageURLChunk(image_url=url_dog),
                        TextChunk(text="live here?"),
                        ImageURLChunk(image_url=url_mountain),
                    ]
                )
            ],
            model="pixtral",
        )
    )
    tokens, text, images = tokenized.tokens, tokenized.text, tokenized.images

    # Count the number of tokens
    print("# tokens", len(tokens))
    print("# images", len(images))

def image_data():
    tokenized = tokenizer.encode_chat_completion(
    ChatCompletionRequest(
        messages=[
            UserMessage(
                content=[
                    TextChunk(text="What is this?"),
                    ImageURLChunk(image_url="data:image/jpeg;base64,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"),
                ]
            )
        ],
        model="pixtral",
    )
)
    tokens, text, images = tokenized.tokens, tokenized.text, tokenized.images

    # Count the number of tokens
    print("# tokens", len(tokens))
    print("# images", len(images))

def simple_example():
    model_name = "mistralai/Pixtral-12B-2409"

    sampling_params = SamplingParams(max_tokens=8192)

    llm = LLM(model=model_name, tokenizer_mode="mistral")

    prompt = "Describe this image in one sentence."
    image_url = "https://picsum.photos/id/237/200/300"

    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_url}}]
        },
    ]

    outputs = vllm_model.model.chat(messages, sampling_params=sampling_params)

    print(outputs[0].outputs[0].text)

def advanced_example():

    model_name = "mistralai/Pixtral-12B-2409"
    max_img_per_msg = 5
    max_tokens_per_img = 4096

    sampling_params = SamplingParams(max_tokens=8192, temperature=0.7)
    llm = LLM(model=model_name, tokenizer_mode="mistral", limit_mm_per_prompt={"image": max_img_per_msg}, max_num_batched_tokens=max_img_per_msg * max_tokens_per_img)

    prompt = "Describe the following image."

    url_1 = "https://huggingface.co/datasets/patrickvonplaten/random_img/resolve/main/yosemite.png"
    url_2 = "https://picsum.photos/seed/picsum/200/300"
    url_3 = "https://picsum.photos/id/32/512/512"

    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": url_1}}, {"type": "image_url", "image_url": {"url": url_2}}],
        },
        {
            "role": "assistant",
            "content": "The images shows nature.",
        },
        {
            "role": "user",
            "content": "More details please and answer only in French!."
        },
        {
            "role": "user",
            "content": [{"type": "image_url", "image_url": {"url": url_3}}],
        }
    ]

    outputs = llm.chat(messages=messages, sampling_params=sampling_params)
    print(outputs[0].outputs[0].text)





def precompute_freqs_cis_2d(
     dim: int,
     height: int,
     width: int,
     theta: float,
 ) -> torch.Tensor:
     """
     freqs_cis: 2D complex tensor of shape (height, width, dim // 2) to be indexed by
         (height, width) position tuples
     """
     # (dim / 2) frequency bases
     freqs = 1.0 / (theta ** (torch.arange(0, dim, 2).float() / dim))
 
     h = torch.arange(height, device=freqs.device)
     w = torch.arange(width, device=freqs.device)
 
     freqs_h = torch.outer(h, freqs[::2]).float()
     freqs_w = torch.outer(w, freqs[1::2]).float()
     freqs_2d = torch.cat(
         [
             freqs_h[:, None, :].repeat(1, width, 1),
             freqs_w[None, :, :].repeat(height, 1, 1),
         ],
         dim=-1,
     )
     return torch.polar(torch.ones_like(freqs_2d), freqs_2d)