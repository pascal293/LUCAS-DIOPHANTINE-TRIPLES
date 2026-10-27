#!/usr/bin/env python3
"""
Exhaustive search for Diophantine triples with values in the generalized
Lucas sequences L_n(s):  L_0 = 2, L_1 = 1, L_{n+2} = L_{n+1} + s L_n.

A triple is a set {a,b,c}, 1 <= a < b < c, with
    ab+1 = L_x,  ac+1 = L_y,  bc+1 = L_z,   2 <= x < y < z <= N.
Exact integer arithmetic only (no floating point).

Usage:  python3 lucas_triples_search.py N S_MAX
"""
import sys
from math import isqrt

def lucas(s, n_max):
    L = [2, 1]
    for n in range(2, n_max + 1):
        L.append(L[-1] + s * L[-2])
    return L

def triples_for(s, n_max):
    L = lucas(s, n_max)
    M = [v - 1 for v in L]          # M[n] = L_n - 1  (> 0 for n >= 2)
    values = {v: i for i, v in enumerate(L) if i >= 2}
    found = []
    for z in range(4, n_max + 1):
        for y in range(3, z):
            for x in range(2, y):
                num = M[x] * M[y]
                if num % M[z]:
                    continue
                q = num // M[z]                  # must equal a^2
                a = isqrt(q)
                if a * a != q:
                    continue
                if M[x] % a or M[y] % a:
                    continue
                b, c = M[x] // a, M[y] // a
                if not (1 <= a < b < c):
                    continue
                # independent verification of the three equations
                assert a * b + 1 == L[x] and a * c + 1 == L[y] and b * c + 1 == L[z]
                found.append((a, b, c, x, y, z))
    return found

def is_pow2(v):
    return v > 0 and v & (v - 1) == 0

if __name__ == "__main__":
    n_max, s_max = int(sys.argv[1]), int(sys.argv[2])
    for s in range(1, s_max + 1):
        t = triples_for(s, n_max)
        if s == 2:
            non_pow2 = [u for u in t if not all(is_pow2(v) for v in u[:3])]
            print(f"s=2: {len(t)} triples, not all powers of two: {len(non_pow2)}")
        elif t:
            print(f"s={s}: {t}")
    print(f"done: 1<=s<={s_max}, 2<=x<y<z<={n_max}")
