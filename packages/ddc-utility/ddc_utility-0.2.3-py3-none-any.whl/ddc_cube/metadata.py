
from typing import Dict, List, Optional


class DanubeDataCubeMetadata:

    def __init__(self):
        self._metadata = _DDC_METADATA

    @property
    def datasets(self) -> Dict:
        return dict(self._metadata['datasets'])

    @property
    def dataset_names(self) -> List[str]:
        return [ds_id for ds_id in self._metadata['datasets']]

    def dataset(self, dataset_name: str) -> Optional[Dict]:
        dataset = self._dataset_direct(dataset_name)
        return dict(dataset) if dataset is not None else None

    def dataset_vars(self, dataset_name: str, default=None) -> \
            Optional[Dict]:
        variables = self._dataset_vars_direct(dataset_name)
        return dict(variables) if variables else default

    def dataset_vars_names(self, dataset_name: str, default=None) -> \
            Optional[List[str]]:
        variables = self._dataset_vars_direct(dataset_name)
        return [var_name for var_name in variables] if variables else default

    def dataset_var(self, dataset_name: str, variable_name: str, default=None) \
            -> Optional[Dict]:
        var = self._dataset_var_direct(dataset_name, variable_name)
        return dict(var) if var else default

    def _dataset_direct(self, dataset_name: str) -> Optional[Dict]:
        return self._metadata['datasets'].get(dataset_name.upper())

    def _dataset_vars_direct(self, dataset_name: str) \
            -> Optional[Dict]:
        dataset = self._dataset_direct(dataset_name)
        return dataset.get('variables') if dataset else None

    def _dataset_var_direct(self, dataset_name: str, variable_name: str) \
            -> Optional[Dict]:
        variables = self._dataset_vars_direct(dataset_name)
        return variables.get(variable_name) if variables else None


_FORECAST_VAR_METADATA = {
    'temp_min': {
        'units': '°C',
        'long_name': 'Minimum temperature (2 m)',
        'standard_name': 'min_air_temperature_2m',
        'coverage_content_type': 'physicalMeasurement',
    },
    'temp_max': {
        'units': '°C',
        'long_name': 'Maximum temperature (2 m)',
        'standard_name': 'max_air_temperature_2m',
        'coverage_content_type': 'physicalMeasurement',
    },
    'temp_avg': {
        'units': '°C',
        'long_name': 'Average temperature (2 m)',
        'standard_name': 'avg_air_temperature_2m',
        'coverage_content_type': 'physicalMeasurement',
    },
    'prec': {
        'units': 'mm',
        'long_name': 'Precipitation amount',
        'standard_name': 'precipitation_mm',
        'coverage_content_type': 'physicalMeasurement',
    },
    'et0': {
        'units': 'mm',
        'long_name': 'Potential evapotranspiration',
        'standard_name': 'evapotranspiration_mm',
        'coverage_content_type': 'physicalMeasurement',
    }
}


_MET_VAR_METADATA = {
    'temp_min': {
        'units': '°C',
        'long_name': 'Minimum temperature (2 m)',
        'standard_name': 'min_air_temperature_2m',
        'coverage_content_type': 'physicalMeasurement',
    },
    'temp_max': {
        'units': '°C',
        'long_name': 'Maximum temperature (2 m)',
        'standard_name': 'max_air_temperature_2m',
        'coverage_content_type': 'physicalMeasurement',
    },
    'temp_avg': {
        'units': '°C',
        'long_name': 'Average temperature (2 m)',
        'standard_name': 'avg_air_temperature_2m',
        'coverage_content_type': 'physicalMeasurement',
    },
    'prec': {
        'units': 'mm',
        'long_name': 'Precipitation amount',
        'standard_name': 'precipitation_mm',
        'coverage_content_type': 'physicalMeasurement',
    },
    'eto': {
        'units': 'mm',
        'long_name': 'Potential evapotranspiration',
        'standard_name': 'evapotranspiration_mm',
        'coverage_content_type': 'physicalMeasurement',
    }
}


_SOIL1_VAR_METADATA = {
    'soil1': {
        'units': None,
        'long_name': None,
        'standard_name': None,
        'coverage_content_type': None,
        'spatial_extent': None,
        'spatial_resolution': None,
        'temporal_extent': None,
        'temporal_resolution': None,
    }
}


_NHRL_VAR_METADATA = {
    'nhrl': {
        'units': None,
        'long_name': 'Land cover and land use thematic map',
        'standard_name': 'landcover_categories',
        'coverage_content_type': 'thematic_classification',
        'spatial_extent': None,
        'spatial_resolution': '20 m (~ ... deg)',
        'temporal_extent': '2016.01.01 - 2021.01.01',
        'temporal_resolution': 'yearly',
    }
}

_ECOSYSTEM_VAR_METADATA = {
    'ecosystem': {
        'units': None,
        'long_name': 'Ecosystem thematic map',
        'standard_name': 'ecosystem_categories',
        'coverage_content_type': 'thematic_classification',
    }
}


_DDC_METADATA = dict(
    datasets={
        'METEOROLOGY_FORECAST': dict(
            title='Meteorological forecast data',
            description='Interpolated grids of meteorological forecast.',
            variables=_FORECAST_VAR_METADATA,
            crs='EPSG:4326'
        ),
        'METEOROLOGY': dict(
            title='Meteorological measurements',
            description='Interpolated grids of meteorological measurements.',
            variables=_MET_VAR_METADATA,
            crs='EPSG:4326'
        ),
        'SOIL': dict(
            title='Soil data',
            variables=_SOIL1_VAR_METADATA,
            crs='EPSG:4326',
            spatial_res=0.0001,
            time_period='1Y',
            def_time_offset={'years': 1},
            def_start_date='1971-01-01',
            def_end_date=None
        ),
        'NHRL': dict(
            title='National High-Resolution Layer of Hungary (NHRL)',
            variables=_NHRL_VAR_METADATA,
            crs='EPSG:4326',
            spatial_res=0.0001,
            time_period='1Y',
            start_date='2016-01-01',
            end_date='2021-01-01',
            bbox=(15.150146, 44.894796, 23.774414, 48.980217)
        ),
        'ECOSYSTEM': dict(
            title='Ecosystem Map of Hungary',
            variables=_ECOSYSTEM_VAR_METADATA,
            crs='EPSG:4326',
            time_period='1Y',
            def_time_offset={'years': 1},
            def_start_date='2015-01-01',
            def_end_date='2015-01-01',
            spatial_extent=None,
            spatial_res='20 m (~ ... deg)',
            temporal_extent='2016.01.01 - 2021.01.01',
            temporal_resolution='yearly',
        ),
    }
)
