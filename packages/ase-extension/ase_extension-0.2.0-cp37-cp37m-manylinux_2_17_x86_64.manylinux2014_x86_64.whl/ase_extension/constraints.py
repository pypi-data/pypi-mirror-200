from ase_extension import ase_extension as _ext


class LogFermiWallPotential:
    """Apply logfermi potential for confined molecular dynamics.
    Confines the system to be inside a sphere by applying wall potential.

    Method referenced from https://xtb-docs.readthedocs.io/en/latest/xcontrol.html#confining-in-a-cavity
    """

    def __init__(self, radius=5.0, temperature=300, beta=6):
        self.radius = radius
        self.temperature = temperature
        self.beta = beta

    def _get_wall_energy_and_force(self, pos):
        E, E_grad = _ext.log_fermi(pos, self.radius, self.temperature, self.beta)
        return E, -E_grad

    def adjust_forces(self, atoms, forces):
        E_wall, F_wall = self._get_wall_energy_and_force(atoms.positions)
        forces += F_wall

    def adjust_potential_energy(self, atoms):
        E_wall, F_wall = self._get_wall_energy_and_force(atoms.positions)
        return E_wall

    def adjust_positions(self, atoms, new):
        pass

    def get_removed_dof(self, atoms):
        return 0
