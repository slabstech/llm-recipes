CUDA_DIR := /usr/local/cuda-12.6

 all: myProgram

 square: square.o
	$(CUDA_DIR)/bin/nvcc -o $@ $^

 square.o: square.cu
	$(CUDA_DIR)/bin/nvcc -c -o $@ $<


 myProgram: main.o kernel.o
	$(CUDA_DIR)/bin/nvcc -o $@ $^

 main.o: main.cpp
	$(CUDA_DIR)/bin/nvcc -c -o $@ $<

 kernel.o: kernel.cu
	$(CUDA_DIR)/bin/nvcc -c -o $@ $<

 clean:
	rm -f myProgram.*
