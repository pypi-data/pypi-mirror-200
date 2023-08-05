import sympy as sp
import numpy as np
import scipy.special as sc
from scipy.special import jv
from shenfun.matrixbase import SparseMatrix
from shenfun.spectralbase import SpectralBase, getCompositeBase, getBCGeneric, BoundaryConditions

#pylint: disable=method-hidden,no-else-return,not-callable,abstract-method,no-member,cyclic-import

bases = ['Orthogonal',
         'CompactDirichlet']
bcbases = []
testbases = []
__all__ = bases + bcbases

xp = sp.Symbol('x', real=True)


class Orthogonal(SpectralBase):
    r"""Function space for a regular Bessel series

    The orthogonal basis is the Fourier-Bessel function of order 0

    .. math::

        \phi_k(x) = J_0(\lambda_k x/b), \quad k = 0, 1, \ldots, N-1,

    where :math:`\lambda_k` is the :math:`k`'th root of :math:`J_0(x)`
    and the domain is :math:`x\in [0, b]`.

    Parameters
    ----------
    N : int
        Number of quadrature points
    padding_factor : float, optional
        Factor for padding backward transforms.
    dealias_direct : bool, optional
        Set upper 1/3 of coefficients to zero before backward transform
    dtype : data-type, optional
        Type of input data in real physical space. Will be overloaded when
        basis is part of a :class:`.TensorProductSpace`.
    coordinates: 2- or 3-tuple (coordinate, position vector (, sympy assumptions)), optional
        Map for curvilinear coordinatesystem, and parameters to :class:`~shenfun.coordinates.Coordinates`

    Note
    ----
    We are using Fourier-Bessel functions and not the regular Bessel functions.

    """
    def __init__(self, N, dtype=float, padding_factor=1, dealias_direct=False,
                 domain=(0, 1), coordinates=None, **kw):
        SpectralBase.__init__(self, N, quad="BG", domain=domain, dtype=dtype,
                              padding_factor=padding_factor, dealias_direct=dealias_direct,
                              coordinates=coordinates)
        self.zeros = np.array([sc.jn_zeros(n, N) for n in range(N)])
        self.plan(int(N*padding_factor), 0, dtype, {})

    @staticmethod
    def family():
        return 'bessel'

    def reference_domain(self):
        return (0, 1)

    def points_and_weights(self, N=None, map_true_domain=False, weighted=True, **kw):
        if N is None:
            N = self.shape(False)
        assert self.quad == "BG"
        points = np.linspace(0, 1, self.N)
        weights = None

        if weighted:
            pass
        else:
            raise NotImplementedError

        return points, weights

    def vandermonde(self, x):
        if x is None:
            x = self.mesh(False, False)
        V = np.zeros((x.shape[0], self.N))
        for i in range(self.dim()):
            f = self.orthogonal_basis_function(i, x=xp)
            V[:, i] = sp.lambdify(xp, f)(x)
        return V

    @staticmethod
    def bnd_values(k=0, **kw):
        if k == 0:
            return (lambda i: int(i==0), None)
        elif k == 1:
            return (lambda i: 0, None)
        raise NotImplementedError

    def stencil_matrix(self, N=None):
        N = self.N if N is None else N
        return SparseMatrix({0: 1}, (N, N))

    def eval(self, x, u, output_array=None):
        x = np.atleast_1d(x)
        raise NotImplementedError

    def orthogonal_basis_function(self, i=0, x=xp):
        lambdai = self.zeros[i, -1]
        return sp.besselj(i, x*lambdai/self.domain[1])

    def L2_norm_sq(self, i):
        lambdai = self.zeros[i, -1]
        return sp.Rational(1, 2)*sp.besselj(i+1, lambdai)**2

    def l2_norm_sq(self, i=None):
        raise NotImplementedError

    def weight(self, x=xp):
        return x

    @property
    def is_orthogonal(self):
        return True

    def get_orthogonal(self, **kwargs):
        d = dict(quad=self.quad,
                 domain=self.domain,
                 dtype=self.dtype,
                 padding_factor=self.padding_factor,
                 dealias_direct=self.dealias_direct,
                 coordinates=self.coors.coordinates)
        d.update(kwargs)
        return Orthogonal(self.N, **d)

    @staticmethod
    def short_name():
        return 'Jn'

    #def get_bc_space(self):
    #    if self._bc_space:
    #        return self._bc_space
    #    self._bc_space = BCGeneric(self.N, bc=self.bcs)
    #    return self._bc_space

CompositeBase = getCompositeBase(Orthogonal)
#BCGeneric = getBCGeneric(CompositeBase)

