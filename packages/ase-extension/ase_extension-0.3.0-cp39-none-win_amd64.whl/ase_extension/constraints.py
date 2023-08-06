from abc import ABCMeta, abstractmethod

from ase_extension import ase_extension as _ext


class BiasPotential(metaclass=ABCMeta):
    @abstractmethod
    def _get_wall_energy_and_force(self, atoms):
        pass

    def adjust_forces(self, atoms, forces):
        _, F_wall = self._get_wall_energy_and_force(atoms)
        forces += F_wall

    def adjust_potential_energy(self, atoms):
        E_wall, _ = self._get_wall_energy_and_force(atoms)
        return E_wall

    def adjust_positions(self, atoms, new):
        pass

    def get_removed_dof(self, atoms):
        return 0


class LogFermiSphericalWallPotential(BiasPotential):
    """Apply logfermi potential for confined molecular dynamics.
    Confines the system to be inside a sphere by applying wall potential.

    Method referenced from https://xtb-docs.readthedocs.io/en/latest/xcontrol.html#confining-in-a-cavity
    """

    def __init__(self, radius=5.0, temperature=300, beta=6):
        self.radius = radius
        self.temperature = temperature
        self.beta = beta

    def _get_wall_energy_and_force(self, atoms):
        E, E_grad = _ext.log_fermi_spherical_potential(atoms.positions, self.radius, self.temperature, self.beta)
        return E, -E_grad
