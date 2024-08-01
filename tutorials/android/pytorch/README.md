Pytorch Deployment


Failed for 
  - armeabi-v7a  - Emulator
  - Samsung a13

Works on emulator
  - x86_64  
 - https://developer.android.com/ndk/guides/abis

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
        - cp deeplab_v3/dlv3_qnn.pte examples/demo-apps/android/ExecuTorchDemo/app/src/main/assets/



Runtime

We build the required ExecuTorch runtime library to run the model.

1.  Build the CMake target for the library with XNNPACK backend
export ANDROID_NDK=/home/sachin/Android/Sdk/ndk/27.0.12077973

 export ANDROID_ABI=armeabi-v7a
//  export ANDROID_ABI=x86_64


 - #### Build the core executorch library
cmake . -DCMAKE_INSTALL_PREFIX=cmake-android-out \
  -DCMAKE_TOOLCHAIN_FILE="${ANDROID_NDK}/build/cmake/android.toolchain.cmake" \
  -DANDROID_ABI="${ANDROID_ABI}" \
  -DEXECUTORCH_BUILD_XNNPACK=ON \
  -DEXECUTORCH_BUILD_EXTENSION_DATA_LOADER=ON \
  -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON \
  -Bcmake-android-out

cmake --build cmake-android-out -j16 --target install


2. Build the Android extension 

#### Build the android extension
cmake extension/android \
  -DCMAKE_TOOLCHAIN_FILE="${ANDROID_NDK}"/build/cmake/android.toolchain.cmake \
  -DANDROID_ABI="${ANDROID_ABI}" \
  -DCMAKE_INSTALL_PREFIX=cmake-android-out \
  -Bcmake-android-out/extension/android

cmake --build cmake-android-out/extension/android -j16

-

 mkdir -p examples/demo-apps/android/ExecuTorchDemo/app/src/main/jniLibs/arm64-v8a

// mkdir -p examples/demo-apps/android/ExecuTorchDemo/app/src/main/jniLibs/x86_64


 cp cmake-android-out/extension/android/libexecutorch_jni.so \
   examples/demo-apps/android/ExecuTorchDemo/app/src/main/jniLibs/arm64-v8a/libexecutorch.so

// cp cmake-android-out/extension/android/libexecutorch_jni.so \
   examples/demo-apps/android/ExecuTorchDemo/app/src/main/jniLibs/x86_64/libexecutorch.so


- Reference
  - https://github.com/pytorch/torchchat
  - https://github.com/pytorch/executorch
  - https://pytorch.org/executorch/stable/getting-started-setup.html#quick-setup-colab-jupyter-notebook-prototype
  - https://pytorch.org/executorch/stable/demo-apps-android.html
  - https://pytorch.org/executorch/stable/extension-module.html
  - https://pytorch.org/executorch/stable/build-run-qualcomm-ai-engine-direct-backend.html