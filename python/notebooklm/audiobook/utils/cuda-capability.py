import torch

if torch.cuda.is_available():
    device = torch.cuda.current_device()
    capability = torch.cuda.get_device_capability(device)
    print(f"CUDA Compute Capability: {capability[0]}.{capability[1]}")
else:
    print("CUDA is not available on this system.")


