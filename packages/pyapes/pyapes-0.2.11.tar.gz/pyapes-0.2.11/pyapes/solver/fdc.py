#!/usr/bin/env python3
"""Finite Difference for the current field `FDC`. Similar to Openfoam's `FVC` class.
Each discretization method should create `A_coeffs` and `rhs_adj` attributes.
The `A_coeffs` contains `Ap`, `Ac`, and `Am` and each coefficient has a dimension of `mesh.dim x var.dim x mesh.nx`. Be careful! leading dimension is `mesh.dim` and not `var.dim`.
"""
import warnings
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

import torch
from pymytools.indices import tensor_idx
from torch import Tensor

from pyapes.geometry.basis import n2d_coord
from pyapes.solver.tools import default_A_ops
from pyapes.solver.types import DiscretizerConfigType
from pyapes.solver.types import DivConfigType
from pyapes.variables import Field
from pyapes.variables.bcs import BC
from pyapes.variables.container import Hess
from pyapes.variables.container import Jac


@dataclass
class Discretizer(ABC):
    """Collection of the operators for explicit finite difference discretization.
    Currently, all operators are meaning in `var[:][inner_slicer(mesh.dim)]` region.
    Therefore, to use in the `FDM` solver, the boundary conditions `var` should be applied before/during the `linalg` process.
    """

    A_coeffs: list[list[Tensor]] | None = None
    """Tuple of A operation matrix coefficients."""
    rhs_adj: Tensor | None = None
    """RHS adjustment tensor."""
    _op_type: str = "Discretizer"
    _config: DiscretizerConfigType | None = None

    @property
    def op_type(self) -> str:
        return self._op_type

    @property
    def config(self) -> DiscretizerConfigType | None:
        return self._config

    @staticmethod
    @abstractmethod
    def build_A_coeffs(
        *args: Field | Tensor | float | Jac | Hess,
        config: DiscretizerConfigType | None = None,
    ) -> list[list[Tensor]]:
        """Build the operation matrix coefficients to be used for the discretization.
        `var: Field` is required due to the boundary conditions. Should always return three tensors in `Ap`, `Ac`, and `Am` order.
        """
        ...

    @staticmethod
    @abstractmethod
    def adjust_rhs(
        *args: Field | Tensor | float | Jac | Hess,
        config: DiscretizerConfigType | None = None,
    ) -> Tensor:
        """Return a tensor that is used to adjust `rhs` of the PDE."""
        ...

    def apply(self, A_coeffs: list[list[Tensor]], var: Field) -> Tensor:
        """Apply the discretization to the input `Field` variable."""

        assert A_coeffs is not None, "FDC: A_A_coeffs is not defined!"
        if self.config is not None:
            edge = self.config[self.op_type.lower()]["edge"]
        else:
            edge = False
            warnings.warn(
                f"FDC: config is not defined! Using default config ({edge=})."
            )

        # Grad operator returns Jacobian, but Laplacian, Div, and Ddt return scalar (sum over j-index)
        if self.op_type == "Grad":
            dis_var_dim = []
            for idx in range(var.dim):
                grad_d = []
                for dim in range(var.mesh.dim):
                    grad_d.append(_A_coeff_var_sum(A_coeffs, var, idx, dim))
                dis_var_dim.append(torch.stack(grad_d))
            discretized = torch.stack(dis_var_dim)

            if edge:
                for dim in range(discretized.shape[0]):
                    _treat_edge(discretized, var, self.op_type, dim)

        elif self.op_type == "Div":
            """Div always returns a scalar field. (`discretized.shape[0] == 1`)"""

            discretized = torch.zeros_like(var()[0]).unsqueeze(0)

            for idx in range(var.mesh.dim):
                disc = _A_coeff_var_sum(A_coeffs, var, idx, idx)
                if edge:
                    _treat_edge(disc, var, self.op_type, idx, self.var_addition)
                discretized[0] += disc
        elif self.op_type == "Laplacian":
            discretized = torch.zeros_like(var())

            for idx in range(var.dim):
                for dim in range(var.mesh.dim):
                    discretized[idx] += _A_coeff_var_sum(A_coeffs, var, idx, dim)

            if edge:
                for dim in range(var.dim):
                    _treat_edge(discretized, var, self.op_type, dim)
                return discretized

        else:
            raise TypeError(f"FDC: ({self.op_type=} is not supported!")

        return discretized

    def reset(self) -> None:
        """Resetting all the attributes to `None`."""

        self.A_coeffs = None
        self.rhs_adj = None

    def set_config(self, config: DiscretizerConfigType) -> None:
        """Set the configuration for the discretization."""

        self._config = config

    def __call__(
        self, *args: Field | Tensor | float | Jac | Hess
    ) -> Tensor | list[Tensor]:
        """By calling the class with the input `Field` variable, the discretization is conducted."""

        if len(args) == 1:
            assert isinstance(args[0], Field), "FDC: only `Field` is allowed for var!"
            return self.__call_one_var(args[0])
        else:
            assert isinstance(
                args[0], Field | Tensor | float | Jac | Hess
            ), "FDC: for var_j, Field, Tensor, float, Jac, and Hess are allowed!"
            assert isinstance(args[1], Field), "FDC: only `Field` is allowed for var_i!"

            return self.__call_two_vars(args[0], args[1])

    # NOTE: Currently always reconstruct the coefficients. Need better idea?
    def __call_one_var(self, var: Field) -> Tensor | list[Tensor]:
        """Return of `__call__` method for the operators that only require one variable."""

        self.A_coeffs = self.build_A_coeffs(var)

        self.rhs_adj = self.adjust_rhs(var)

        return self.apply(self.A_coeffs, var)

    def __call_two_vars(
        self, var_j: Field | Tensor | float | Jac | Hess, var_i: Field
    ) -> Tensor:
        """Return of `__call__` method for the operators that require two variables."""

        self.A_coeffs = self.build_A_coeffs(var_j, var_i, config=self.config)

        self.rhs_adj = self.adjust_rhs(var_j, var_i, config=self.config)

        self.var_addition = var_j

        return self.apply(self.A_coeffs, var_i)


