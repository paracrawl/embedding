
#define DIM 1024


#include <iostream>
#include <getopt.h>

#include "faiss/IndexFlat.h"
#include "faiss/index_io.h"


void search_index(faiss::Index* index, float *xb, int nb, int kbest) {
  long *I = new long[kbest * nb];
  float *D = new float[kbest * nb];
  (*index).search(nb, xb, kbest, D, I);

  for(int n = 0; n < nb; ++n) {
    for(int i = 0; i < kbest; ++i) {
      std::cout << I[i + n * kbest] << ":" << D[i + n * kbest] << " ";
    }
    std::cout << std::endl;
  }
}

faiss::Index* read_index(const char *file_path) {
  return faiss::read_index(file_path);
}

void print_usage() {
  fprintf(stderr, "Usage: \n -i: <index_file> \n -b: <batch_size> \n -k: <k_best> \n");
}


int main(int argc, char **argv) {
  std::string index_file;
  int opt;
  long kbest = -1;
  long batch_size = -1;

  // GETOPT
  if (argc < 2) {
    print_usage();
    return 1;
  }

  while ((opt = getopt(argc, argv, "i:b:k:h")) != EOF) {
    switch(opt)
    {
        case 'i':
          index_file = optarg;
          break;
        case 'b':
            batch_size = std::strtol(optarg, NULL, 10);;
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
  if (kbest == -1 || batch_size == -1 || index_file.length() == 0) {
    throw std::runtime_error("wrong arguments");
  }

  // LOAD INDEX FILE
  faiss::Index* index = read_index(index_file.c_str());

  // QUERY STDIN
  int col_pos;
  float *xb = new float[DIM * batch_size];

  long line_num = 0;
  for (std::string line; std::getline(std::cin, line);) {
    std::stringstream iss(line);
    float number;
    col_pos = 0;

    while (iss >> number && col_pos < DIM) {
      xb[(line_num % batch_size)*DIM + col_pos++] = number;
    }

    if (col_pos != DIM) {
      throw std::runtime_error("dimensionality broken - found: " + std::to_string(col_pos) + " expected: " + std::to_string(DIM));
    }

    if (line_num == batch_size - 1) {
      search_index(index, xb, batch_size, kbest);
      line_num = 0;
    } else {
      ++line_num;
    }
  }

  return 0;
}
