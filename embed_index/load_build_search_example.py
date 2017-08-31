#!/usr/bin/env python2
# encoding=utf-8

from __future__ import print_function

import argparse
import faiss
import gzip
import itertools
import sys
import torch
import torch.utils.serialization


def _parse_options():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument(
        '--embeddings',
        default='/data/holger/europarl.un16lc/embed.th7/eparl7lu.efs.w50.en.00.efsraz-1allmd.BLSTM.1x512.max.@13.embed',
        help='embeddings file, e.g. "eparl7lu.efs.w50.en.00.efsraz-1allmd.BLSTM.1x512.max.@13.embed"')
    p.add_argument(
        '--sentences',
        default='/data/holger/europarl.un16lc/data.norm.un6lc/eparl7lu.efs.w50.en.gz',
        help=('sentences (order of the lines and embeddings is expected to be identical), e.g.' +
              ' "eparl7lu.efs.w50.en.gz"'))
    p.add_argument(
        '--offset',
        default=0,
        help='embeddings file offset (0 for the example emddings file)')
    p.add_argument(
        '--sent-index',
        default=100500,
        help='sentence index to search for', )
    p.add_argument(
        '-k',
        default=10,
        help='number of nearest neighbors to search for', )
    return p.parse_args()


def _open(path, mode):
    if path.endswith('.gz'):
        return gzip.open(path, mode)
    return open(path, mode)


def _main(a):
    print('Loading embeddings...')
    sys.stdout.flush()
    t = torch.utils.serialization.load_lua(a.embeddings)

    print('Loading sentences...')
    sys.stdout.flush()
    sent = _open(a.sentences, 'rb').readlines()

    res = faiss.StandardGpuResources()
    index = faiss.GpuIndexFlatIP(res, t.size()[1])
    print('Building index on GPU...')
    sys.stdout.flush()
    index.add(x=t.numpy())

    print('Searching index...')
    sys.stdout.flush()
    distances, indices = index.search(x=t[a.sent_index:a.sent_index + 1].numpy(), k=a.k)

    print('Searched for: "{}"'.format(sent[a.sent_index].encode('string-escape')))
    print('Nearest neighbors (distance \\t index \\t sentence):')
    for d, i in itertools.izip(distances[0], indices[0]):
        j = i + a.offset
        c_sentence = sent[j].encode('string-escape')
        print('{dist:.2f}\t{index}\t"{sentence}"'.format(dist=d, index=j, sentence=c_sentence))
    sys.stdout.flush()

    print('Done')
    sys.stdout.flush()


if '__main__' == __name__:
    a = _parse_options()
    sys.exit(_main(a) or 0)
