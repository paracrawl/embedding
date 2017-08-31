#!/usr/bin/env python2
# coding=utf-8

import argparse
import faiss
import sys
import torch.utils.serialization
import os
import logging

_logger = logging.getLogger(__name__)


def _parse_options():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument(
        '-l', '--lang',
        required=True,
        help='embeddings language to build index for', )
    p.add_argument(
        '-d', '--dir',
        default='/data/holger/europarl.un16lc/embed.th7',
        help='embeddings directory', )
    p.add_argument(
        '-o', '--output',
        required=True,
        help='where to save index', )
    return p.parse_args()


def _init_log():
    fmt = '%(asctime)s | %(name)-20s | %(levelname).1s | %(message)s'
    logging.basicConfig(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def _find_embedings(lang, dir_):
    n = '.' + lang + '.'
    e = []
    for name in os.listdir(dir_):
        if n not in name:
            continue
        e.append(os.path.join(dir_, name))

    return sorted(e)  # order of files is important!


def _build_index(embed_paths, use_gpu=True):
    # this is a good place to decide if we want to build index on cpu or on gpu
    gpu_res = faiss.StandardGpuResources()

    # this one should be retreived from the embeddings file, we also should check if all embeddings
    # have the same size
    embed_size = 1024

    index = faiss.GpuIndexFlatIP(gpu_res, embed_size)

    for path in embed_paths:
        _logger.info('loading embeddings from %s', path)
        t = torch.utils.serialization.load_lua(path)

        _logger.info('adding embeddings to the index')
        index.add(t.numpy())

    return index


def _main(a):
    embed_paths = _find_embedings(a.lang, a.dir)
    index = _build_index(embed_paths)
    faiss.write_index(index, a.output)


if '__main__' == __name__:
    _init_log()
    a = _parse_options()
    sys.exit(_main(a) or 0)
