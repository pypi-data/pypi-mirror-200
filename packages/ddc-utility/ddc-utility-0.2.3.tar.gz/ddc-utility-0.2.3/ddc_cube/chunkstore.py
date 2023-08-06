
import itertools
import json
import time
from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping
from typing import (Any, Callable, Dict, Iterable, Iterator, KeysView, List,
                    Optional, Tuple)

import numpy as np
import pandas as pd
import pyproj
from numcodecs import Blosc

from .config import CubeConfig, CustomCubeConfig, DdcCubeConfig
from .errors import DdcException, DdcRequestError

_STATIC_ARRAY_COMPRESSOR_PARAMS = dict(
    cname='zstd',
    clevel=1,
    shuffle=Blosc.SHUFFLE,
    blocksize=0
)

_STATIC_ARRAY_COMPRESSOR_CONFIG = dict(
    id='blosc',
    **_STATIC_ARRAY_COMPRESSOR_PARAMS
)

_REMOTE_ARRAY_COMPRESSOR_PARAMS = dict(
    cname='lz4',
    clevel=5,
    shuffle=Blosc.SHUFFLE,
    blocksize=0
)

_REMOTE_ARRAY_COMPRESSOR_CONFIG = dict(
    id='blosc',
    **_REMOTE_ARRAY_COMPRESSOR_PARAMS
)

_STATIC_ARRAY_COMPRESSOR = Blosc(**_STATIC_ARRAY_COMPRESSOR_PARAMS)


def _dict_to_bytes(d: Dict) -> bytes:
    return _str_to_bytes(json.dumps(d, indent=2))


def _bytes_to_dict(b: bytes) -> Dict:
    return json.loads(_bytes_to_str(b))


def _str_to_bytes(s: str):
    return bytes(s, encoding='utf-8')


def _bytes_to_str(b: bytes) -> str:
    return b.decode('utf-8')


