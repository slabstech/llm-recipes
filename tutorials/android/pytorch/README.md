Pytorch Deployment

- Setup - Executorch
    - Setup virtual envrionment
        - python3.10 -m venv venv
        - source venv/bin/activate

    - git clone --branch v0.3.0 https://github.com/pytorch/executorch.git
    - cd executorch
    - git submodule sync   
    - git submodule update --init
    - ./install_requirements.sh

    - Build model 
        - python3 export_add.py


    - Build Tooling Setup (in executorch directory)
    - rm -rf cmake-out && mkdir cmake-out && cd cmake-out && cmake ..
    - cd ..

    - cmake --build cmake-out --target executor_runner -j9

    - ./cmake-out/executor_runner --model_path add.pte


- We generate the model file for the ExecuTorch runtime in Android Demo App.
    - XNNPACK Delegation
        - python3 -m examples.xnnpack.aot_compiler --model_name="dl3" --delegate
        - mkdir -p examples/demo-apps/android/ExecuTorchDemo/app/src/main/assets/
- Reference
  - https://github.com/pytorch/torchchat
  - https://github.com/pytorch/executorch
  - https://pytorch.org/executorch/stable/getting-started-setup.html#quick-setup-colab-jupyter-notebook-prototype
  - https://pytorch.org/executorch/stable/demo-apps-android.html
  - https://pytorch.org/executorch/stable/extension-module.html
  - https://pytorch.org/executorch/stable/build-run-qualcomm-ai-engine-direct-backend.html