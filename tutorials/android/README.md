Deploy on Android

Run GPT-2 model on device 
- https://codelabs.developers.google.com/kerasnlp-tflite#0


- Can it be upgraded for larger models ?

- API based - 


- Nexa - https://github.com/NexaAI/Ocotpus-v2-demo



- git clone https://github.com/googlesamples/mediapipe
- cd mediapipe
- git sparse-checkout init --cone
- git sparse-checkout set examples/llm_inference/android


- Start android studio
- Import project into android studio

- Download the model - gemma-2b

- Copy model to device using device explorer
	- https://developer.android.com/studio/debug/device-file-explorer

- Model download at
  - https://www.kaggle.com/models/google/gemma/tfLite/

- https://developers.googleblog.com/en/large-language-models-on-device-with-mediapipe-and-tensorflow-lite/

- https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/llm_inference/conversion/llm_conversion.ipynb
- https://github.com/google-ai-edge/mediapipe-samples/blob/main/examples/llm_inference/conversion/llm_conversion.ipynb



reference
- https://github.com/google-ai-edge/mediapipe-samples
- https://www.tensorflow.org/lite/examples
- https://ai.google.dev/edge/lite
- https://ai.google.dev/edge/mediapipe/solutions/genai/llm_inference

- https://ai.google.dev/edge/mediapipe/solutions/genai/llm_inference/android
- https://ai.google.dev/edge/mediapipe/solutions/setup_android#example_code

- https://llm.mlc.ai/

- https://bazel.build/install/ubuntu

Install bazel

Download bazel

wget https://github.com/bazelbuild/bazel/releases/download/7.3.0rc1/bazel-7.3.0rc1-installer-linux-x86_64.sh

chmod +x bazel-7.3.0rc1-installer-linux-x86_64.sh
./bazel-7.3.0rc1-installer-linux-x86_64.sh --user

add .bashrc
export PATH="$PATH:$HOME/bin"


-- 

tenorflow lite

- https://www.youtube.com/watch?v=pNWNMPi0Mvk
- https://keras.io/keras_nlp/
- https://www.tensorflow.org/lite
- https://ai.google.dev/gemma/docs/lora_tuning

- https://codelabs.developers.google.com/kerasnlp-tflite#0
- https://github.com/tensorflow/codelabs

Steps
  - Install - Android Studio - https://developer.android.com/studio/
- Dowload - https://github.com/tensorflow/examples

- build the tflite model - https://colab.research.google.com/github/tensorflow/codelabs/blob/main/KerasNLP/io2023_workshop.ipynb
