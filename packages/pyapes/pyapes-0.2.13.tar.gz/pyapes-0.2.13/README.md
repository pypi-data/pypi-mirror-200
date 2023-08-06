
# pyapes: PYthon Awesome Partial differential Equation Solver (general purpose finite difference PDE solver)

![python](http://ForTheBadge.com/images/badges/made-with-python.svg)

## Description

`pyapes` is designed to solve various engineering problems in rectangular grid.

The goal of `pyapes` (should be/have) is

- Cross-platform
  - Both tested on Mac and Linux (Arch)
  - Windows support is under testing
- GPU acceleration in a structured grid with [PyTorch](https://pytorch.org)
  - Use of `torch.Tensor`. User can choose either `torch.device("cpu")` or `torch.device("cuda")`.
- Generically expressed (OpenFOAM-like, human-readable formulation)

## Installation

We recommend to use `poetry` to manage/install all dependencies.

- From `git`

  ```bash
  git clone git@gitlab.ethz.ch:kchung/pyapes.git
  cd pyapes
  poetry install
  ```

- From `pypi`

  ```bash
  python3 -m pip install pyapes
  # or
  poetry add pyapes
  ```

## Dependencies

- Core dependency
  - `python >= 3.10`
    - As of 19.02.2023, `torch` does not support 3.11 properly (for the official release). Therefore, stick to `python3.10`.
  - `torch >= 1.10.0`
- Dependencies from my personal projects
  - `pymyplot` (plotting tools)
  - `pymytools` (misc. tools including data I/O, logging, etc.)

## Implemented Features

- CPU/GPU(CUDA) computation using `torch`
- (OpenFOAM like) generically expressed solver

  ```python
    >>> solver.set_eq(fdm.laplacian(1.0, var) == rhs)
    >>> solver.solve()
  ```

- FDM Discretizations
  - Spatial: `Grad`, `Laplacian`, `Div`
    - Supports flux limiter `upwind` for the `Div` operator
  - Temporal: `Ddt`
- Boundary conditions:
  - Supports `Dirichlet`, `Neumann`, `Periodic`, and `Symmetry`
- Demo cases in `jupter` notebooks

## Examples

Check our [demos files](demos/)

## Todos

- Boundary conditions
  - [ ] Inflow/Outflow
- Need different derivative order at the cell face
  - Additional features
    - [ ] High order time discretization
    - [ ] Immersed body BC
    - [ ] Higher order flux limiters (`quick`)
- Testing and validation
  - [ ] `Ddt` class (implementation is tested but haven't validated with practical test cases)
- Working on demo files
  - [x] The Poisson equation
  - [x] The advection-diffusion equation
  - [ ] The Burgers' equation
  - [ ] The Navier-Stokes equation at low Reynolds numbers
  - [ ] The Black-Scholes equation
