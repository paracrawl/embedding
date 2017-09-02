
#define DIM 1024


#include <iostream>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>
#include <ctype.h>
#include <getopt.h>

#include "faiss/IndexFlat.h"
#include "faiss/index_io.h"



void construct_index(faiss::IndexFlatL2* index, float *xb, int nb){
  printf("is_trained = %s\n", (*index).is_trained ? "true" : "false");
  (*index).add(nb, xb);
  printf("ntotal = %ld\n", (*index).ntotal);
}

void write_index(faiss::IndexFlatL2* index, const char* fname){
  faiss:write_index(index, fname);
}

void construct_and_write_index(std::string output_folder, int id, float *xb, int row_pos) {
  std::string tmp = output_folder + "/faiss_" + std::to_string(id) + ".idx";
  const char *outfilename = tmp.c_str();
  printf(">> building index in: %s\n", tmp.c_str());

  faiss::IndexFlatL2 index(DIM);
  construct_index(&index, xb, row_pos);
  faiss::write_index(&index, outfilename);
}

void print_usage() {
  fprintf(stderr, "Usage: \n -o: <output_folder> \n -s: <index_size> \n");
}


int main(int argc, char **argv) {
  std::string output_folder = "";
  long index_size = -1;
  int opt;

  // GETOPT
  if (argc < 3) {
    print_usage();
    return 1;
  }

  while ((opt = getopt(argc, argv, "o:s:h")) != EOF) {
    switch(opt)
    {
        case 'o':
          output_folder = optarg;
          break;
        case 's':
          index_size = std::strtol(optarg, NULL, 10);
          break;
        case 'h':
        default:
          print_usage();
          return 1;
    }
  }

  // check arguments
  if (index_size == -1 || output_folder.length() == 0) {
    throw std::runtime_error("wrong arguments");
  }

  float *xb = new float[DIM * index_size];

  // BUILD INDEX FILES FROM STDIN
  int id = 0;
  int row_pos = 0;
  for (std::string line; std::getline(std::cin, line);) {
    std::stringstream iss(line);
    float number;
    int col_pos = 0;
    while (iss >> number) {
      if (col_pos > DIM-1) {
        throw std::runtime_error("dimensionality broken - reached: " + std::to_string(col_pos));
      }
      xb[DIM*row_pos + col_pos] = number;
      ++col_pos;
    }

    if (col_pos != DIM) {
      throw std::runtime_error("dimensionality broken - found: " + std::to_string(col_pos) + " expected: " + std::to_string(DIM));
    }

    ++row_pos;
    if (row_pos == index_size) {
      construct_and_write_index(output_folder, id, xb, row_pos);
      row_pos = 0;
      ++id;
    }
  }

  construct_and_write_index(output_folder, id, xb, row_pos);

  return 0;
}