class CompactDirichlet(CompositeBase):
    r"""Laguerre function space for Dirichlet boundary conditions

    The basis :math:`\{\phi_k\}_{k=0}^{N-1}` is

    .. math::

        \phi_k &= (La_k - La_{k+1})\exp(-x/2), \, k=0, 1, \ldots, N-2, \\
        \phi_{N-1} &= L_0\exp(-x/2),

    such that

    .. math::
        u(x) &= \sum_{k=0}^{N-1} \hat{u}_k \phi_k(x), \\
        u(0) &= a

    The last basis function is for boundary condition and only used if a is
    different from 0. In one dimension :math:`\hat{u}_{N-1}=a`.

    Parameters
    ----------
    N : int
        Number of quadrature points
    quad : str, optional
        Type of quadrature

        - LG - Laguerre-Gauss
    bc : 1-tuple of number (a,)
        Boundary value at x=0
    padding_factor : float, optional
        Factor for padding backward transforms.
    dealias_direct : bool, optional
        Set upper 1/3 of coefficients to zero before backward transform
    dtype : data-type, optional
        Type of input data in real physical space. Will be overloaded when
        basis is part of a :class:`.TensorProductSpace`.
    coordinates: 2- or 3-tuple (coordinate, position vector (, sympy assumptions)), optional
        Map for curvilinear coordinatesystem, and parameters to :class:`~shenfun.coordinates.Coordinates`

    """
    def __init__(self, N, bc=(0,), dtype=float, padding_factor=1,
                 dealias_direct=False, coordinates=None, **kw):
        CompositeBase.__init__(self, N, quad='LG', dtype=dtype, padding_factor=padding_factor,
                               bc=bc, dealias_direct=dealias_direct, domain=(0, sp.S.Infinity),
                               coordinates=coordinates)
        self._stencil = {0: 1, 1: -1}

    @staticmethod
    def boundary_condition():
        return 'Dirichlet'

    @staticmethod
    def short_name():
        return 'SD'

#
#class CompactNeumann(CompositeBase):
#    r"""Laguerre function space for Dirichlet boundary conditions
#
#    The basis :math:`\{\phi_k\}_{k=0}^{N-1}` is
#
#    .. math::
#        \phi_k &= (La_k - \frac{2k+1}{2k+3}La_{k+1})\exp(-x/2), \, k=0, 1, \ldots, N-2, \\
#        \phi_{N-1} &= La_0\exp(-x/2),
#
#    such that
#
#    .. math::
#        u(x) &= \sum_{k=0}^{N-1} \hat{u}_k \phi_k(x), \\
#        u'(0) &= a
#
#    Parameters
#    ----------
#    N : int
#        Number of quadrature points
#    quad : str, optional
#        Type of quadrature
#
#        - LG - Laguerre-Gauss
#    bc : 1-tuple of number (a,)
#        Boundary value a = u'(0)
#    padding_factor : float, optional
#        Factor for padding backward transforms.
#    dealias_direct : bool, optional
#        Set upper 1/3 of coefficients to zero before backward transform
#    dtype : data-type, optional
#        Type of input data in real physical space. Will be overloaded when
#        basis is part of a :class:`.TensorProductSpace`.
#    coordinates: 2- or 3-tuple (coordinate, position vector (, sympy assumptions)), optional
#        Map for curvilinear coordinatesystem, and parameters to :class:`~shenfun.coordinates.Coordinates`
#
#    """
#    def __init__(self, N, bc=(0,), dtype=float, padding_factor=1,
#                 dealias_direct=False, coordinates=None, **kw):
#        if isinstance(bc, (tuple, list)):
#            assert len(bc) == 1
#            bc = BoundaryConditions({'left': {'N': bc[0]}, 'right': {}}, domain=(0, np.inf))
#        CompositeBase.__init__(self, N, dtype=dtype, quad='LG', padding_factor=padding_factor,
#                               bc=bc, dealias_direct=dealias_direct, domain=(0, sp.S.Infinity),
#                               coordinates=coordinates)
#        self._stencil = {0: 1, 1: -(2*n+1)/(2*n+3)}
#
#    @staticmethod
#    def boundary_condition():
#        return 'Neumann'
#
#    @staticmethod
#    def short_name():
#        return 'CN'
#
#
#class Generic(CompositeBase):
#    r"""Function space for Laguerre space with any boundary conditions
#
#    Any combination of Dirichlet and Neumann is possible.
#
#    Parameters
#    ----------
#    N : int, optional
#        Number of quadrature points
#    quad : str, optional
#        Type of quadrature
#
#        - LG - Laguerre-Gauss
#
#    bc : dict, optional
#        The dictionary must have key 'left' (not 'right'), to describe boundary
#        conditions on the left boundary. Specify Dirichlet with
#
#            {'left': {'D': a}}
#
#        for some value `a`, that will be neglected in the current
#        function. Specify mixed Neumann and Dirichlet as
#
#            {'left': {'D': a, 'N': b}}
#
#        See :class:`~shenfun.spectralbase.BoundaryConditions`.
#    domain : 2-tuple of floats, optional
#        The computational domain
#    dtype : data-type, optional
#        Type of input data in real physical space. Will be overloaded when
#        basis is part of a :class:`.TensorProductSpace`.
#    padding_factor : float, optional
#        Factor for padding backward transforms.
#    dealias_direct : bool, optional
#        Set upper 1/3 of coefficients to zero before backward transform
#    coordinates: 2- or 3-tuple (coordinate, position vector (, sympy assumptions)), optional
#        Map for curvilinear coordinatesystem, and parameters to :class:`~shenfun.coordinates.Coordinates`
#
#    """
#    def __init__(self, N, quad="LG", bc={}, domain=(0, sp.S.Infinity), dtype=float,
#                 padding_factor=1, dealias_direct=False, coordinates=None, **kw):
#        from shenfun.utilities.findbasis import get_stencil_matrix
#        self._stencil = get_stencil_matrix(bc, 'laguerre')
#        if not isinstance(bc, BoundaryConditions):
#            bc = BoundaryConditions(bc, domain=domain)
#        CompositeBase.__init__(self, N, quad=quad, domain=domain, dtype=dtype, bc=bc,
#                               padding_factor=padding_factor, dealias_direct=dealias_direct,
#                               coordinates=coordinates)
#
#    @staticmethod
#    def boundary_condition():
#        return 'Generic'
#
#    @staticmethod
#    def short_name():
#        return 'GL'
