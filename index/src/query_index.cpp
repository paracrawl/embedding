
#define DIM 1024


#include <iostream>
#include <getopt.h>

#include "faiss/IndexFlat.h"
#include "faiss/index_io.h"


void search_index(faiss::Index* index, float *xb, int kbest) {
  long *I = new long[kbest * 1];
  float *D = new float[kbest * 1];
  (*index).search(1, xb, kbest, D, I);

  for(int i = 0; i < kbest; ++i) {
    std::cout << I[i] << ":" << D[i] << " ";
  }
  std::cout << std::endl;
}

faiss::Index* read_index(const char *file_path) {
  return faiss::read_index(file_path);
}

void print_usage() {
  fprintf(stderr, "Usage: \n -i: <index_file> \n -k: <k_best> \n");
}


int main(int argc, char **argv) {
  std::string index_file;
  int opt;
  long kbest = -1;

  // GETOPT
  if (argc < 2) {
    print_usage();
    return 1;
  }

  while ((opt = getopt(argc, argv, "i:k:h")) != EOF) {
    switch(opt)
    {
        case 'i':
          index_file = optarg;
          break;
        case 'k':
          kbest = std::strtol(optarg, NULL, 10);;
          break;
        case 'h':
        default:
          print_usage();
          return 1;
    }
  }

  // check arguments
  if (kbest == -1 || index_file.length() == 0) {
    throw std::runtime_error("wrong arguments");
  }

  // LOAD INDEX FILE
  faiss::Index* index = read_index(index_file.c_str());

  // QUERY STDIN
  int col_pos;
  float *xb = new float[DIM];

  for (std::string line; std::getline(std::cin, line);) {
    std::stringstream iss(line);
    float number;
    col_pos = 0;

    while (iss >> number && col_pos < DIM) {
      xb[col_pos++] = number;
    }

    if (col_pos != DIM) {
      throw std::runtime_error("dimensionality broken - found: " + std::to_string(col_pos) + " expected: " + std::to_string(DIM));
    }

    search_index(index, xb, kbest);
  }

  return 0;
}
