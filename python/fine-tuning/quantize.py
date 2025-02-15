import functools
from tqdm import tqdm

import torch 

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

from nn_pruning.inference_model_patcher import optimize_model
from nn_pruning.modules.quantization import prepare_static, quantize
