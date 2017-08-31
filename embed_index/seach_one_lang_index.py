#!/usr/bin/env python2
# coding=utf-8

import argparse
import faiss
import sys
import torch.utils.serialization
import os
import logging

_logger = logging.getLogger(__name__)


def _init_log():
    fmt = '%(asctime)s | %(name)-20s | %(levelname).1s | %(message)s'
    logging.basicConfig(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def _parse_options():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument(
        '--index',
        default='/data/holger/europarl.un16lc/faiss-index/eparl7lu.efs.w50.en.efsraz-1allmd.BLSTM.1x512.max.@13.OPQ128,IVF16384,PQ128.norm.data.idx',
        help='faiss index of embeddings for _one_ language', )
    p.add_argument(
        '-d', '--dir',
        default='/data/holger/europarl.un16lc/embed.th7',
        help='embeddings directory', )
    p.add_argument(
        '-l', '--lang',
        required=True,
        help='embeddings language', )
    p.add_argument(
        '-o', '--output',
        required=True,
        help='where to put results (nearest neighbor index in index)', )
    return p.parse_args()


def _find_embedings(lang, dir_):
    n = '.' + lang + '.'
    e = []
    for name in os.listdir(dir_):
        if n not in name:
            continue
        e.append(os.path.join(dir_, name))

    return sorted(e)  # order of files is important!


def _load_index_to_gpu(path):
    _logger.info('loading index to RAM')
    cpu_index = faiss.read_index(a.index)
    return cpu_index

    # doesn't work with provided index for some reason:
    #
    # RuntimeError: Error in void faiss::gpu::GpuIndexIVFPQ::verifySettings_() const at
    # GpuIndexIVFPQ.cu:436: Error: 'IVFPQ::isSupportedPQCodeLength(subQuantizers_)' failed: Number
    # of bytes per encoded vector / sub-quantizers (128) is not supported

    gpu_res = faiss.StandardGpuResources()

    _logger.info('copying index to GPU')
    # TODO: use index_cpu_to_gpu_multiple
    gpu_index = faiss.index_cpu_to_gpu(gpu_res, 0, cpu_index)

    return gpu_index


def _main(a):
    _logger.info('loading faiss index')
    index = _load_index_to_gpu(a.index)
    res = []

    for path in _find_embedings(a.lang, a.dir):
        _logger.info('loading embeddings from %s', path)
        t = torch.utils.serialization.load_lua(path)

        _logger.info('searching index for embeddings')
        _, indices = index.search(x=t.numpy(), k=1)

        _logger.info('saving nearest neighbors')
        res.extend(i[0] for i in indices)

        del t

    _logger.info('saving search results')
    with open(a.output, 'wb') as out:
        for r in res:
            out.write(str(res))
            out.write('\n')


if '__main__' == __name__:
    _init_log()
    a = _parse_options()
    sys.exit(_main(a) or 0)
