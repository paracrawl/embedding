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

// not very clean, but works as long as sizeof(int) == sizeof(float)
int *ivecs_read(const char *fname, size_t *d_out, size_t *n_out)
{
    return (int*)fvecs_read(fname, d_out, n_out);
}

///////////////////////////////////////////////////////////////////////////////////////
faiss::Index * LoadData(size_t &d, const char *index_key)
{
   //printf ("[%.3f s] Loading train set\n", elapsed() - t0);

   size_t nt;
   float *xt = fvecs_read("sift1M/sift_learn.fvecs", &d, &nt);

  faiss::Index * index;
  //printf ("[%.3f s] Preparing index \"%s\" d=%ld\n",
  //        elapsed() - t0, index_key, d);
  index = faiss::index_factory(d, index_key);

  //printf ("[%.3f s] Training on %ld vectors\n", elapsed() - t0, nt);

  index->train(nt, xt);
  delete [] xt;

  return index;
}

///////////////////////////////////////////////////////////////////////////////////////
void LoadDb(const size_t &d,faiss::Index *index)
{
  //printf ("[%.3f s] Loading database\n", elapsed() - t0);

  size_t nb, d2;
  float *xb = fvecs_read("sift1M/sift_base.fvecs", &d2, &nb);
  assert(d == d2 || !"dataset does not have same dimension as train set");

  //printf ("[%.3f s] Indexing database, size %ld*%ld\n",
  //        elapsed() - t0, nb, d);

  index->add(nb, xb);

  delete [] xb;

}

///////////////////////////////////////////////////////////////////////////////////////
size_t LoadQueries(const size_t &d)
{
  size_t nq;
  float *xq;

  size_t d2;
  xq = fvecs_read("sift1M/sift_query.fvecs", &d2, &nq);
  assert(d == d2 || !"query does not have same dimension as train set");

  return nq;
}

///////////////////////////////////////////////////////////////////////////////////////
void LoadGroundTruths(const size_t &nq)
{
  size_t k; // nb of results per query in the GT
  faiss::Index::idx_t *gt;  // nq * k matrix of ground-truth nearest-neighbors

  //printf ("[%.3f s] Loading ground truth for %ld queries\n",
  //        elapsed() - t0, nq);

  // load ground-truth and convert int to long
  size_t nq2;
  int *gt_int = ivecs_read("sift1M/sift_groundtruth.ivecs", &k, &nq2);
  assert(nq2 == nq || !"incorrect nb of ground truth entries");

  gt = new faiss::Index::idx_t[k * nq];
  for(int i = 0; i < k * nq; i++) {
      gt[i] = gt_int[i];
  }
  delete [] gt_int;
}

///////////////////////////////////////////////////////////////////////////////////////

int main()
{
  cerr << "Starting..." << endl;

  // this is typically the fastest one.
  const char *index_key = "IVF4096,Flat";

  size_t d;

  faiss::Index *index = LoadData(d, index_key);
  LoadDb(d, index);
  
  size_t nq = LoadQueries(d);

  cerr << "Finished." << endl;
  return 0;
}