# MutableMapping, metaclass=ABCMeta):
class RemoteStore(MutableMapping, metaclass=ABCMeta):
    """
    A remote Zarr Store for accessing spatial data cubes.

    Args:
        cube_config (CubeConfig): Cube configuration.
        observer (Optional[Callable]): An optional callback function called when
            remote requests are mode: observer(**kwargs).
        trace_store_calls (bool): Whether store calls shall be
            printed (for debugging).
    """

    def __init__(self,
                 cube_config: CubeConfig,
                 observer: Optional[Callable] = None,
                 trace_store_calls=False):

        self._cube_config = cube_config
        self._observers = [observer] if observer is not None else []
        self._trace_store_calls = trace_store_calls

        self._time_ranges = self._cube_config.time_lst
        if self._time_ranges.empty:
            raise ValueError('Could not determine any valid time stamps')

        self._bbox = self._cube_config.bbox.bbox

        width, height = self._cube_config.size.get(
            'x'), self._cube_config.size.get('y')

        x1, y1, x2, y2 = self._bbox
        x_array = np.linspace(x1, x2, width, dtype=np.float64)
        y_array = np.linspace(y2, y1, height, dtype=np.float64)
        self._x_ranges = x_array
        self._y_ranges = y_array

        crs = pyproj.CRS.from_string(self._cube_config.crs)

        def time_stamp_to_str(ts: pd.Timestamp) -> str:
            """
            Convert to ISO string and strip timezone.
            Used to create numpy datetime64 arrays.
            We cannot create directly from pd.Timestamp because Numpy doesn't
            like parsing timezones anymore.
            """
            ts_str: str = ts.isoformat()
            if ts_str[-1] == 'Z':
                return ts_str[0:-1]
            try:
                i = ts_str.rindex('+')
                return ts_str[0: i]
            except ValueError:
                return ts_str

        t_array = np.array([time_stamp_to_str(ts)
                            for ts in self._time_ranges],
                           dtype='datetime64[s]').astype(np.int64)

        global_attrs = dict(
            Conventions='CF-1.7',
            # coordinates='time_bnds',
            title=f'{self._cube_config.dataset_name} Data Cube Subset',
            history=[
                dict(
                    program=f'{self._class_name}'
                )
            ],
            date_created=pd.Timestamp.now().isoformat(),
            time_coverage_start=self._time_ranges[0].isoformat(),
            time_coverage_end=self._time_ranges[1].isoformat(),
            time_coverage_duration=(
                self._time_ranges[1] - self._time_ranges[0]
            ).isoformat(),
        )

        if crs.is_geographic:
            x1, y1, x2, y2 = self._bbox
            global_attrs.update(geospatial_lon_min=x1,
                                geospatial_lat_min=y1,
                                geospatial_lon_max=x2,
                                geospatial_lat_max=y2)
        else:
            x1, y1, x2, y2 = self._bbox
            global_attrs.update(projected_x_min=x1,
                                projected_y_min=y1,
                                projected_x_max=x2,
                                projected_y_max=y2)

        # setup Virtual File System (vfs)
        self._vfs = {
            '.zgroup': _dict_to_bytes(dict(zarr_format=2)),
            '.zattrs': _dict_to_bytes(global_attrs)
        }

        if crs.is_geographic:
            x_name, y_name = 'lon', 'lat'
            x_attrs, y_attrs = (
                {
                    "_ARRAY_DIMENSIONS": ['lon'],
                    "units": "decimal_degrees",
                    "long_name": "longitude",
                    "standard_name": "longitude",
                },
                {
                    "_ARRAY_DIMENSIONS": ['lat'],
                    "units": "decimal_degrees",
                    "long_name": "latitude",
                    "standard_name": "latitude",
                }
            )
        else:
            x_name, y_name = 'x', 'y'
            x_attrs, y_attrs = (
                {
                    "_ARRAY_DIMENSIONS": ['x'],
                    "long_name": "x coordinate of projection",
                    "standard_name": "projection_x_coordinate",
                },
                {
                    "_ARRAY_DIMENSIONS": ['y'],
                    "long_name": "y coordinate of projection",
                    "standard_name": "projection_y_coordinate",
                }
            )

        time_attrs = {
            "_ARRAY_DIMENSIONS": ['time'],
            "units": "seconds since 1970-01-01T00:00:00Z",
            "calendar": "proleptic_gregorian",
            "standard_name": "time"
        }

        self._add_static_array(x_name, x_array, x_attrs)
        self._add_static_array(y_name, y_array, y_attrs)
        self._add_static_array('time', t_array, time_attrs)

        crs_var_attrs = dict()
        # if not crs.is_geographic:
        self._add_static_array('crs', np.array(0), dict(
            _ARRAY_DIMENSIONS=[],
            **crs.to_cf()))
        crs_var_attrs['grid_mapping'] = 'crs'

        if crs.is_geographic:
            band_array_dimensions = ['time', 'lat', 'lon']
        else:
            band_array_dimensions = ['time', 'y', 'x']

        for var_name in self._cube_config.variable_names:
            size = (self._cube_config.size.get('time'),
                    self._cube_config.size.get('y'),
                    self._cube_config.size.get('x'))

            chunk_size = (self._cube_config.chunk_size.get(var_name).get('time'),
                          self._cube_config.chunk_size.get(var_name).get('y'),
                          self._cube_config.chunk_size.get(var_name).get('x'))
            var_encoding = self.get_band_encoding(var_name)
            var_attrs = self.get_var_attrs(var_name)
            var_attrs.update(_ARRAY_DIMENSIONS=band_array_dimensions)
            self._add_remote_array(var_name,
                                   [*size],
                                   [*chunk_size],
                                   var_encoding,
                                   {**var_attrs, **crs_var_attrs})

        self._consolidate_metadata()

    @abstractmethod
    def get_var_attrs(self, var_name: str) -> Dict[str, Any]:
        """
        Get any metadata attributes for variable var_name.
        """
        pass

    @abstractmethod
    def get_band_encoding(self, var_name: str) -> Dict[str, Any]:
        """
        Get data encoding of a variable.
        """
        pass

    @abstractmethod
    def fetch_chunk(self,
                    key: str,
                    band_name: str,
                    bbox: Tuple[float, float, float, float],
                    time_range: Tuple[pd.Timestamp, pd.Timestamp]) -> bytes:
        """
        Fetch chunk data from remote.
        """
        pass

    def get_bbox_chunk_info(self,
                            x_chunk_index: int,
                            y_chunk_index: int,
                            x_chunk_size: int,
                            y_chunk_size: int) -> Tuple[float, float, float, float]:
        """
        Get xy dimension information about a given chunk, based on chunk index
        of the xy dimension.

        Args:
            x_chunk_index (int): Start index of the chunk in
                the x dimension.
            y_chunk_index (int): Start index of the chunk in
                the y dimension.
            x_chunk_size (int): Size of the chunk in the x dimension.
            y_chunk_size (int): Size of the chunk in the y dimension.

        Returns:
            Tuple[float, float, float, float]: Tuple of bounding box.
        """

        x_start_index = x_chunk_index * x_chunk_size
        y_start_index = y_chunk_index * y_chunk_size
        x_end_index = x_chunk_index * x_chunk_size + x_chunk_size - 1
        y_end_index = y_chunk_index * y_chunk_size + y_chunk_size - 1

        x1 = self._x_ranges[x_start_index]
        x2 = self._x_ranges[x_end_index]

        # The reverse in y direction because of upper-left corner indexing start
        # i.e. the minimum value of a bounding box in the y direction is the 
        # x last value of the y coordinate array
        y1 = self._y_ranges[y_end_index]
        y2 = self._y_ranges[y_start_index]

        return (x1, y1, x2, y2)

    def get_time_chunk_info(self,
                            time_chunk_index: int,
                            time_chunk_size: int
                            ) -> Tuple[pd.Timestamp, pd.Timestamp, int]:
        """
        Get time dimension information about a given chunk, based on chunk index
        of the time dimension.

        Args:
            time_chunk_index (int): Start index of the chunk in
                the time dimension.
            time_chunk_size (int): Size of the chunk in
                the time dimension.

        Returns:
            Tuple[pd.Timestamp, pd.Timestamp, int]: Tuple of start time, 
                end time and the number of timesteps between them.
        """

        start_index = time_chunk_index * time_chunk_size
        end_index = time_chunk_index * time_chunk_size + time_chunk_size - 1
        end_index = end_index if end_index < len(
            self._time_ranges) else len(self._time_ranges) - 1

        start_time = self._time_ranges[start_index]
        end_time = self._time_ranges[end_index]
        num_dates = len(self._time_ranges[start_index:end_index+1])

        return start_time, end_time, num_dates

    def add_observer(self, observer: Callable):
        """
        Add a request observer.

        Args:
            observer (Callable): A callback function called when remote
                requests are mode: observer(**kwargs).
        """
        self._observers.append(observer)

    def _fetch_chunk(self,
                     key: str,
                     band_name: str,
                     chunk_index: Tuple[int, ...]) -> bytes:

        t_chunk_index, y_chunk_index, x_chunk_index = chunk_index
        chunk_sizes = self._cube_config.chunk_size.get(band_name)
        t_chunk_size, y_chunk_size, x_chunk_size = (chunk_sizes.get('time'),
                                                    chunk_sizes.get('y'),
                                                    chunk_sizes.get('x'))

        request_bbox = self.get_bbox_chunk_info(
            x_chunk_index, y_chunk_index, x_chunk_size, y_chunk_size)

        start_time, end_time, num_dates = self.get_time_chunk_info(
            t_chunk_index, t_chunk_size)

        t0 = time.perf_counter()
        try:
            exception = None
            chunk_data = self.fetch_chunk(key,
                                          band_name,
                                          bbox=request_bbox,
                                          time_range=(start_time, end_time))

            if num_dates < t_chunk_size:

                extend_nan = np.empty(
                    ((t_chunk_size - num_dates)*y_chunk_size * x_chunk_size),
                    dtype='float32')

                extend_nan[:] = np.nan
                extend_nan = extend_nan.tobytes(order='C')

                chunk_data_ed = Blosc(
                    **_REMOTE_ARRAY_COMPRESSOR_PARAMS).decode(buf=chunk_data)

                chunk_data_ed += extend_nan
                chunk_data = Blosc(
                    **_REMOTE_ARRAY_COMPRESSOR_PARAMS).encode(buf=chunk_data_ed)

        except DdcException as err:
            exception = err
            chunk_data = None

        duration = time.perf_counter() - t0

        for observer in self._observers:
            observer(variable_name=band_name,
                     chunk_index=chunk_index,
                     bbox=request_bbox,
                     time_range=(start_time.isoformat(sep='T'),
                                 end_time.isoformat(sep='T')),
                     duration=duration,
                     exception=exception)

        if exception:
            raise exception

        return chunk_data

    def _add_static_array(self, name: str, array: np.ndarray, attrs: Dict):
        shape = list(map(int, array.shape))
        dtype = str(array.dtype.str)
        order = "C"
        array_metadata = {
            "zarr_format": 2,
            "chunks": shape,
            "shape": shape,
            "dtype": dtype,
            "fill_value": None,
            "compressor": _STATIC_ARRAY_COMPRESSOR_CONFIG,
            "filters": None,
            "order": order,
        }
        chunk_key = '.'.join(['0'] * array.ndim)
        self._vfs[name] = _str_to_bytes('')
        self._vfs[name + '/.zarray'] = _dict_to_bytes(array_metadata)
        self._vfs[name + '/.zattrs'] = _dict_to_bytes(attrs)
        self._vfs[name + '/' +
                  chunk_key] = _STATIC_ARRAY_COMPRESSOR.encode(array.tobytes(order=order))

    def _add_remote_array(self,
                          name: str,
                          shape: List[int],
                          chunks: List[int],
                          encoding: Dict[str, Any],
                          attrs: Dict):
        array_metadata = dict(zarr_format=2,
                              shape=shape,
                              chunks=chunks,
                              compressor=None,
                              fill_value=None,
                              filters=None,
                              order='C')
        array_metadata.update(encoding)
        self._vfs[name] = _str_to_bytes('')
        self._vfs[name + '/.zarray'] = _dict_to_bytes(array_metadata)
        self._vfs[name + '/.zattrs'] = _dict_to_bytes(attrs)
        nums = - (np.array(shape) // - np.array(chunks))
        indexes = itertools.product(*tuple(map(range, map(int, nums))))
        for index in indexes:
            filename = '.'.join(map(str, index))
            # noinspection PyTypeChecker
            self._vfs[name + '/' + filename] = name, index

    def _consolidate_metadata(self):
        metadata = dict()
        for k, v in self._vfs.items():
            if k == '.zattrs' or k.endswith('/.zattrs') \
                    or k == '.zarray' or k.endswith('/.zarray') \
                    or k == '.zgroup' or k.endswith('/.zgroup'):
                metadata[k] = _bytes_to_dict(v)
        self._vfs['.zmetadata'] = _dict_to_bytes(
            dict(zarr_consolidated_format=1, metadata=metadata)
        )

    @property
    def cube_config(self) -> CubeConfig:
        return self._cube_config

    @property
    def _class_name(self):
        return self.__module__ + '.' + self.__class__.__name__

    ##########################################################################
    # Zarr Store (MutableMapping) implementation
    ##########################################################################

    def keys(self) -> KeysView[str]:
        if self._trace_store_calls:
            print(f'{self._class_name}.keys()')
        return self._vfs.keys()

    def listdir(self, key: str) -> Iterable[str]:
        if self._trace_store_calls:
            print(f'{self._class_name}.listdir(key={key!r})')
        if key == '':
            return list((k for k in self._vfs.keys() if '/' not in k))
        else:
            prefix = key + '/'
            start = len(prefix)
            return list((k for k in self._vfs.keys()
                         if k.startswith(prefix) and k.find('/', start) == -1))

    def getsize(self, key: str) -> int:
        if self._trace_store_calls:
            print(f'{self._class_name}.getsize(key={key!r})')
        return len(self._vfs[key])

    def __iter__(self) -> Iterator[str]:
        if self._trace_store_calls:
            print(f'{self._class_name}.__iter__()')
        return iter(self._vfs.keys())

    def __len__(self) -> int:
        if self._trace_store_calls:
            print(f'{self._class_name}.__len__()')
        return len(self._vfs.keys())

    def __contains__(self, key) -> bool:
        if self._trace_store_calls:
            print(f'{self._class_name}.__contains__(key={key!r})')
        return key in self._vfs

    def __getitem__(self, key: str) -> bytes:
        if self._trace_store_calls:
            print(f'{self._class_name}.__getitem__(key={key!r})')
        value = self._vfs[key]
        if isinstance(value, tuple):
            return self._fetch_chunk(key, *value)
        return value

    def __setitem__(self, key: str, value: bytes) -> None:
        if self._trace_store_calls:
            print(
                f'{self._class_name}.__setitem__(key={key!r}, value={value!r})'
            )
        raise TypeError(f'{self._class_name} is read-only')

    def __delitem__(self, key: str) -> None:
        if self._trace_store_calls:
            print(f'{self._class_name}.__delitem__(key={key!r})')
        raise TypeError(f'{self._class_name} is read-only')


class DdcChunkStore(RemoteStore):  # RemoteStore):
    """
    A remote Zarr Store using DanubeDataCube portal as backend for DDC
    environemntal datasets.

    Args:
        cube_config (CustomCubeConfig): Custom cube configuration.
        observer (Optional[Callable]): An optional callback function called when
            remote requests are mode: observer(**kwargs).
        trace_store_calls (bool): Whether store calls shall be
            printed (for debugging).

    """

    _SAMPLE_TYPE_TO_DTYPE = {
        'uint8': '|u1',
        'uint16': '<u2',
        'uint32': '<u4',
        'int8': '|u1',
        'int16': '<u2',
        'int32': '<u4',
        'float32': '<f4',
        'float64': '<f8',
        'bool': '|b1',
    }

    def __init__(self,
                 cube_config: DdcCubeConfig,
                 observer: Optional[Callable] = None,
                 trace_store_calls=False):

        self._danube_data_cube = cube_config.danube_data_cube

        super().__init__(cube_config=cube_config,
                         observer=observer,
                         trace_store_calls=trace_store_calls)

    def get_var_attrs(self, var_name: str) -> Dict[str, Any]:
        band_metadata = self._danube_data_cube.dataset_var(
            self._cube_config.dataset_name,
            var_name,
            default={}
        )
        if 'fill_value' in band_metadata:
            band_metadata.pop('fill_value')
        return band_metadata

    def get_band_encoding(self, var_name: str) -> Dict[str, Any]:

        if isinstance(self._cube_config.datatype, dict):
            sample_type = self._cube_config.datatype.get(var_name)
        else:
            sample_type = 'float32'

        # Convert to sample type name to Zarr dtype value
        dtype = self._SAMPLE_TYPE_TO_DTYPE.get(str(sample_type))
        if dtype is None:
            raise TypeError(f'Invalid sample type {sample_type!r},'
                            f' must be one of'
                            f' {tuple(self._SAMPLE_TYPE_TO_DTYPE.keys())}.')

        fill_value = None

        return dict(dtype=dtype,
                    fill_value=fill_value,
                    compressor=_REMOTE_ARRAY_COMPRESSOR_CONFIG,
                    order='C')

    def fetch_chunk(self,
                    key: str,
                    band_name: str,
                    bbox: Tuple[float, float, float, float],
                    time_range: Tuple[pd.Timestamp, pd.Timestamp]) -> bytes:

        time_period = self.cube_config.time_period
        dataset = self.cube_config.dataset_name.lower()
        bbox = ','.join(map(str, bbox))
        start_time, end_time = time_range
        start_time, end_time = (start_time.isoformat(sep='T').split('T')[0],
                                end_time.isoformat(sep='T').split('T')[0])

        request = dict(
            dataset=dataset,
            variable=band_name,
            time_range_start=start_time,
            time_range_end=end_time,
            time_period=time_period,
            bbox=bbox
        )

        try:
            response = self._danube_data_cube.get_data(
                route='/dynamic_data_cube/get_binary', request=request)
        except DdcRequestError as err:
            raise DdcException(
                f'{key}: cannot fetch chunk for variable {band_name}, '
                f'bbox {bbox}, and time_range {time_range}') from err

        return response.content


class CustomChunkStore(RemoteStore):
    """
    A remote Zarr Store using DanubeDataCube portal as backend for
    Custom datasets.

    Args:
        cube_config (CustomCubeConfig): Custom cube configuration.
        observer (Optional[Callable]): An optional callback function called when
            remote requests are mode: observer(**kwargs).
        trace_store_calls (bool): Whether store calls shall be
            printed (for debugging).
    """

    _SAMPLE_TYPE_TO_DTYPE = {
        'uint8': '|u1',
        'uint16': '<u2',
        'uint32': '<u4',
        'int8': '|u1',
        'int16': '<u2',
        'int32': '<u4',
        'float32': '<f4',
        'float64': '<f8',
        'bool': '|b1',
    }

    def __init__(self,
                 cube_config: CustomCubeConfig,
                 observer: Optional[Callable] = None,
                 trace_store_calls=False):

        self._danube_data_cube = cube_config.danube_data_cube

        super().__init__(cube_config=cube_config,
                         observer=observer,
                         trace_store_calls=trace_store_calls)

    def get_var_attrs(self, var_name: str) -> Dict[str, Any]:
        return {}

    def get_band_encoding(self, var_name: str) -> Dict[str, Any]:

        if isinstance(self._cube_config.datatype, dict):
            sample_type = self._cube_config.datatype.get(var_name)
        else:
            sample_type = 'float32'

        # Convert to sample type name to Zarr dtype value
        dtype = self._SAMPLE_TYPE_TO_DTYPE.get(str(sample_type))
        if dtype is None:
            raise TypeError(f'Invalid sample type {sample_type!r},'
                            f' must be one of'
                            f' {tuple(self._SAMPLE_TYPE_TO_DTYPE.keys())}.')

        fill_value = None

        return dict(dtype=dtype,
                    fill_value=fill_value,
                    compressor=_REMOTE_ARRAY_COMPRESSOR_CONFIG,
                    order='C')

    def fetch_chunk(self,
                    key: str,
                    band_name: str,
                    bbox: Tuple[float, float, float, float],
                    time_range: Tuple[pd.Timestamp, pd.Timestamp]) -> bytes:

        dataset = self.cube_config.dataset_name.lower()
        bbox = ','.join(map(str, bbox))
        start_time, end_time = time_range
        start_time, end_time = (start_time.isoformat(sep='T').split('T')[0],
                                end_time.isoformat(sep='T').split('T')[0])

        request = {
            'dataset': dataset,
            'variable': band_name,
            'time_range_start': start_time,
            'time_range_end': end_time,
            'bbox': bbox
        }

        try:
            response = self._danube_data_cube.get_data(
                route='/dynamic_data_cube/get_custom_binary', request=request)
        except DdcRequestError as err:
            raise DdcException(
                f'{key}: cannot fetch chunk for variable {band_name}, '
                f'bbox {bbox}, and time_range {time_range}') from err

        return response.content