def _A_coeff_var_sum(
    A_coeffs: list[list[Tensor]], var: Field, idx: int, dim: int
) -> Tensor:
    """Sum the coefficients and the variable.
    Here, `len(A_coeffs) = 5` to implement `quick` scheme for `div` operator in the future.

    Args:
        A_coeffs (list[list[Tensor]]): A list of coefficient tensors.
        var (Field): The input `Field` variable.
        idx (int): The index of the variable in `var.dim`.
        dim (int): The dimension of the mesh domain.
    """

    assert (
        len(A_coeffs) == 5
    ), "FDC: the total number of coefficient tensor should be 5!"

    summed = torch.zeros_like(var[0])

    for i, c in enumerate(A_coeffs):
        if var.dim == 1:
            coeff = c[dim][0]
            v_idx = 0
        else:
            coeff = c[dim][idx]
            v_idx = idx

        summed += coeff * torch.roll(var[v_idx], -2 + i, dim)

    return summed


def _treat_edge(
    discretized: Tensor | list[Tensor],
    var: Field,
    ops: str,
    dim: int,
    var_add: Field | Tensor | float | Jac | Hess | None = None,
) -> None:
    """Treat edge of discretized variable using the forward/backward difference.
    Here the edge means the domain (mesh) boundary.

    Note:
        - Using slicers is inspired from `numpy.gradient` function
    """

    # Slicers
    slicer_1: list[slice | int] = [slice(None) for _ in range(var.mesh.dim)]
    slicer_2: list[slice | int] = [slice(None) for _ in range(var.mesh.dim)]
    slicer_3: list[slice | int] = [slice(None) for _ in range(var.mesh.dim)]
    slicer_4: list[slice | int] = [slice(None) for _ in range(var.mesh.dim)]

    if ops == "Laplacian":
        # Treat edge with the second order forward/backward difference

        for idx in range(var.mesh.dim):
            slicer_1[idx] = 0
            slicer_2[idx] = 1
            slicer_3[idx] = 2
            slicer_4[idx] = 3

            bc_val = var()[dim][slicer_1]
            bc_val_p = var()[dim][slicer_2]
            bc_val_pp = var()[dim][slicer_3]
            bc_val_ppp = var()[dim][slicer_4]

            discretized[dim][slicer_1] = (
                2.0 * bc_val - 5.0 * bc_val_p + 4.0 * bc_val_pp - bc_val_ppp
            ) / (var.mesh.dx[idx] ** 2)

            slicer_1[idx] = -1
            slicer_2[idx] = -2
            slicer_3[idx] = -3
            slicer_4[idx] = -4

            bc_val = var()[dim][slicer_1]
            bc_val_p = var()[dim][slicer_2]
            bc_val_pp = var()[dim][slicer_3]
            bc_val_ppp = var()[dim][slicer_4]

            discretized[dim][slicer_1] = (
                2.0 * bc_val - 5.0 * bc_val_p + 4.0 * bc_val_pp - bc_val_ppp
            ) / (var.mesh.dx[idx] ** 2)

            slicer_1[idx] = slice(None)
            slicer_2[idx] = slice(None)
            slicer_3[idx] = slice(None)
            slicer_4[idx] = slice(None)

    elif ops == "Grad":
        for idx in range(var.mesh.dim):
            slicer_1[idx] = 0
            slicer_2[idx] = 1
            slicer_3[idx] = 2

            bc_val = var()[dim][slicer_1]
            bc_val_p = var()[dim][slicer_2]
            bc_val_pp = var()[dim][slicer_3]

            discretized[dim][idx][slicer_1] = -(
                3 / 2 * bc_val - 2.0 * bc_val_p + 1 / 2 * bc_val_pp
            ) / (var.mesh.dx[idx])

            slicer_1[idx] = -1
            slicer_2[idx] = -2
            slicer_3[idx] = -3

            bc_val = var()[dim][slicer_1]
            bc_val_p = var()[dim][slicer_2]
            bc_val_pp = var()[dim][slicer_3]

            discretized[dim][idx][slicer_1] = (
                3 / 2 * bc_val - 2.0 * bc_val_p + 1 / 2 * bc_val_pp
            ) / (var.mesh.dx[idx])

            slicer_1[idx] = slice(None)
            slicer_2[idx] = slice(None)
            slicer_3[idx] = slice(None)

    elif ops == "Div":
        assert isinstance(discretized, Tensor)

        n2d = n2d_coord(var.mesh.coord_sys)

        if isinstance(var_add, Field):
            adv = var_add[dim]
        elif isinstance(var_add, Tensor):
            if var_add.shape == var().shape:
                adv = var_add[dim]
            else:
                adv = var_add
        elif isinstance(var_add, float):
            adv = torch.ones_like(var[dim]) * var_add
        elif isinstance(var_add, Jac):
            adv = var_add[n2d[dim]]
        elif var_add is None:
            adv = torch.ones_like(var[dim])
        else:
            raise NotImplementedError("FDC: var_j Hess is not implemented yet!")

        if var().shape[0] == 1:
            target = var[0]
        else:
            target = var[dim]

        slicer_1[dim] = 0
        slicer_2[dim] = 1
        slicer_3[dim] = 2

        bc_val = target[slicer_1]
        bc_val_p = target[slicer_2]
        bc_val_pp = target[slicer_3]

        discretized[slicer_1] = (
            -(3 / 2 * bc_val - 2.0 * bc_val_p + 1 / 2 * bc_val_pp)
            / (var.mesh.dx[dim])
            * adv[slicer_1]
        )

        if var.mesh.coord_sys == "rz" and dim == 0:
            rz_add = torch.nan_to_num(
                bc_val / var.mesh.R[slicer_1], nan=0.0, posinf=0.0, neginf=0.0
            )
            discretized[slicer_1] += rz_add

        slicer_1[dim] = -1
        slicer_2[dim] = -2
        slicer_3[dim] = -3

        bc_val = target[slicer_1]
        bc_val_p = target[slicer_2]
        bc_val_pp = target[slicer_3]

        discretized[slicer_1] = (
            (3 / 2 * bc_val - 2.0 * bc_val_p + 1 / 2 * bc_val_pp)
            / (var.mesh.dx[dim])
            * adv[slicer_1]
        )

        if var.mesh.coord_sys == "rz" and dim == 0:
            rz_add = torch.nan_to_num(
                bc_val * adv[slicer_1] / var.mesh.R[slicer_1],
                nan=0.0,
                posinf=0.0,
                neginf=0.0,
            )
            discretized[slicer_1] += rz_add

        slicer_1[dim] = slice(None)
        slicer_2[dim] = slice(None)
        slicer_3[dim] = slice(None)

    else:
        raise RuntimeError(f"FDC: edge treatment of {ops=} is not supported!")

    pass


