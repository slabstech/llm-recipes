#include <stdio.h>
#include <cuda_runtime.h>

__global__ void myKernel(int n) {
  int idx = threadIdx.x + blockIdx.x * blockDim.x;
  if (idx < n) printf("Hello from thread %d\n", idx);
}
