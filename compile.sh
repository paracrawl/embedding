c++ -std=c++11 -fopenmp -lpthread -I../faiss -L../faiss faiss-cmd.cpp  -L/opt/intel/compilers_and_libraries/linux/mkl//lib/intel64 ../faiss/AutoTune.cpp -lfaiss -lmkl_intel_ilp64 -lmkl_core -lmkl_gnu_thread