class Laplacian(Discretizer):
    """Laplacian discretizer."""

    def __init__(self):
        self._op_type = __class__.__name__

    @staticmethod
    def build_A_coeffs(var: Field) -> list[list[Tensor]]:
        App, Ap, Ac, Am, Amm = default_A_ops(var, __class__.__name__)

        dx = var.dx
        # Treat boundaries
        for i in range(var.dim):
            for j in range(var.mesh.dim):
                if var.bcs is None:
                    # Do nothing
                    continue

                # Treat BC
                for bc in var.bcs:
                    # If discretization direction is not the same as the BC surface normal direction, do nothing
                    if bc.bc_n_vec[j] == 0:
                        continue

                    if bc.bc_type == "neumann" or bc.bc_type == "symmetry":
                        # Treatment for the cylindrical coordinate
                        dr = var.mesh.dx[j] if j == 0 else 0.0
                        r = var.mesh.grid[j][bc.bc_mask_prev]
                        alpha = (
                            torch.nan_to_num(
                                2 / 3 * dr / r, nan=0.0, posinf=0.0, neginf=0.0
                            )
                            if var.mesh.coord_sys == "rz"
                            else torch.zeros_like(r)
                        )

                        if bc.bc_n_dir < 0:
                            # At lower side
                            Ap[j][i][bc.bc_mask_prev] = 2 / 3 + alpha
                            Ac[j][i][bc.bc_mask_prev] = -(2 / 3 + alpha)
                            Am[j][i][bc.bc_mask_prev] = 0.0
                        else:
                            # At upper side
                            Ap[j][i][bc.bc_mask_prev] = 0.0
                            Ac[j][i][bc.bc_mask_prev] = -(2 / 3 + alpha)
                            Am[j][i][bc.bc_mask_prev] = 2 / 3 + alpha
                    else:
                        # Do nothing
                        pass

                Ap[j][i] /= dx[j] ** 2
                Ac[j][i] /= dx[j] ** 2
                Am[j][i] /= dx[j] ** 2

        return [App, Ap, Ac, Am, Amm]

    @staticmethod
    def adjust_rhs(var: Field) -> Tensor:
        rhs_adj = torch.zeros_like(var())
        dx = var.dx

        # Treat boundaries
        for i in range(var.dim):
            if var.bcs is None:
                # Do nothing
                continue

            for j in range(var.mesh.dim):
                for bc in var.bcs:
                    if bc.bc_type == "neumann":
                        # Treatment for the cylindrical coordinate
                        dr = var.mesh.dx[j] if j == 0 else 0.0
                        r = var.mesh.grid[j][bc.bc_mask_prev]
                        alpha = (
                            torch.nan_to_num(
                                1 / 3 * dr / r, nan=0.0, posinf=0.0, neginf=0.0
                            )
                            if var.mesh.coord_sys == "rz"
                            else torch.zeros_like(r)
                        )

                        at_bc = _return_bc_val(bc, var, i)
                        rhs_adj[i][bc.bc_mask_prev] += (
                            (2 / 3 - alpha) * (at_bc * bc.bc_n_vec[j]) / dx[j]
                        )
                    else:
                        # Do nothing
                        pass

        return rhs_adj


