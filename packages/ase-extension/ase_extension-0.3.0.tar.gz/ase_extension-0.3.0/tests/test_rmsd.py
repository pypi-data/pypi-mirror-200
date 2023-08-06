import jax
import jax.numpy as jnp
import numpy as np
from ase import Atoms
from jax.config import config
import pytest

from ase_extension.geometry import RMSD

config.update("jax_enable_x64", True)


@jax.jit
def rmsd_jax(P: jax.Array, Q: jax.Array):
    P, Q = Q, P
    centroid_P, centroid_Q = P.mean(axis=0), Q.mean(axis=0)
    P_c, Q_c = P - centroid_P, Q - centroid_Q
    H = P_c.T @ Q_c
    U, S, Vt = jnp.linalg.svd(H, full_matrices=False)
    V = Vt.T
    d = jnp.sign(jnp.linalg.det(V @ U.T))
    M = jnp.eye(3).at[2, 2].multiply(d)
    R = V @ M @ U.T
    # Find translation vectors
    t = centroid_Q[None, :] - (R @ centroid_P[None, :].T).T
    t = t.T.squeeze()
    ref0 = (R @ P.T).T + t
    rmsd = jnp.sqrt(jnp.sum((ref0 - Q) ** 2, axis=1).mean())
    return rmsd


@pytest.mark.parametrize("task", ["value", "gradient"])
def test_rmsd(task):
    P = np.random.rand(100, 3) * 10
    Q = np.random.rand(100, 3) * 10
    atoms_1 = Atoms("100H", positions=P)
    atoms_2 = Atoms("100H", positions=Q)

    rmsd_calc = RMSD(atoms_2)
    compute_gradient = task == "gradient"
    rmsd = rmsd_calc.compute(atoms_1, compute_gradient=compute_gradient)
    if task == "value":
        rmsd_ref = np.asarray(rmsd_jax(P, Q))
        assert np.allclose(rmsd, rmsd_ref)
    elif task == "gradient":
        rmsd_grad = rmsd_calc.rmsd_grad
        rmsd_grad_ref = np.asarray(jax.grad(rmsd_jax)(P, Q))
        assert np.allclose(rmsd_grad, rmsd_grad_ref)
