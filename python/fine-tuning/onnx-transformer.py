from pathlib import Path
import timeit
from copy import deepcopy
from onnxruntime import InferenceSession
from onnxruntime.transformers.optimizer import optimize_model
from optimum.onnxruntime import ORTModelForQuestionAnswering
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

def benchmark(f, name=""):
    # warmup
    for _ in range(10):
        f()
    seconds_per_iter = timeit.timeit(f, number=100) / 100
    print(
        f"{name}:",
        f"{seconds_per_iter * 1000:.3f} ms",
    )