class Grad(Discretizer):
    """Gradient operator.
    Once the discretization is conducted, returned value is a `2 + len(mesh.nx)` dimensional tensor with the shape of `(var.dim, mesh.dim, *mesh.nx)`

    Example:

    >>> mesh = Mesh(Box[0:1, 0:1], None, [10, 10]) # 2D mesh with 10x10 cells
    >>> var = Field("test_field", 1, mesh, ...) # scalar field
    >>> fdm = FDM()
    >>> grad = fdm.grad(var)
    >>> grad.shape
    torch.Size([1, 2, 10, 10])

    """

    def __init__(self):
        self._op_type = __class__.__name__

    @staticmethod
    def build_A_coeffs(var: Field) -> list[list[Tensor]]:
        r"""Build the coefficients for the discretization of the gradient operator using the second-order central finite difference method.

        ..math::
            \nabla \Phi = \frac{\Phi^{i+1} - \Phi^{i-1}}{2 \Delta x}
        """
        App, Ap, Ac, Am, Amm = default_A_ops(var, __class__.__name__)

        if var.bcs is not None:
            for i in range(var.dim):
                _grad_central_adjust(var, [Ap, Ac, Am], i)

        return [App, Ap, Ac, Am, Amm]

    @staticmethod
    def adjust_rhs(var: Field) -> Tensor:
        rhs_adj = torch.zeros_like(var())

        if var.bcs is not None:
            for i in range(var.dim):
                _grad_rhs_adjust(var, rhs_adj, i)

        return rhs_adj


