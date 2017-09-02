#!/usr/bin/env python2

import os
import sys
import torch.utils.serialization
import gzip


outout_folder = "/data/holger/europarl.un16lc/embed_extracted"

for filepath in sys.stdin:
    filepath = filepath.strip()
    loaded = torch.utils.serialization.load_lua(filepath)
    with gzip.open("{0}/{1}.gz".format(outout_folder, os.path.basename(filepath)), "wb") as f:
        print("> Extracting file: {0}".format(os.path.basename(filepath)))
        line_num = 0
        for line in loaded:
            line_num += 1
            if (line_num % 10000 == 0):
                print(line_num)

            for col in line:
                f.write("{0:.2f} ".format(float(col)))
            f.write("\n")
