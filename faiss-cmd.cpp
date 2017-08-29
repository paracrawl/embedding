#include <cassert>
#include <cstring>
#include <iostream>
#include <sys/stat.h>
#include "AutoTune.h"

using namespace std;

/*****************************************************
 * I/O functions for fvecs and ivecs
 *****************************************************/


float * fvecs_read (const char *fname,
                    size_t *d_out, size_t *n_out)
{
    FILE *f = fopen(fname, "r");
    if(!f) {
        fprintf(stderr, "could not open %s\n", fname);
        perror("");
        abort();
    }
    int d;
    fread(&d, 1, sizeof(int), f);
    assert((d > 0 && d < 1000000) || !"unreasonable dimension");
    fseek(f, 0, SEEK_SET);
    struct stat st;
    fstat(fileno(f), &st);
    size_t sz = st.st_size;
    assert(sz % ((d + 1) * 4) == 0 || !"weird file size");
    size_t n = sz / ((d + 1) * 4);

    *d_out = d; *n_out = n;
    float *x = new float[n * (d + 1)];
    size_t nr = fread(x, sizeof(float), n * (d + 1), f);
    assert(nr == n * (d + 1) || !"could not read whole file");

    // shift array to remove row headers
    for(size_t i = 0; i < n; i++)
        memmove(x + i * d, x + 1 + i * (d + 1), d * sizeof(*x));

    fclose(f);
    return x;
}


void Load(size_t &d)
{
  size_t nt;
  float *xt = fvecs_read("sift1M/sift_learn.fvecs", &d, &nt);

}

int main()
{
  cerr << "Starting..." << endl;

  // this is typically the fastest one.
  const char *index_key = "IVF4096,Flat";

  size_t d;

  Load(d);

  cerr << "Finished." << endl;
  return 0;
}