def _grad_rhs_adjust(
    var: Field, rhs_adj: Tensor, dim: int, gamma: tuple[Tensor, ...] | None = None
) -> None:
    """Adjust the RHS for the gradient operator. This function is seperated from the class to be reused in the `Div` operator."""

    if gamma is None:
        gamma_min = torch.ones_like(var())
        gamma_max = torch.ones_like(var())
    else:
        if len(gamma) == 1:
            gamma_min = 2.0 * gamma[0]
            gamma_max = 2.0 * gamma[0]
        else:
            gamma_min = 2.0 * gamma[0]
            gamma_max = 2.0 * gamma[1]

    for j in range(var.mesh.dim):
        for bc in var.bcs:
            if bc.bc_type == "neumann":
                at_bc = _return_bc_val(bc, var, dim)

                if bc.bc_n_dir < 0:
                    rhs_adj[dim][bc.bc_mask_prev] -= (
                        (1 / 3)
                        * (at_bc * bc.bc_n_vec[j])
                        * gamma_max[dim][bc.bc_mask_prev]
                    )
                else:
                    rhs_adj[dim][bc.bc_mask_prev] -= (
                        (1 / 3)
                        * (at_bc * bc.bc_n_vec[j])
                        * gamma_min[dim][bc.bc_mask_prev]
                    )
            else:
                # Dirichlet and Symmetry BC: Do nothing
                pass


def _grad_central_adjust(
    var: Field,
    A_ops: list[list[Tensor]],
    dim: int,
    gamma: tuple[Tensor, ...] | None = None,
) -> None:
    """Adjust gradient's A_ops to accommodate boundary conditions.

    Args:
        var (Field): input variable to be discretized
        A_ops (tuple[list[Tensor], ...]): tuple of lists of tensors containing the coefficients of the discretization. `len(A_ops) == 3` since we need `Ap`, `Ac`, and `Am` coefficients.
        dim (int): variable dimension. It should be in the range of `var.dim`. Defaults to 0.
        it is not the dimension of the mesh!
        gamma: advection term that accounts the divergence operation
    """

    if gamma is None:
        gamma_min = torch.ones_like(var())
        gamma_max = torch.ones_like(var())
    else:
        if len(gamma) == 1:
            gamma_min = gamma[0]
            gamma_max = gamma[0]
        else:
            gamma_min = gamma[0]
            gamma_max = gamma[1]

    Ap, Ac, Am = A_ops

    dx = var.dx

    # Treat boundaries
    for j in range(var.mesh.dim):
        # Treat BC
        for bc in var.bcs:
            # If discretization direction is not the same as the BC surface normal direction, do nothing
            if bc.bc_n_vec[j] == 0:
                continue

            if bc.bc_type == "neumann" or bc.bc_type == "symmetry":
                gmx_at_mask = gamma_max[dim][bc.bc_mask_prev]
                gmn_at_mask = gamma_min[dim][bc.bc_mask_prev]

                if bc.bc_n_dir < 0:
                    # At lower side
                    Ap[j][dim][bc.bc_mask_prev] += 1 / 3 * gmx_at_mask
                    Ac[j][dim][bc.bc_mask_prev] -= 1 / 3 * gmn_at_mask
                    Am[j][dim][bc.bc_mask_prev] = 0.0
                else:
                    # At upper side
                    Ap[j][dim][bc.bc_mask_prev] = 0.0
                    Ac[j][dim][bc.bc_mask_prev] += 1 / 3 * gmn_at_mask
                    Am[j][dim][bc.bc_mask_prev] -= 1 / 3 * gmx_at_mask
            elif bc.bc_type == "periodic":
                if bc.bc_n_dir < 0:
                    # At lower side
                    Am[j][dim][bc.bc_mask_prev] = 0.0
                else:
                    # At upper side
                    Ap[j][dim][bc.bc_mask_prev] = 0.0
            else:
                # Dirichlet BC: Do nothing
                pass

        Ap[j][dim] /= 2.0 * dx[j]
        Ac[j][dim] /= 2.0 * dx[j]
        Am[j][dim] /= 2.0 * dx[j]


