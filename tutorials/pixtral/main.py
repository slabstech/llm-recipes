from vllm import LLM
from vllm.sampling_params import SamplingParams


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