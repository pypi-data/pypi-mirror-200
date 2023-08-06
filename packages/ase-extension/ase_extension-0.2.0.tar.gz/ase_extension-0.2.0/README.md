# ase_extension

Extension to ASE(atomistic simulation environment), written in Rust and Python.

## Features

- `ase_extension.constraints.LogFermiWallPotential`: Constrain atoms in sphere with logfermi potential
- `ase_extension.geometry.RMSD`: Minimum RMSD between molecules and its gradient
- `ase_extension.neighborlist.neighbor_list`: Drop-in replacement for `ase.neighborlist.neighbor_list`.

Note that `LogFermiWallPotential` and  `RMSD` does not support PBC yet.

## Installation


### With pypi

pip install ase_extension

### From source 

Install `maturin` first, and do:
```bash
pip install git+https://github.com/mjhong0708/ase_extension
```

## User guide

See [wiki](https://github.com/mjhong0708/ase_extension/wiki).


## Features to add

- [ ] Molecule packer for MD (like packmol, but supports PBC)
