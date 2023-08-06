from pathlib import Path

import ase.io
import numpy as np
import pytest
from ase.neighborlist import neighbor_list as ase_neighbor_list

from ase_extension.neighborlist import neighbor_list as ase_extension_neighbor_list

datapath = Path(__file__).absolute().parent / "data"


def sort_edge_index(idx_i, idx_j, *values):
    idx_i = np.asarray(idx_i)
    idx_j = np.asarray(idx_j)
    new_values = [v.copy() for v in values]
    for i in range(len(new_values)):
        new_values[i] = np.asarray(new_values[i])

    sort_idx = np.argsort(idx_i)
    idx_i = idx_i[sort_idx]
    idx_j = idx_j[sort_idx]
    for i in range(len(new_values)):
        new_values[i] = new_values[i][sort_idx]

    n_nodes = int(idx_i.max() + 1)
    for i in range(n_nodes):
        mask = idx_i == i
        sort_idx = np.argsort(idx_j[mask])
        idx_j[mask] = idx_j[mask][sort_idx]
        for i in range(len(new_values)):
            new_values[i][mask] = new_values[i][mask][sort_idx]
    return idx_i, idx_j, new_values


@pytest.mark.parametrize("cutoff", [1.0, 3.0, 5.0])
def test_neighborlist(cutoff):
    atoms = ase.io.read(datapath / "water_box_triclinic.vasp")
    pos = atoms.get_positions()
    i_ase, j_ase, d_ase, D_ase, S_ase = ase_neighbor_list("ijdDS", atoms, cutoff, self_interaction=False)
    i_ext, j_ext, d_ext, D_ext, S_ext = ase_extension_neighbor_list("ijdDS", atoms, cutoff, self_interaction=False)

    i_ase, j_ase, (d_ase, D_ase, S_ase) = sort_edge_index(i_ase, j_ase, d_ase, D_ase, S_ase)
    i_ext, j_ext, (d_ext, D_ext, S_ext) = sort_edge_index(i_ext, j_ext, d_ext, D_ext, S_ext)

    # Test equivalence
    assert np.allclose(i_ase, i_ext)
    assert np.allclose(j_ase, j_ext)
    assert np.allclose(d_ase, d_ext)
    # Test offsets
    D_from_shift = pos[j_ext] - pos[i_ext] + S_ext @ atoms.cell.array
    d_from_shift = np.linalg.norm(D_from_shift, axis=1)
    assert np.allclose(D_ext, D_from_shift)
    assert np.allclose(d_ext, d_from_shift)
