Deploy on Android

- Run GPT-2 model on device 
  - https://codelabs.developers.google.com/kerasnlp-tflite#0
  - Steps
    - Install - Android Studio - https://developer.android.com/studio/
    - Download - https://github.com/tensorflow/examples
    - build the tflite model 
      - https://colab.research.google.com/github/tensorflow/codelabs/blob/main/KerasNLP/io2023_workshop.ipynb
  - Reference - https://github.com/tensorflow/codelabs

  - Can it be upgraded for larger models ?
  - API based - 
    - train with own data for evaluation

- On device Translation 
  - https://github.com/googlesamples/mlkit/tree/master/android/translate

- Nexa - https://github.com/NexaAI/Ocotpus-v2-demo


- llm_inference
    
  - git clone https://github.com/googlesamples/mediapipe
  - cd mediapipe
  - git sparse-checkout init --cone
  - git sparse-checkout set examples/llm_inference/android


  - Start android studio and Import project into android studio
  - Model download at
    - https://www.kaggle.com/models/google/gemma/tfLite/
  - Copy model to device using device explorer
    - https://developer.android.com/studio/debug/device-file-explorer
  - https://developers.googleblog.com/en/large-language-models-on-device-with-mediapipe-and-tensorflow-lite/
  - Convert models to tf-lite format 
    - https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/llm_inference/conversion/llm_conversion.ipynb
    - https://github.com/google-ai-edge/mediapipe-samples/blob/main/examples/llm_inference/conversion/llm_conversion.ipynb



- reference
  - https://github.com/google-ai-edge/mediapipe-samples
  - https://www.tensorflow.org/lite/examples
  - https://ai.google.dev/edge/lite
  - https://ai.google.dev/edge/mediapipe/solutions/genai/llm_inference

  - https://ai.google.dev/edge/mediapipe/solutions/genai/llm_inference/android
  - https://ai.google.dev/edge/mediapipe/solutions/setup_android#example_code

  - https://llm.mlc.ai/
  - https://www.youtube.com/watch?v=pNWNMPi0Mvk
  - https://keras.io/keras_nlp/
  - https://www.tensorflow.org/lite
  - https://ai.google.dev/gemma/docs/lora_tuning


- Bazel Build for mediapipe
  - https://bazel.build/install/ubuntu

  - Install bazel

  - Download bazel

  - wget https://github.com/bazelbuild/bazel/releases/download/7.3.0rc1/bazel-7.3.0rc1-installer-linux-x86_64.sh

  -  chmod +x bazel-7.3.0rc1-installer-linux-x86_64.sh
  -  ./bazel-7.3.0rc1-installer-linux-x86_64.sh --user

  -  add .bashrc
  -  export PATH="$PATH:$HOME/bin"

