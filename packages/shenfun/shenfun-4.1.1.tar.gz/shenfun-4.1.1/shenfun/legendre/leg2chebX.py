from shenfun import *
import sympy as sp

x = sp.Symbol('x', real=True)
N = 100
omegax = sp.exp(sp.loggamma(x + sp.S.Half) - sp.loggamma(x + 1))
T = FunctionSpace(N, 'C')
L = FunctionSpace(N, 'L')
M = inner(TestFunction(T), TrialFunction(L))
k0 = 26
T0 = FunctionSpace(25, 'C', domain=[k0, N-1])
m0 = Array(T0, buffer=omegax)
T1 = FunctionSpace(25, 'C', domain=[k0-2, N-3])
m1 = Array(T1, buffer=omegax)
T2 = FunctionSpace(25, 'C', domain=[k0-4, N-5])
m2 = Array(T2, buffer=omegax)
