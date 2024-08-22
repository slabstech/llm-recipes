#include <cuda_runtime.h>
#include "kernel.cu"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
  printf("first program in CUDA cpp");
  myKernel<<<1, n>>>(n);
  cudaDeviceSynchronize();
  return 0;
}
