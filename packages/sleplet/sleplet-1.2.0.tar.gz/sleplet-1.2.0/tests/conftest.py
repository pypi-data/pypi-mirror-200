import numpy as np
import pytest
from numpy import typing as npt
from numpy.random import default_rng

from sleplet._vars import RANDOM_SEED
from sleplet.functions import Earth, SlepianDiracDelta, SlepianWavelets, SouthAmerica
from sleplet.harmonic_methods import compute_random_signal
from sleplet.meshes import Mesh, MeshField, MeshSlepian, MeshSlepianWavelets
from sleplet.slepian import SlepianArbitrary, SlepianLimitLatLon, SlepianPolarCap

ARRAY_DIM = 10
L = 16
MASK = "south_america"
PHI_0 = np.pi / 6
PHI_1 = np.pi / 3
THETA_0 = np.pi / 6
THETA_1 = np.pi / 3
THETA_MAX = 2 * np.pi / 9


@pytest.fixture(scope="session")
def slepian_polar_cap() -> SlepianPolarCap:
    """Create a Slepian polar cap class."""
    return SlepianPolarCap(L, THETA_MAX)


@pytest.fixture(scope="session")
def slepian_lim_lat_lon() -> SlepianLimitLatLon:
    """Create a Slepian limited latitude longitude class."""
    return SlepianLimitLatLon(
        L,
        theta_min=THETA_0,
        theta_max=THETA_1,
        phi_min=PHI_0,
        phi_max=PHI_1,
    )


@pytest.fixture(scope="session")
def slepian_arbitrary() -> SlepianArbitrary:
    """Create a Slepian arbitrary class."""
    return SlepianArbitrary(L, MASK)


@pytest.fixture(scope="session")
def earth_polar_cap(slepian_polar_cap) -> Earth:
    """Earth with polar cap region."""
    return Earth(slepian_polar_cap.L, region=slepian_polar_cap.region)


@pytest.fixture(scope="session")
def earth_lim_lat_lon(slepian_lim_lat_lon) -> Earth:
    """Earth with limited latitude longitude region."""
    return Earth(slepian_lim_lat_lon.L, region=slepian_lim_lat_lon.region)


@pytest.fixture(scope="session")
def south_america_arbitrary(slepian_arbitrary) -> SouthAmerica:
    """South America already has region."""
    return SouthAmerica(slepian_arbitrary.L)


@pytest.fixture(scope="session")
def slepian_dirac_delta_polar_cap(slepian_polar_cap) -> SlepianDiracDelta:
    """Creates a polar cap Slepian Dirac delta."""
    return SlepianDiracDelta(slepian_polar_cap.L, region=slepian_polar_cap.region)


@pytest.fixture(scope="session")
def slepian_dirac_delta_lim_lat_lon(slepian_lim_lat_lon) -> SlepianDiracDelta:
    """Creates a limited latitude longitude Slepian Dirac delta."""
    return SlepianDiracDelta(slepian_lim_lat_lon.L, region=slepian_lim_lat_lon.region)


@pytest.fixture(scope="session")
def slepian_wavelets_polar_cap(slepian_polar_cap) -> SlepianWavelets:
    """Computes the Slepian wavelets for the polar cap region."""
    return SlepianWavelets(slepian_polar_cap.L, region=slepian_polar_cap.region)


@pytest.fixture(scope="session")
def slepian_wavelets_lim_lat_lon(slepian_lim_lat_lon) -> SlepianWavelets:
    """Computes the Slepian wavelets for the lim_lat_lon region."""
    return SlepianWavelets(slepian_lim_lat_lon.L, region=slepian_lim_lat_lon.region)


@pytest.fixture(scope="session")
def random_flm() -> npt.NDArray[np.complex_]:
    """Creates random flm."""
    rng = default_rng(RANDOM_SEED)
    return compute_random_signal(L, rng, var_signal=1)


@pytest.fixture(scope="session")
def random_nd_flm() -> npt.NDArray[np.complex_]:
    """Creates multiple random flm."""
    rng = default_rng(RANDOM_SEED)
    return np.array(
        [compute_random_signal(L, rng, var_signal=1) for _ in range(ARRAY_DIM)],
    )


@pytest.fixture(scope="session")
def mesh() -> Mesh:
    """Creates a bird mesh."""
    return Mesh("bird")


@pytest.fixture(scope="session")
def mesh_slepian(mesh) -> MeshSlepian:
    """Creates a Slepian bird mesh."""
    return MeshSlepian(mesh)


@pytest.fixture(scope="session")
def mesh_field_region(mesh) -> MeshField:
    """Creates a field on the mesh."""
    return MeshField(mesh, region=True)


@pytest.fixture(scope="session")
def mesh_slepian_wavelets(mesh) -> MeshSlepianWavelets:
    """Creates a field on the mesh."""
    return MeshSlepianWavelets(mesh)