class Div(Discretizer):
    """Divergence operator.
    It supports `central` and `upwind` discretization methods.

    FUTURE: quick scheme
    """

    def __init__(self):
        self._op_type = __class__.__name__

    @staticmethod
    def build_A_coeffs(
        var_j: Field | float | Tensor | Hess | Jac,
        var_i: Field,
        config: DiscretizerConfigType,
    ) -> list[list[Tensor]]:
        r"""Build the coefficients for the discretization of the gradient operator using the second-order central finite difference method. `i` and `j` indicates the Einstein summation convention. Here, `j` comes first to be consistent with the equation:

        ..math::
            \vec{u}_{j} \frac{\partial \Phi}{\partial x_j} = \frac{\Phi^{i+1} - \Phi^{i-1}}{2 \Delta x} + ...

        Args:
            var_j (Field | float | Tensor): advection term
            var_i (Field): input variable to be discretized
            config (dict[str, str]): configuration dictionary. It should contain the following keys: `limiter`.
        """

        if isinstance(var_j, Field | Tensor | float):
            adv = _div_var_j_to_tensor(var_j, var_i)
        else:
            adv = var_j

        assert "div" in config, "FDC Div: config should contain 'div' key."

        limiter = _check_limiter(config["div"])

        App, Ap, Ac, Am, Amm = default_A_ops(var_i, __class__.__name__)

        if limiter == "none":
            Ap, Ac, Am = _adv_central(adv, var_i, [Ap, Ac, Am])
        elif limiter == "upwind":
            if isinstance(adv, Hess):
                raise NotImplementedError(
                    "FDC: Upwind limiter is not implemented for Hessians and Jacobians advection term."
                )
            else:
                Ap, Ac, Am = _adv_upwind(adv, var_i, [Ap, Ac, Am])
        elif limiter == "quick":
            raise NotImplementedError("FDC Div: quick scheme is not implemented yet.")
        else:
            raise RuntimeError(f"FDC Div: {limiter=} is an unknown limiter type.")

        return [App, Ap, Ac, Am, Amm]

    @staticmethod
    def adjust_rhs(
        var_j: Field | Tensor | float, var_i: Field, config: DiscretizerConfigType
    ) -> Tensor:
        rhs_adj = torch.zeros_like(var_i())

        # FIXME: var_j hessian is not supported yet
        if var_i.bcs is not None:
            adv = _div_var_j_to_tensor(var_j, var_i)

            assert "div" in config, "FDC Div: config should contain 'div' key."

            limiter = _check_limiter(config["div"])

            if limiter == "none":
                for i in range(var_i.dim):
                    _grad_rhs_adjust(var_i, rhs_adj, i, (adv,))
            elif limiter == "upwind":
                gamma_min, gamma_max = _gamma_from_adv(adv, var_i)
                for i in range(var_i.dim):
                    _grad_rhs_adjust(var_i, rhs_adj, i, (gamma_min, gamma_max))
            elif limiter == "quick":
                raise NotImplementedError(
                    "FDC Div: quick scheme is not implemented yet."
                )
            else:
                raise RuntimeError(f"FDC Div: {limiter=} is an unknown limiter type.")

        return rhs_adj


