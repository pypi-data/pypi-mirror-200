from ase import Atoms
from ase_extension import ase_extension as _ext


class RMSD:
    """Compute RMSD between two sets of atoms

    Args:
        ref_atoms: reference Atoms. The RMSD will be computed against this.
    """

    def __init__(self, ref_atoms: Atoms):
        self.ref_pos = ref_atoms.get_positions()
        self.rmsd = None
        self.rmsd_grad = None
        self.transform_ref = None

    def compute(self, atoms: Atoms, compute_gradient: bool = False):
        pos = atoms.positions
        rmsd_val, rmsd_grad, U, c = _ext.compute_minimum_rmsd(pos, self.ref_pos, compute_gradient)
        self.rmsd = rmsd_val
        self.rmsd_grad = rmsd_grad

        def transform(x):
            return x.dot(U) + c

        self.transform_ref = transform
        return rmsd_val
