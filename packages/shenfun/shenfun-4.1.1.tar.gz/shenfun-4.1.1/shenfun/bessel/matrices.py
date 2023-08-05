from shenfun.matrixbase import SpectralMatrix, SpectralMatDict
from shenfun.spectralbase import get_norm_sq
from . import bases

CD = bases.CompactDirichlet
J = bases.Orthogonal

class BJJmat(SpectralMatrix):
    r"""Mass matrix :math:`B=(b_{kj}) \in \mathbb{R}^{M \times N}`, where

    .. math::

        b_{kj}=(J_k(x \lambda_k), J_k(x \lambda_j))_w,

    where the Bessel function :math:`J_k(x \lambda_k) \in` :class:`.bases.Orthogonal`,
    and test and trial spaces have dimensions of M and N, respectively.

    """
    def __init__(self, test, trial, scale=1, measure=1, assemble=None, kind=None, fixed_resolution=None):
        assert isinstance(test[0], J)
        assert isinstance(trial[0], J)
        SpectralMatrix.__init__(self, test, trial, scale=scale, measure=measure, assemble=assemble, kind=kind, fixed_resolution=fixed_resolution)

    def assemble(self, method):
        test, trial = self.testfunction, self.trialfunction
        return {0: get_norm_sq(test[0], trial[0], method)}


mat = SpectralMatDict({
    ((J, 0), (J, 0)): BJJmat
    })
