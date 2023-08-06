from pathlib import Path

import numpy as np
import pyssht as ssht
from numpy import typing as npt

import sleplet
import sleplet._data.create_earth_flm
import sleplet._data.setup_pooch
import sleplet._vars
import sleplet.harmonic_methods
import sleplet.meshes.mesh
import sleplet.slepian.region

_data_path = Path(__file__).resolve().parent / "_data"

AFRICA_RANGE = np.deg2rad(41)
SOUTH_AMERICA_RANGE = np.deg2rad(40)


def create_mask_region(
    L: int,
    region: "sleplet.slepian.region.Region",
) -> npt.NDArray[np.float_]:
    """
    Creates a mask of a region of interested, the output will be based
    on the value of the provided L. The mask could be either:
    * polar cap - if theta_max provided
    * limited latitude longitude - if one of theta_min, theta_max,
                                   phi_min or phi_max is provided
    * arbitrary - just checks the shape of the input mask.
    """
    thetas, phis = ssht.sample_positions(
        L,
        Grid=True,
        Method=sleplet._vars.SAMPLING_SCHEME,
    )

    match region.region_type:
        case "arbitrary":
            sleplet.logger.info("loading and checking shape of provided mask")
            name = f"{region.mask_name}_L{L}.npy"
            mask = _load_mask(L, name)
            assert mask.shape == thetas.shape, (  # noqa: S101
                f"mask {name} has shape {mask.shape} which does not match "
                f"the provided L={L}, the shape should be {thetas.shape}"
            )

        case "lim_lat_lon":
            sleplet.logger.info("creating limited latitude longitude mask")
            mask = (
                (thetas >= region.theta_min)
                & (thetas <= region.theta_max)
                & (phis >= region.phi_min)
                & (phis <= region.phi_max)
            )

        case "polar":
            sleplet.logger.info("creating polar cap mask")
            mask = thetas <= region.theta_max
            if region.gap:
                sleplet.logger.info("creating polar gap mask")
                mask += thetas >= np.pi - region.theta_max
    return mask


def _load_mask(L: int, mask_name: str) -> npt.NDArray[np.float_]:
    """Attempts to read the mask from the config file."""
    mask = sleplet._data.setup_pooch.find_on_pooch_then_local(
        f"slepian_masks_{mask_name}",
    )
    return create_mask(L, mask_name) if mask is None else np.load(mask)


def ensure_masked_flm_bandlimited(
    flm: npt.NDArray[np.complex_],
    L: int,
    region: "sleplet.slepian.region.Region",
    *,
    reality: bool,
    spin: int,
) -> npt.NDArray[np.complex_]:
    """Ensures the coefficients is bandlimited for a given region."""
    field = ssht.inverse(
        flm,
        L,
        Reality=reality,
        Spin=spin,
        Method=sleplet._vars.SAMPLING_SCHEME,
    )
    mask = create_mask_region(L, region)
    field = np.where(mask, field, 0)
    return ssht.forward(
        field,
        L,
        Reality=reality,
        Spin=spin,
        Method=sleplet._vars.SAMPLING_SCHEME,
    )


def create_default_region() -> "sleplet.slepian.region.Region":
    """Creates default region."""
    return sleplet.slepian.region.Region(
        gap=sleplet.POLAR_GAP,
        mask_name=sleplet.SLEPIAN_MASK,
        phi_max=np.deg2rad(sleplet.PHI_MAX),
        phi_min=np.deg2rad(sleplet.PHI_MIN),
        theta_max=np.deg2rad(sleplet.THETA_MAX),
        theta_min=np.deg2rad(sleplet.THETA_MIN),
    )


def create_mesh_region(
    mesh_config: dict,
    vertices: npt.NDArray[np.float_],
) -> npt.NDArray[np.bool_]:
    """Creates a boolean region for the given mesh."""
    return (
        (vertices[:, 0] >= mesh_config["XMIN"])
        & (vertices[:, 0] <= mesh_config["XMAX"])
        & (vertices[:, 1] >= mesh_config["YMIN"])
        & (vertices[:, 1] <= mesh_config["YMAX"])
        & (vertices[:, 2] >= mesh_config["ZMIN"])
        & (vertices[:, 2] <= mesh_config["ZMAX"])
    )


def ensure_masked_bandlimit_mesh_signal(
    mesh: "sleplet.meshes.mesh.Mesh",
    u_i: npt.NDArray[np.complex_ | np.float_],
) -> npt.NDArray[np.float_]:
    """Ensures that signal in pixel space is bandlimited."""
    field = sleplet.harmonic_methods.mesh_inverse(mesh, u_i)
    masked_field = np.where(mesh.region, field, 0)
    return sleplet.harmonic_methods.mesh_forward(mesh, masked_field)


def convert_region_on_vertices_to_faces(
    mesh: "sleplet.meshes.mesh.Mesh",
) -> npt.NDArray[np.float_]:
    """Converts the region on vertices to faces."""
    region_reshape = np.argwhere(mesh.region).reshape(-1)
    faces_in_region = np.isin(mesh.faces, region_reshape).all(axis=1)
    region_on_faces = np.zeros(mesh.faces.shape[0])
    region_on_faces[faces_in_region] = 1
    return region_on_faces


def _create_africa_mask(
    L: int,
    earth_flm: npt.NDArray[np.complex_],
) -> npt.NDArray[np.float_]:
    """Creates the Africa region mask."""
    rot_flm = sleplet.harmonic_methods.rotate_earth_to_africa(earth_flm, L)
    earth_f = ssht.inverse(
        rot_flm,
        L,
        Reality=True,
        Method=sleplet._vars.SAMPLING_SCHEME,
    )
    thetas, _ = ssht.sample_positions(
        L,
        Grid=True,
        Method=sleplet._vars.SAMPLING_SCHEME,
    )
    return (thetas <= AFRICA_RANGE) & (earth_f >= 0)


def _create_south_america_mask(
    L: int,
    earth_flm: npt.NDArray[np.complex_],
) -> npt.NDArray[np.float_]:
    """Creates the Africa region mask."""
    rot_flm = sleplet.harmonic_methods.rotate_earth_to_south_america(earth_flm, L)
    earth_f = ssht.inverse(
        rot_flm,
        L,
        Reality=True,
        Method=sleplet._vars.SAMPLING_SCHEME,
    )
    thetas, _ = ssht.sample_positions(
        L,
        Grid=True,
        Method=sleplet._vars.SAMPLING_SCHEME,
    )
    return (thetas <= SOUTH_AMERICA_RANGE) & (earth_f >= 0)


def create_mask(L: int, mask_name: str) -> npt.NDArray[np.float_]:
    """Creates the South America region mask."""
    earth_flm = sleplet._data.create_earth_flm.create_flm(L)
    if mask_name == f"africa_L{L}.npy":
        mask = _create_africa_mask(L, earth_flm)
    elif mask_name == f"south_america_L{L}.npy":
        mask = _create_south_america_mask(L, earth_flm)
    else:
        raise ValueError(f"Mask name {mask_name} not recognised")
    np.save(_data_path / f"slepian_masks_{mask_name}", mask)
    return mask
