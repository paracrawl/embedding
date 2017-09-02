# Embedding
Mine parallel corpora with embeddings

## sentence preprocessing

Tokenizes and normalizes all sentences with language-specific scripts. Also converts to lowercase and applies BPE .
```bash
./preprocess/prep.sh -l {language} -f {input_file} | gzip > {output_file}
```

## converting th7

Loads given t7 files and converts them into a compressed format that can be read as a stream.
```bash
cat {list_of_input_files} | python ./read_t7.py
```

## building index

Builds faiss index from the input stream. `-s` sets the number of sentences one index can hold. If the index size is exceeded, the index is outputted to `output_folder` and new index is processed.
```bash
cd index
mkdir -p build && cd build
cmake .. && make -j 5

zcat {embeddings_file}.gz | ./bin/build_index -o {output_folder} -s {index_size}
```

## querying index

Loads index from `index_file` and searches for `k` nearest vectors for each input vector. The search performed on an index is the k-nearest-neighbor search.
```bash
cd index
mkdir -p build && cd build
cmake .. && make -j 5

zcat {embeddings_file}.gz | ./bin/query_index -i {index_file} -k {k-best} > {output_file}
```
