
from typing import Union

import pandas as pd
import xarray as xr
import zarr

from .chunkstore import CustomChunkStore, DdcChunkStore
from .config import CustomCubeConfig, DdcCubeConfig
from .errors import DdcException


def open_cube(
        cube_config: Union[CustomCubeConfig, DdcCubeConfig],
        max_cache_size: int = 2 ** 30) -> xr.Dataset:

    """
    Open a data cube from Danube Data Cube.
    This is a facade function that hides the details of opening a
    data cube from Danube Data Cube.

    Args:
        cube_config (Union[CustomCubeConfig, DdcCubeConfig]):
            The cube configuration.
        max_cache_size (int): Cache size in bytes. Defaults to 1 GB.

    """

    if isinstance(cube_config, CustomCubeConfig):
        cube_store = CustomChunkStore(cube_config)
    elif isinstance(cube_config, DdcCubeConfig):
        cube_store = DdcChunkStore(cube_config)
    else:
        raise DdcException(
            'cube_config must be a valid instance of '
            'CustomCubeConfig or DdcCubeConfig')

    if max_cache_size:
        cube_store = zarr.LRUStoreCache(cube_store, max_cache_size)

    return xr.open_zarr(cube_store)


def set_valid_obs(dataarray: xr.DataArray) -> xr.DataArray:
    """
    Set valid observation Timestamps as new, MultiIndex coordinate.

    Args:
        dataarray (xr.DataArray): _description_
    """
    lst = (~dataarray.isnull().all(dim=['x', 'y']).values).astype(int)
    lst.append(dataarray.time.values)
    idx = pd.MultiIndex.from_arrays(lst, names=('valid_obs', 'time_obs'))

    arr = xr.DataArray(dataarray.values,
                       [("time", idx), ("y", dataarray.y.values),
                        ("x", dataarray.x.values)])

    return arr
