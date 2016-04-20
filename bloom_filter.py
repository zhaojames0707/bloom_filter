#!/usr/bin/env python
# coding=utf-8
import hashlib


class BloomFilter(object):

    def __init__(self, m, n, k=None):
        if not k:
            k = int(0.7 * (float(m) / n))
        self._bit_map = 0
        self.m = m
        self.n = n
        self.k = k
        self._init_hash_funcs()

    def insert(self, obj):
        for hash_func in self._hash_funcs:
            self._bit_map |= 1 << hash_func(obj)

    def __contains__(self, obj):
        for hash_func in self._hash_funcs:
            if not self._bit_map & (1 << hash_func(obj)):
                return False
        return True

    def _init_hash_funcs(self):
        self._hash_funcs = []
        for i in range(self.k):
            salt = hex(i)[2:]
            hash_func = lambda s: int(
                hashlib.md5(s).hexdigest() + salt,
                base=16) % self.m
            self._hash_funcs.append(hash_func)

    def clear(self):
        self._bit_map = 0
        self._hash_funcs = []

if __name__ == '__main__':
    f = BloomFilter(10000, 10, 7)
    l = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    for i in l:
        f.insert(i)
    print('b' in f)
    print('x' in f)
    print('y' in f)
    print('1' in f)
    print('a' in f)
