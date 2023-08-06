from typing import List, Literal, Union

import numpy as np
from ase import Atoms

from ase_extension import ase_extension as _ext


def _determine_parallel(atoms: Atoms) -> bool:
    n_atoms = len(atoms)
    if n_atoms < 20:
        return False
    return True


def neighbor_list(
    quantities: str,
    atoms: Atoms,
    cutoff: float,
    self_interaction: bool = False,
    parallel: Union[bool, Literal["auto"]] = "auto",
) -> List[np.ndarray]:
    """Construct neighbor list.
    Uses octree algorithm to find neighbors within cutoff distance with
    gchemol-neighbors crate written in rust.

    Args:
        quantities (str): combination of "i", "j", "d", "D", "S".
            - "i": indices of central atoms
            - "j": indices of neighbor atoms
            - "d": distances between central and neighbor atoms
            - "D": vectors between central and neighbor atoms
            - "S": shift(offset) vectors between central and neighbor atoms
            example: "ijD" -> returns [i, j, D]
        atoms (Atoms): ASE atoms object
        cutoff (float): cutoff distance
        self_interaction (bool, optional): whether to include self interaction.
            Defaults to False. Currently self interaction is not implemented.
        parallel (bool, optional): whether to use multi-threading. Defaults to "auto".
            If "auto", parallel is set to True if number of atoms is larger than 20.
    """
    if self_interaction:
        raise NotImplementedError("self_interaction is not implemented")
    parallel = _determine_parallel(atoms) if parallel == "auto" else parallel

    positions = atoms.get_positions()
    cell = atoms.get_cell().array
    pbc = np.any(atoms.get_pbc())
    if not pbc:
        cell = None

    i, j, d, S = _ext.neighbor_list(positions, cell, cutoff, parallel)
    results = {"i": i, "j": j, "d": d, "S": S}
    if "D" in quantities:
        results["D"] = positions[j] - positions[i] + S @ cell

    return [results[q] for q in quantities]
