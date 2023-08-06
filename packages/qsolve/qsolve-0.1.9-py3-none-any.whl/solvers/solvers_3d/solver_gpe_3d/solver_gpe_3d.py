from qsolve.solvers.solvers_3d.solver_gpe_3d.init_seed import init_seed
from qsolve.solvers.solvers_3d.solver_gpe_3d.init_device import init_device
from qsolve.solvers.solvers_3d.solver_gpe_3d.init_units import init_units

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_grid_3d import init_grid

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_potential import init_potential

from qsolve.solvers.solvers_3d.solver_gpe_3d.set_psi import set_psi
from qsolve.solvers.solvers_3d.solver_gpe_3d.set_V import set_V

from qsolve.solvers.solvers_3d.solver_gpe_3d.getter_functions import get

from qsolve.solvers.solvers_3d.solver_gpe_3d import densities
from qsolve.solvers.solvers_3d.solver_gpe_3d import spectrum
from qsolve.solvers.solvers_3d.solver_gpe_3d import n_atoms
from qsolve.solvers.solvers_3d.solver_gpe_3d import energies
from qsolve.solvers.solvers_3d.solver_gpe_3d import chemical_potential

from qsolve.core import qsolve_core_gpe_3d


class SolverGPE3D(object):

    def __init__(self, **kwargs):

        init_seed(self, kwargs)
        init_device(self, kwargs)
        init_units(self, kwargs)

    def init_grid(self, **kwargs):
        init_grid(self, kwargs)

    def init_potential(self, potential, params):
        init_potential(self, potential, params)

    def set_V(self, **kwargs):
        set_V(self, kwargs)

    def set_psi(self, identifier, **kwargs):
        set_psi(self, identifier, kwargs)

    def compute_ground_state_solution(self, **kwargs):
        qsolve_core_gpe_3d.compute_ground_state_solution(self, kwargs)

    def init_sgpe_z_eff(self, **kwargs):
        qsolve_core_gpe_3d.init_sgpe_z_eff(self, kwargs)

    def set_u_of_times(self, u_of_times):
        self.u_of_times = u_of_times

    def propagate_gpe(self, **kwargs):
        qsolve_core_gpe_3d.propagate_gpe(self, kwargs)

    def init_time_of_flight(self, params):
        qsolve_core_gpe_3d.init_time_of_flight(self, params)

    def compute_time_of_flight(self, **kwargs):
        qsolve_core_gpe_3d.compute_time_of_flight(self, kwargs)

    def propagate_sgpe_z_eff(self, **kwargs):
        qsolve_core_gpe_3d.propagate_sgpe_z_eff(self, kwargs)

    def init_time_evolution(self, **kwargs):
        qsolve_core_gpe_3d.init_time_evolution(self, kwargs)

    def get(self, identifier, **kwargs):
        return get(self, identifier, kwargs)

    def compute_n_atoms(self, identifier):
        return n_atoms.compute_n_atoms(self, identifier)

    def compute_chemical_potential(self, identifier, **kwargs):
        return chemical_potential.compute_chemical_potential(self, identifier, kwargs)

    def compute_E_total(self, identifier, **kwargs):
        return energies.compute_E_total(self, identifier, kwargs)

    def compute_E_kinetic(self, identifier, **kwargs):
        return energies.compute_E_kinetic(self, identifier, kwargs)

    def compute_E_potential(self, identifier, **kwargs):
        return energies.compute_E_potential(self, identifier, kwargs)

    def compute_E_interaction(self, identifier, **kwargs):
        return energies.compute_E_interaction(self, identifier, kwargs)

    def compute_density_xy(self, identifier, **kwargs):
        return densities.compute_density_xy(self, identifier, kwargs)

    def compute_density_xz(self, identifier, **kwargs):
        return densities.compute_density_xz(self, identifier, kwargs)

    def compute_spectrum_abs_xy(self, identifier, **kwargs):
        return spectrum.compute_spectrum_abs_xy(self, identifier, kwargs)

    def compute_spectrum_abs_xz(self, identifier, **kwargs):
        return spectrum.compute_spectrum_abs_xz(self, identifier, kwargs)