def _check_limiter(config: DivConfigType | None) -> str:
    """Check the limiter type."""
    if config is not None and "limiter" in config:
        return config["limiter"].lower()  # make sure it is lower case
    else:
        warnings.warn(
            "FDM: no limiter is specified. Use `none` (central difference) as a default."
        )
        return "none"


def _adv_central(
    adv: Tensor | Hess | Jac, var: Field, A_ops: list[list[Tensor]]
) -> list[list[Tensor]]:
    """Discretization of the advection tern using central difference.

    Args:
        adv (Tensor): Advection term, i.e., `var_j`.
        var (Field): variable to be discretized. i.e., `var_i`.
        A_ops (tuple[list[Tensor], ...]): Discretization coefficients.
    """

    # Leading dimension is the dimension of the mesh
    # The following dimension is the dimension of the variable
    # A_[mesh.dim][var.dim]
    Ap, Ac, Am = A_ops

    n2d = n2d_coord(var.mesh.coord_sys)

    advection = torch.zeros_like(var()[0])

    for i in range(var.dim):
        for j in range(var.mesh.dim):
            if isinstance(adv, Jac):
                advection = adv[n2d[i]]
            elif isinstance(adv, Hess):
                advection = adv[n2d[i] + n2d[j]]
            else:
                advection = adv[i]
            Ap[j][i] *= torch.roll(advection, -1, dims=j)
            Ac[j][i] *= advection
            Am[j][i] *= torch.roll(advection, 1, dims=j)

        # NOTE: This is not working for the case of `isinstance(adv, Hess)`!!
        _grad_central_adjust(var, [Ap, Ac, Am], i, (advection,))

    return [Ap, Ac, Am]


def _adv_upwind(
    adv: Tensor | Hess | Jac, var: Field, A_ops: list[list[Tensor]]
) -> list[list[Tensor]]:
    n2d = n2d_coord(var.mesh.coord_sys)

    Ap, Ac, Am = A_ops

    zeros = torch.zeros_like(var()[0])

    for i in range(var.dim):
        for j in range(var.mesh.dim):
            if isinstance(adv, Jac):
                advection = adv[n2d[i]]
            elif isinstance(adv, Tensor):
                advection = adv[i]
            else:
                raise NotImplementedError(
                    "FDC: Upwind limiter is not implemented for Hessians advection term."
                )
            gamma_min = torch.min(advection, zeros)
            gamma_max = torch.max(advection, zeros)

            Ap[j][i] = 2.0 * gamma_min
            Ac[j][i] *= 2.0 * advection
            Am[j][i] = 2.0 * gamma_max

    return [Ap, Ac, Am]


def _div_var_j_to_tensor(var_j: Field | Tensor | float | Jac, var_i: Field) -> Tensor:
    """In `Div` operator, convert `var_j` to a `Tensor`. Also check the shape of `var_j` so that is has the same shape of target variable `var_i`."""

    if isinstance(var_j, float):
        adv = torch.ones_like(var_i()) * var_j
    elif isinstance(var_j, Tensor):
        adv = var_j
        # Shape check
        assert adv.shape == var_i().shape, "FDC Div: adv shape must match var_i shape"
    elif isinstance(var_j, Field):
        adv = var_j()
    else:
        n2d = n2d_coord(var_i.mesh.coord_sys)
        adv = torch.zeros((len(var_j), *var_i().shape[1:]))
        for i in range(len(var_j)):
            adv[i] = var_j[n2d[i]]

    return adv


def _gamma_from_adv(adv: Tensor, var: Field) -> tuple[Tensor, Tensor]:
    zeros = torch.zeros_like(var())
    gamma_min = torch.min(adv, zeros)
    gamma_max = torch.max(adv, zeros)

    return gamma_min, gamma_max


