from shenfun import *
from shenfun.optimization.cython import Leg2Cheb
config['optimization']['mode'] = 'cython'

#N = 1000000
#u = np.random.random(N)
#v = np.zeros_like(u)
#f = Leg2Cheb(u, v, diagonals=8, levels=3, maxs=100, use_direct=1000)
#v = f(u, v)
#
#C1 = legendre.dlt.FMMLeg2Cheb(N, diagonals=8, levels=3, maxs=100, use_direct=1000)
#a = np.zeros(N)
#a = C1(u, a)

M = 100
#u2 = np.random.random((M, M))
u2 = np.ones((M, M))
v2 = np.zeros_like(u2)
f2 = Leg2Cheb(u2, v2, axis=1, diagonals=8, maxs=100, use_direct=10)
v2 = f2(u2, v2, transpose=False)

C2 = legendre.dlt.FMMLeg2Cheb(u2, axis=1, diagonals=8, maxs=100, use_direct=10)
a = np.zeros((M, M))
a = C2(u2, a)
assert np.linalg.norm(v2-a) < 1e-8

v3 = np.zeros(M)
f0 = Leg2Cheb(u2[0], v3,  diagonals=8, maxs=100, use_direct=10)
v3 = f0(u2[0], v3)
assert np.linalg.norm(v3-a[0]) < 1e-8