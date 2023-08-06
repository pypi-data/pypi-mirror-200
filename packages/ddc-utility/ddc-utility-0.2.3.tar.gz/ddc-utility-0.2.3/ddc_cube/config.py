from __future__ import annotations

import math
from abc import ABC
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from dask.array.core import auto_chunks
from pydantic import BaseModel, Extra, root_validator, validator

from .constants import DDC_MAX_CHUNK_SIZE, DEFAULT_CRS, TIME_PERIODS
from .ddc import DanubeDataCube
from .errors import DdcConfigurationError
from .utils import Bbox, TimeRange


class CubeConfig(BaseModel, ABC):
    """
    Cube configuration abstract interface for various data collections.
    Specific configuration implementations can inheret from this base class.


    Attributes:
        dataset_name (str): Name of the dataset.
        variable_names (Optional[List[str]]): Variable names
            of the dataset.

    """

    dataset_name: str
    variable_names: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


class CustomCubeConfig(CubeConfig):
    """
    Cube configuration for Custom datasets.

    Attributes:
        dataset_name (str): Name of the custom zarr dataset, with '.zarr'
            extension at the end.
        variable_names (Optional[List[str]], optional): Variable names
            of the dataset.
        danube_data_cube Optional[DanubeDataCube]: Instance of DanubeDataCube,
            the object representing the DanubeDataCube API.
        param ddc_kwargs: Optional keyword arguments passed to the
            DanubeDataCube constructor. Only used if
            'danube_data_cube' is not given.

    """

    dataset_name: str
    variable_names: Optional[List[str]] = None
    danube_data_cube: Optional[DanubeDataCube] = None

    @validator('dataset_name')
    def check_dataset_name(cls, val):
        if val.split('.')[-1] != 'zarr':
            raise ValueError(
                'Invalid dataset, dataset_name must be with .zarr extension.')
        return val

    def __init__(self,
                 dataset_name: str,
                 variable_names: Optional[List[str]] = None,
                 danube_data_cube: Optional[DanubeDataCube] = None,
                 **ddc_kwargs) -> None:
        """Custom init."""

        if danube_data_cube is None:
            try:
                danube_data_cube = DanubeDataCube(**ddc_kwargs)
            except (TypeError, ValueError) as exc:
                raise DdcConfigurationError(
                    "Coudn't initialize DanubeDataCube object with the "
                    f"supported arguments {ddc_kwargs}") from exc

        super().__init__(dataset_name=dataset_name,
                         variable_names=variable_names,
                         danube_data_cube=danube_data_cube)

        src_properties = danube_data_cube.get_custom_properties(
            self.dataset_name)

        data = self.configure(src_properties)

        for key, value in data.items():
            setattr(self, key, value)


    def configure(self, src_properties: Dict) -> Dict:
        """
        Executes further validations based on source dataset and
        modifies parameters if neccessary.

        Args:
            src_properties (Dict): Source dataset properties.
        """
        # retrieve source metadata and convert those to correct types
        # improve this with metadata api response
        src_variable_names = src_properties.get('bands')

        src_bbox = Bbox(*src_properties.get('bbox'))

        src_crs = src_properties.get('crs')

        src_datatype = src_properties.get('dtypes')

        src_spatial_res = float(src_properties.get('spatial_res'))

        src_dimensions = src_properties.get('dimensions')

        src_time_lst = pd.to_datetime(src_properties.get('time_lst')).sort_values()

        # Adjust user defined input arguments with the source parameters
        variable_names = self._get_variable_names(src_variable_names, self.variable_names)

        datatype = {k: np.dtype(src_datatype.get(k)) for k in variable_names}

        depth = src_dimensions.get('time')
        width = src_dimensions.get('x')
        height = src_dimensions.get('y')

        width, height, chunk_w, chunk_h = self._get_xy_chunk_size(width, height)

        chunk_size = {}
        num_chunks = {}

        for var in variable_names:
            dt = datatype[var]

            chunk_d = self._get_t_chunk_size(
                chunk_w, chunk_h, depth, width, height, dt)

            chunk_size[var] = {'time': chunk_d, 'x': chunk_w, 'y': chunk_h}

            num_chunks[var] = (math.ceil(depth / chunk_d),
                               width // chunk_w, height // chunk_h)

        return {
            'variable_names': variable_names,
            'datatype': datatype,
            'size': {'time': depth, 'x': width, 'y': height},
            'chunk_size': chunk_size,
            'num_chunks': num_chunks,
            'bbox': src_bbox,
            'spatial_res': src_spatial_res,
            'crs': src_crs,
            'time_lst': src_time_lst,
            'time_range': TimeRange(src_time_lst[0], src_time_lst[-1])
        }

    def _get_variable_names(self,
                           src_variable_names: List[str],
                           variable_names: Optional[List[str]] = None
                           ) -> List[str]:
        if not variable_names:
            variable_names = src_variable_names
        else:
            variable_names = list(set(variable_names) & set(src_variable_names))
        return variable_names

    def _get_xy_chunk_size(self,
                          width: int,
                          height: int) -> Tuple[int, int, int, int]:

        chunk_width = width
        chunk_height = height
        return width, height, chunk_width, chunk_height
    
    def _get_t_chunk_size(self,
                         chunk_width: int,
                         chunk_height: int,
                         depth: int,
                         width: int,
                         height: int,
                         datatype: np.dtype) -> Tuple[int, int, int]:
        """Return chunk_size in the time dimension."""

        chunk_depth, chunk_width, chunk_height = auto_chunks(
            ('auto', chunk_width, chunk_height),
            (depth, width, height), DDC_MAX_CHUNK_SIZE, datatype)

        if isinstance(chunk_depth, tuple):
            chunk_depth = chunk_depth[0]

        if depth < 1.2 * chunk_depth:
            chunk_depth = depth

        return chunk_depth



class DdcCubeConfig(CubeConfig):
    """
    Cube configuration for DDC datasets.

    Args:
        dataset_name (str): Name of the dataset.
        variable_names (Optional[List[str]], optional): Variable names
            of the dataset.
        bbox (Optional[Bbox], optional): Bounding box, tuple of 4 numbers:
            (minx, miny, maxx, maxy). Must be is WGS 84 coordinates.
        time_range (Optional[TimeRange], optional): Time range tuple:
            (start time, end time).
        time_period (Optional[str, None], optional): A string denoting
            the temporal aggregation period, such as "8D", "1W", "1M".
        danube_data_cube: Instance of DanubeDataCube,
            the object representing the DanubeDataCube API.
        param ddc_kwargs: Optional keyword arguments passed to the
            DanubeDataCube constructor. Only valid if
            danube_data_cube is not given.
    """

    dataset_name: str
    variable_names: Optional[List[str]] = None
    bbox: Optional[Bbox] = None
    time_range: Optional[TimeRange]= None
    time_period: Optional[str] = None
    danube_data_cube: Optional[DanubeDataCube] = None 

    @validator('dataset_name')
    def convert_dataset_name(cls, val):
        return val.upper()

    @validator('time_period')
    def check_time_period(cls, val):
        if val and val not in TIME_PERIODS:
            raise ValueError(
                f"Invalid value for time_period: {val} "
                f"- must be one of {TIME_PERIODS}")
        return val

    @root_validator
    def check_dataset_name(cls, values):
        ddc = values.get('danube_data_cube')
        dataset_name = values.get('dataset_name')
        if dataset_name not in ddc.dataset_names:
            raise ValueError(
                f'Invalid dataset, dataset_name must be in {ddc.dataset_names}')
        return values

    def __init__(self,
                 dataset_name: str,
                 variable_names: Optional[List[str]] = None,
                 bbox: Optional[Bbox] = None,
                 time_range: Optional[TimeRange] = None,
                 time_period: Optional[str] = None,
                 danube_data_cube: Optional[DanubeDataCube] = None,
                 **ddc_kwargs) -> None:
        """Custom init."""

        if danube_data_cube is None:
            try:
                danube_data_cube = DanubeDataCube(**ddc_kwargs)
            except (TypeError, ValueError) as exc:
                raise DdcConfigurationError(
                    "Coudn't initialize DanubeDataCube object with the "
                    f"supported arguments {ddc_kwargs}") from exc

        super().__init__(dataset_name=dataset_name,
                         variable_names=variable_names,
                         bbox=bbox,
                         time_range=time_range,
                         time_period=time_period,
                         danube_data_cube=danube_data_cube)

        src_properties = danube_data_cube.get_properties(self.dataset_name)

        data = self.configure(src_properties)

        for key, value in data.items():
            setattr(self, key, value)


    def configure(self, src_properties: Dict) -> Dict:
        """
        Executes further validations based on source dataset and
        modifies parameters if neccessary.

        Args:
            src_properties (Dict): Source dataset properties.
        """
        # retrieve source metadata and convert those to correct types
        # improve this with metadata api response
        src_variable_names = list(src_properties.get('datatypes').keys())

        src_bbox = Bbox(*src_properties.get('bbox').split(','))

        src_datatype = src_properties.get('datatypes')

        src_spatial_res = float(src_properties.get('spatial_res'))

        src_time_lst = pd.to_datetime(src_properties.get('time_lst'))

        # Adjust user defined input arguments with the source parameters
        variable_names = self._get_variable_names(src_variable_names, self.variable_names)

        datatype = {k: np.dtype(src_datatype.get(k)) for k in variable_names}

        bbox = self._get_bbox(src_bbox, self.bbox, src_spatial_res)

        time_lst = self._get_time_lst(src_time_lst, self.time_range, self.time_period) 

        depth = self._get_t_size(time_lst)
        width, height = self._get_xy_size(bbox, src_spatial_res)

        base_dt = max(datatype.values())
        width, height, chunk_w, chunk_h = self._get_xy_chunk_size(width, height, base_dt)

        time_freq = self.time_period or 'original'
        # readjust bbox based on new size
        bbox.maxx = bbox.minx + (width-1) * src_spatial_res
        bbox.maxy = bbox.miny + (height-1) * src_spatial_res

        chunk_size = {}
        num_chunks = {}

        # get chunksize in time dim. Size of the chunks can be varied on the
        # time dimension based on the variable's datatype
        for var in variable_names:

            dt = datatype[var]

            chunk_d = self._get_t_chunk_size(
                chunk_w, chunk_h, depth, width, height, dt)

            chunk_size[var] = {'time': chunk_d, 'x': chunk_w, 'y': chunk_h}

            num_chunks[var] = (math.ceil(depth / chunk_d),
                               width // chunk_w, height // chunk_h)
    
        return {
            'variable_names': variable_names,
            'datatype': datatype,
            'size': {'time': depth, 'x': width, 'y': height},
            'chunk_size': chunk_size,
            'num_chunks': num_chunks,
            'bbox': bbox,
            'spatial_res': src_spatial_res,
            'crs': DEFAULT_CRS,
            'time_range': TimeRange(time_lst[0], time_lst[-1]),
            'time_lst': time_lst,
            'time_period': time_freq
        }

    def _get_variable_names(self,
                           src_variable_names: List[str],
                           variable_names: Optional[List[str]] = None
                           ) -> List[str]:
        if not variable_names:
            variable_names = src_variable_names
        else:
            variable_names = list(set(variable_names) & set(src_variable_names))
        return variable_names

    def _get_bbox(self,
                 src_bbox: Bbox,
                 bbox: Optional[Bbox] = None,
                 spatial_res: Optional[float] = None) -> Bbox:

        if not bbox:
            bbox = src_bbox
        else:
            x1 = bbox.minx if bbox.minx >= src_bbox.minx else src_bbox.minx
            y1 = bbox.miny if bbox.miny >= src_bbox.miny else src_bbox.miny
            x2 = bbox.maxx if bbox.maxx <= src_bbox.maxx else src_bbox.maxx
            y2 = bbox.maxy if bbox.maxy <= src_bbox.maxy else src_bbox.maxy
            precision = len(str(spatial_res).split('.')[-1])
            bbox = Bbox(x1, y1, x2, y2, precision)

        return bbox

    def _get_time_lst(self,
                     src_time_lst: pd.DatetimeIndex,
                     time_range: Optional[TimeRange] = None,
                     time_period: Optional[str] = None) -> pd.DatetimeIndex:

        if not time_range:
            time_lst = src_time_lst
        else:
            time_lst = src_time_lst[
                (src_time_lst >= time_range.start_time) &
                (src_time_lst <= time_range.end_time)
                ]
           
            if len(time_lst) == 0:
                raise ValueError(f'Invalid time_range {time_range.time_range} '
                                 '-- results in an empty time range list')
       
        if time_period:
            time_lst = pd.date_range(
                time_lst[0], time_lst[-1], freq=time_period, inclusive='both')

        return time_lst

    def _get_t_size(self, time_lst: pd.DatetimeIndex) -> int:
        return len(time_lst)

    def _get_xy_size(self,
                    bbox: Bbox,
                    spatial_res: float) -> Tuple[int, int]:

        x1, y1, x2, y2 = bbox.bbox
        x_array = np.arange(x1, x2, spatial_res, dtype=np.float64)
        y_array = np.arange(y1, y2, spatial_res, dtype=np.float64)
        width, height = x_array.size, y_array.size
        return width, height

    def _get_xy_chunk_size(self,
                          width: int,
                          height: int,
                          datatype: np.dtype) -> Tuple[int, int, int, int]:

        item_size = datatype.itemsize
        num_pixels_per_chunk = DDC_MAX_CHUNK_SIZE / item_size
        chunk_width = math.ceil(
            math.sqrt(width * num_pixels_per_chunk / height))
        chunk_height = math.ceil((
            num_pixels_per_chunk + chunk_width - 1) // chunk_width)

        def _adjust_size(size: int, chunk_size: int) -> int:
            if size > chunk_size:
                num_chunk = size // chunk_size
                size = num_chunk * chunk_size
            return int(size)

        if width < 1.2 * chunk_width:
            chunk_width = width
        else:
            width = _adjust_size(width, chunk_width)
        if height < 1.2 * chunk_height:
            chunk_height = height
        else:
            height = _adjust_size(height, chunk_height)

        return width, height, chunk_width, chunk_height

    def _get_t_chunk_size(self,
                         chunk_width: int,
                         chunk_height: int,
                         depth: int,
                         width: int,
                         height: int,
                         datatype: np.dtype) -> int:
        """Return chunk_size in the time dimension."""

        chunk_depth, chunk_width, chunk_height = auto_chunks(
            ('auto', chunk_width, chunk_height),
            (depth, width, height), DDC_MAX_CHUNK_SIZE, datatype)

        if isinstance(chunk_depth, tuple):
            chunk_depth = chunk_depth[0]

        if depth < 1.2 * chunk_depth:
            chunk_depth = depth

        return chunk_depth