def _return_bc_val(bc: BC, var: Field, dim: int) -> Tensor | float:
    """Return boundary values."""

    if callable(bc.bc_val):
        at_bc = bc.bc_val(var.mesh.grid, bc.bc_mask, var(), bc.bc_n_vec)
    elif isinstance(bc.bc_val, list):
        at_bc = bc.bc_val[dim]
    elif isinstance(bc.bc_val, float | int):
        at_bc = bc.bc_val
    elif bc.bc_val is None:
        at_bc = 0.0
    else:
        raise ValueError(f"Unknown boundary condition value: {bc.bc_val}")

    return at_bc


class DiffFlux:
    """Object to be used in the tensor diffussion term."""

    @staticmethod
    def __call__(diff: Hess, var: Field) -> Field:
        r"""Compute the diffusive flux without boundary treatment (just forward-backward difference)

        .. math::
            D_ij \frac{\partial \Phi}{\partial x_j}

        Therefore, it returns a vector field.

        Args:
            diff (Hess): Diffusion tensor
            var (Field): Scalar input field
        """

        jac_var = jacobian(var)
        flux = Field("DiffFlux", len(jac_var), var.mesh, None)

        n2d = n2d_coord(var.mesh.coord_sys)

        for i in range(var.mesh.dim):
            diff_flux = torch.zeros_like(var()[0])
            for j in range(var.mesh.dim):
                j_key = n2d[j]
                h_key = n2d[i] + n2d[j]

                if n2d[i] == "r":
                    d_coeff = var.mesh.grid[0] * diff[h_key]
                else:
                    d_coeff = diff[h_key]

                diff_flux += d_coeff * jac_var[j_key]

            flux.set_var_tensor(diff_flux, i)

        return flux


class FDC:
    """Collection of Finite Difference discretization. The operation is explicit, therefore, all methods return a tensor."""

    div: Div = Div()
    """Divergence operator: `div(var_j, var_i)`."""
    laplacian: Laplacian = Laplacian()
    """Laplacian operator: `laplacian(coeffs, var)`."""
    grad: Grad = Grad()
    """Gradient operator: `grad(var)`."""
    diffFlux: DiffFlux = DiffFlux()

    def __init__(self, config: DiscretizerConfigType | None = None):
        """Init FDC class."""

        self.config = config

        if self.config is not None:
            for c, _ in self.config.items():
                scheme: Discretizer = getattr(self, c)
                scheme.set_config(self.config)

    def update_config(self, scheme: str, target: str, val: str):
        """Update config values."""

        if self.config is not None:
            self.config[scheme][target] = val
        else:
            self.config = {scheme: {target: val}}

        assert isinstance(self.config, DiscretizerConfigType)

        for c, _ in self.config.items():
            s: Discretizer = getattr(self, c)
            s.set_config(self.config)


def jacobian(var: Field) -> Jac:
    """Compute the Jacobian of a scalar field."""
    assert var().shape[0] == 1, "Scalar: var must be a scalar field."

    data_jac: dict[str, Tensor] = {}

    n2d = n2d_coord(var.mesh.coord_sys)

    fdc = FDC({"grad": {"edge": True}})

    var_dummy = Field("container", 1, var.mesh, None)
    jac = fdc.grad(var_dummy.set_var_tensor(var[0]))[0]

    for i, j in enumerate(jac):
        data_jac[n2d[i]] = j

    fdc.grad.reset()

    return Jac(**data_jac)


def hessian(var: Field) -> Hess:
    """Compute the Hessian of a scalar field."""

    indices = tensor_idx(var.mesh.dim)

    data_hess: dict[str, Tensor] = {}

    hess: list[Tensor] = []

    n2d = n2d_coord(var.mesh.coord_sys)

    fdc = FDC({"grad": {"edge": True}})

    var_dummy = Field("container", 1, var.mesh, None)

    jac = fdc.grad(var_dummy.set_var_tensor(var[0]))[0]

    jac_f = var_dummy.copy()

    hess = [fdc.grad(jac_f.set_var_tensor(j))[0] for j in jac]

    for i, hi in enumerate(hess):
        for j, h in enumerate(hi):
            if (i, j) in indices:
                data_hess[n2d[i] + n2d[j]] = h

    FDC.grad.reset()
    return Hess(**data_hess)
