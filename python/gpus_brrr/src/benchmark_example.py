from transformers import AutoModelForCausalLM, AutoTokenizer, logging
import torch
import time
from tqdm import tqdm
import pynvml
import platform
import os
import random
import numpy as np

# Disable all warnings and progress bars from transformers
logging.set_verbosity_error()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def get_clean_platform():
    os_platform = platform.system()
    if os_platform == "Linux":
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.strip().split("=")[1].strip('"')
        except Exception:
            pass
        return f"Linux {platform.release()}"
    elif os_platform == "Windows":
        return f"Windows {platform.release()}"
    elif os_platform == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    else:
        return os_platform

def get_nvml_device_handle():
    """Get the correct NVML device handle for the GPU being used."""
    pynvml.nvmlInit()
    
    cuda_visible_devices = os.environ.get('CUDA_VISIBLE_DEVICES')
    if cuda_visible_devices is not None:
        try:
            original_gpu_index = int(cuda_visible_devices.split(',')[0])
            handle = pynvml.nvmlDeviceGetHandleByIndex(original_gpu_index)
            return handle
        except (ValueError, IndexError):
            print(f"Warning: Could not parse CUDA_VISIBLE_DEVICES={cuda_visible_devices}")
    
    cuda_idx = torch.cuda.current_device()
    return pynvml.nvmlDeviceGetHandleByIndex(cuda_idx)

def setup_qwen_model():
    model_name = "Qwen/Qwen3-0.6B"
    # Disable tokenizer warnings
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        # Disable model warnings and progress bars
        use_cache=True,
        low_cpu_mem_usage=True,
    )
    # Disable generation warnings
    model.generation_config.pad_token_id = tokenizer.pad_token_id
    model.config.pad_token_id = tokenizer.pad_token_id
    return model, tokenizer

def run_benchmark(model, tokenizer, duration):
    """Run the GPU benchmark for the specified duration in seconds."""
    handle = get_nvml_device_handle()
    
    # Setup variables
    generation_count = 0
    total_gpu_time = 0
    temp_readings = []
    power_readings = []
    
    # Start benchmark
    start_time = time.time()
    end_time = start_time + duration
    prompt = "Write a technical explanation of how GPUs process neural networks, in exactly 100 words."
    
    try:
        # Create a single progress bar for the entire benchmark
        with tqdm(total=100, desc="Benchmark progress", unit="%", ncols=100) as pbar:
            last_update_percent = 0
            
            while time.time() < end_time:
                # Get GPU temperature
                current_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                temp_readings.append(current_temp)
                
                # CUDA timing events
                start_event = torch.cuda.Event(enable_timing=True)
                end_event = torch.cuda.Event(enable_timing=True)
                torch.cuda.synchronize()
                
                # Record start time and generate text
                start_event.record()
                
                # Generate text without warnings
                with torch.no_grad():
                    messages = [{"role": "user", "content": prompt}]
                    text = tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True,
                        enable_thinking=False,
                        add_special_tokens=False
                    )
                    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
                    
                    generated_ids = model.generate(
                        **model_inputs,
                        max_new_tokens=256,
                        do_sample=False,
                        use_cache=True,
                        pad_token_id=tokenizer.pad_token_id
                    )

                
                end_event.record()
                torch.cuda.synchronize()
                
                # Calculate timing
                gpu_time_ms = start_event.elapsed_time(end_event)
                total_gpu_time += gpu_time_ms
                
                # Update counter
                generation_count += 1
                
                # Sample power usage
                try:
                    current_power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
                    power_readings.append(current_power)
                except:
                    pass
                
                # Update progress bar only when percentage changes
                current_time = time.time()
                current_percent = min(100, int((current_time - start_time) / duration * 100))
                if current_percent > last_update_percent:
                    pbar.update(current_percent - last_update_percent)
                    pbar.set_postfix({
                        'Generations': generation_count, 
                        'Temp': f"{current_temp}°C"
                    }, refresh=True)
                    last_update_percent = current_percent
        
        # Calculate results
        elapsed = time.time() - start_time
        avg_time_ms = total_gpu_time / generation_count if generation_count > 0 else 0
        avg_temp = sum(temp_readings) / len(temp_readings)
        max_temp = max(temp_readings)
        
        # Get GPU memory info
        try:
            meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            gpu_memory_total = round(meminfo.total / (1024 * 1024 * 1024), 2)
        except:
            gpu_memory_total = None
        
        # Calculate average power
        avg_power = round(sum(power_readings) / len(power_readings), 2) if power_readings else None
        
        # Clean up
        pynvml.nvmlShutdown()
        
        return {
            "completed": True,
            "result": generation_count,
            "max_temp": max_temp,
            "avg_temp": avg_temp,
            "elapsed_time": elapsed,
            "avg_time_ms": avg_time_ms,
            "gpu_utilization": (total_gpu_time/1000)/elapsed*100,
            "gpu_power_watts": avg_power,
            "gpu_memory_total": gpu_memory_total,
            "platform": get_clean_platform(),
            "acceleration": f"CUDA {torch.version.cuda}" if torch.cuda.is_available() else "N/A",
            "torch_version": torch.__version__
        }
    
    except KeyboardInterrupt:
        pynvml.nvmlShutdown()
        return {
            "completed": False,
            "result": generation_count,
            "max_temp": max(temp_readings) if temp_readings else 0,
            "avg_temp": sum(temp_readings)/len(temp_readings) if temp_readings else 0,
            "avg_time_ms": total_gpu_time / generation_count if generation_count > 0 else 0
        }
    except Exception as e:
        pynvml.nvmlShutdown()
        print(f"Error during benchmark: {e}")
        return {
            "completed": False,
            "error": str(e),
            "result": generation_count,
            "avg_time_ms": total_gpu_time / generation_count if generation_count > 0 else 0
        }

def load_pipeline():
    """Load the Qwen model pipeline and return it."""    
    model_name = "Qwen/Qwen3-0.6B"
    # Disable tokenizer warnings
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        use_cache=True,
        low_cpu_mem_usage=True,
    )
    # Disable generation warnings
    model.generation_config.pad_token_id = tokenizer.pad_token_id
    model.config.pad_token_id = tokenizer.pad_token_id
    return model, tokenizer

# if __name__ == "__main__":
#     # Load the model pipeline
#     model, tokenizer = load_pipeline()
    
#     # Run benchmark for 300 seconds (5 minutes)
#     results = run_benchmark(model, tokenizer, duration=300)
    
#     # Print results
#     print("\nBenchmark Results:")
#     print(f"Completed: {results['completed']}")
#     if results.get('error'):
#         print(f"Error: {results['error']}")
#     else:
#         print(f"Total generations: {results['result']}")
#         if 'avg_time_ms' in results:
#             print(f"Average generation time: {results['avg_time_ms']:.2f}ms")
#             print(f"GPU utilization: {results['gpu_utilization']:.2f}%")
#             print(f"Maximum GPU temperature: {results['max_temp']}°C")
#             print(f"Average GPU temperature: {results['avg_temp']:.2f}°C")
#             if results['gpu_power_watts']:
#                 print(f"Average GPU power usage: {results['gpu_power_watts']}W")
#             print(f"GPU memory total: {results['gpu_memory_total']}GB")
#             print(f"Platform: {results['platform']}")
#             print(f"Acceleration: {results['acceleration']}")
#             print(f"PyTorch version: {results['torch_version']}")
