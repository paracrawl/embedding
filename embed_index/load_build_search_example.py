#!/usr/bin/env python2
# encoding=utf-8

from __future__ import print_function

import argparse
import faiss
import torch
import torch.utils.serialization
import sys


def _parse_options():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument(
        '--embeddings',
        required=True,
        help='embeddings file, e.g. "eparl7lu.efs.w50.en.00.efsraz-1allmd.BLSTM.1x512.max.@13.embed"')
    return p.parse_args()


def _main(a):
    t = torch.utils.serialization.load_lua(a.embeddings)

    res = faiss.StandardGpuResources()
    index = faiss.GpuIndexFlatIP(res, t.size()[1])
    print('Building index...')
    sys.stdout.flush()
    index.add(x=t.numpy())

    print('Searching index...')
    sys.stdout.flush()
    print(index.search(x=t[7:8].numpy(), k=10))

    print('Done')
    sys.stdout.flush()


if '__main__' == __name__:
    a = _parse_options()
    sys.exit(_main(a) or 0)
