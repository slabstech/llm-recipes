import numpy as np
import keras_nlp
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_text as tf_text
from tensorflow import keras
from tensorflow.lite.python import interpreter
import time


def get_gpt2_lm():
    gpt2_tokenizer = keras_nlp.models.GPT2Tokenizer.from_preset("gpt2_base_en")
    gpt2_preprocessor = keras_nlp.models.GPT2CausalLMPreprocessor.from_preset(
        "gpt2_base_en",
        sequence_length=256,
        add_end_token=True,
    )
    gpt2_lm = keras_nlp.models.GPT2CausalLM.from_preset("gpt2_base_en", preprocessor=gpt2_preprocessor)
    return gpt2_lm

'''
start = time.time()

output = gpt2_lm.generate("My trip to Yosemite was", max_length=200)
print("\nGPT-2 output:")
print(output.numpy().decode("utf-8"))

end = time.time()
print("TOTAL TIME ELAPSED: ", end - start)


start = time.time()

output = gpt2_lm.generate("My trip to Yosemite was", max_length=200)
print("\nGPT-2 output:")
print(output.numpy().decode("utf-8"))

end = time.time()
print("TOTAL TIME ELAPSED: ", end - start)

gpt2_tokenizer.tokenize(["Today is a beautiful day"]).flat_values
'''

'''
ds = tf.data.Dataset.from_tensor_slices(["Today is a beautiful day"])
preprocessed_ds = ds.map(gpt2_preprocessor)
output = next(iter(preprocessed_ds))
print('token ids:')
print(output[0]['token_ids'])
print('padding masks:')
print(output[0]['padding_mask'])



prediction_logits = gpt2_lm.predict(["Today is a beautiful day"])
print(prediction_logits.shape)
print(prediction_logits[0])

'''

@tf.function
def generate(prompt, max_length):
    return gpt2_lm.generate(prompt, max_length)



def run_inference(input, generate_tflite):
  interp = interpreter.InterpreterWithCustomOps(
      model_content=generate_tflite,
      custom_op_registerers=tf_text.tflite_registrar.SELECT_TFTEXT_OPS)
  interp.get_signature_list()

  generator = interp.get_signature_runner('serving_default')
  output = generator(prompt=np.array([input]))
  print("\nGenerated with TFLite:\n", output["output_0"])

# Non Quantized model
'''
concrete_func = generate.get_concrete_function(tf.TensorSpec([], tf.string), 100)
gpt2_lm.jit_compile = False
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func],
                                                            gpt2_lm)
converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
  tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]
converter.allow_custom_ops = True
converter.target_spec.experimental_select_user_tf_ops = ["UnsortedSegmentJoin", "UpperBound"]
converter._experimental_guarantee_all_funcs_one_use = True
generate_tflite = converter.convert()
run_inference("I'm enjoying a", generate_tflite)

with open('unquantized_gpt2.tflite', 'wb') as f:
  f.write(generate_tflite)

'''

def quantize_model():
    concrete_func = generate.get_concrete_function(tf.TensorSpec([], tf.string), 100)
    # Quantized model
    gpt2_lm.jit_compile = False
    converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func],
                                                                gpt2_lm)
    converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
    tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
    ]
    converter.allow_custom_ops = True
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.experimental_select_user_tf_ops = ["UnsortedSegmentJoin", "UpperBound"]
    converter._experimental_guarantee_all_funcs_one_use = True
    quant_generate_tflite = converter.convert()
    run_inference("I'm enjoying a", quant_generate_tflite)

    with open('quantized_gpt2.tflite', 'wb') as f:
        f.write(quant_generate_tflite)


def load_model(model_name):
    # quantized_gpt2 as autocomplete
    with open(model_name, 'rb') as file:
        model = file.read()
    return model


def run_inferenced(input, model):
  interp = interpreter.InterpreterWithCustomOps(
      model_content=model,
      custom_op_registerers=tf_text.tflite_registrar.SELECT_TFTEXT_OPS)
  interp.get_signature_list()

  generator = interp.get_signature_runner('serving_default')
  output = generator(prompt=np.array([input]))
  output_text = output["output_0"].item(0).decode('utf-8')
  return output_text


def main():
    model_name = 'unquantized_gpt2.tflite'

    model = load_model(model_name)
    text_input='who are you?'
    output_text = run_inferenced(text_input, model)
    print(output_text)

if __name__ == "__main__":
    main()
