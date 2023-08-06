"""Prepare user data for weight generation."""
import logging
import time
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import List
from typing import Union

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from pyproj import CRS
from shapely.geometry import box

from gdptools.data.agg_gen_data import AggData
from gdptools.data.odap_cat_data import CatGrids
from gdptools.data.odap_cat_data import CatParams
from gdptools.data.weight_gen_data import WeightData
from gdptools.helpers import build_subset
from gdptools.helpers import build_subset_tiff
from gdptools.utils import _check_for_intersection
from gdptools.utils import _check_for_intersection_nc
from gdptools.utils import _get_cells_poly
from gdptools.utils import _get_data_via_catalog
from gdptools.utils import _get_geodataframe
from gdptools.utils import _get_rxr_dataset
from gdptools.utils import _get_shp_bounds_w_buffer
from gdptools.utils import _get_shp_file
from gdptools.utils import _get_top_to_bottom
from gdptools.utils import _get_xr_dataset
from gdptools.utils import _read_shp_file

logger = logging.getLogger(__name__)


class UserData(ABC):
    """Prepare data for different sources for weight generation."""

    @abstractmethod
    def __init__(self) -> None:
        """Init class."""
        pass

    @abstractmethod
    def get_source_subset(self, key: str) -> xr.DataArray:
        """Abstract method for getting subset of source data."""
        pass

    @abstractmethod
    def prep_wght_data(self) -> WeightData:
        """Abstract interface for generating weight data."""
        pass

    @abstractmethod
    def prep_agg_data(self, key: str) -> AggData:
        """Abstract method for preparing data for aggregation."""
        pass

    @abstractmethod
    def get_vars(self) -> list[str]:
        """Return a list of variables."""
        pass

    @abstractmethod
    def get_feature_id(self) -> str:
        """Abstract method for returning the id_feature parameter."""
        pass


class ClimRCatData(UserData):
    """Instance of UserData using Climate-R catalog data."""

    def __init__(
        self: "ClimRCatData",
        *,
        cat_dict: dict[str, dict[str, Any]],
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        id_feature: str,
        period: List[str],
    ) -> None:  # sourcery skip: simplify-len-comparison
        """Initialize ClimRCatData class.

        This class uses wraps the ClimateR-catalogs developed by Mike Johnson
        and available here:

        'https://mikejohnson51.github.io/climateR-catalogs/catalog.json'

        This can be queried in pandas to return the dictionary associated with a
        specific source and variable as in the ClimateR-catalog. The cat_dict arguments
        are composed of a key defined by the variable name and a dictionary of the
        corresponding ClimateR-catalog json string from the.

        Args:
            cat_dict (dict[str, dict]): Parameter metadata from climateR-catalog
                catalog.
            f_feature (Union[str, Path, gpd.GeoDataFrame]): GeoDataFself.rotate_dsrame
                or any path-like object that can be read by geopandas.read_file().
            id_feature (str): Header in GeoDataFrame to use as index for weights.
            period (List[str]): List containing date strings defining start and end
                time slice for aggregation.
        """
        logger.info("Initializing ODAPCatData")
        logger.info("  - loading data")
        self.cat_dict = cat_dict
        self.f_feature = f_feature
        self.id_feature = id_feature
        self.period = pd.to_datetime(period)
        self._check_input_dict()
        self.gdf = _read_shp_file(self.f_feature)

        self._check_id_feature()
        self.keys = self.get_vars()
        self.cat_params, self.cat_grid = self._create_odapcats(key=self.keys[0])

        logger.info("  - checking latitude bounds")
        is_intersect, is_degrees, is_0_360 = _check_for_intersection(
            cat_params=self.cat_params, cat_grid=self.cat_grid, gdf=self.gdf
        )
        self.gdf, self.gdf_bounds = _get_shp_file(
            shp_file=self.gdf, cat_grid=self.cat_grid, is_degrees=is_degrees
        )
        self.rotate_ds = bool((not is_intersect) & is_degrees & (is_0_360))

    def get_source_subset(self, key: str) -> xr.DataArray:
        """get_source_subset Get subset of source data by key.

        _extended_summary_

        Args:
            key (str): _description_

        Returns:
            xr.DataArray: _description_
        """
        return _get_data_via_catalog(
            cat_params=self.cat_params,
            cat_grid=self.cat_grid,
            bounds=self.gdf_bounds,
            begin_date=self.period[0],
            end_date=self.period[1],
            rotate_lon=self.rotate_ds,
        )

    def prep_interp_data(self, key: str, poly_id: int) -> AggData:
        """Prepare data for line-interpolation."""
        cp, cg = self._create_odapcats(key=key)

        # Select a feature and make sure it remains a geodataframe
        feature = self.gdf[
            self.gdf.loc[:, "geometry"] == self.gdf.loc[:, "geometry"][poly_id]
        ]

        # Reproject to grid crs and get bounding box
        crs = cg.proj
        x_cell_size = cg.resX
        y_cell_size = cg.resY
        bbox = box(*feature.to_crs(crs).total_bounds)
        bounds = np.asarray(
            bbox.buffer(2 * max(x_cell_size, y_cell_size)).bounds  # type: ignore
        )

        # Clip grid by x, y and time
        ds_ss = _get_data_via_catalog(
            cat_params=cp,
            cat_grid=cg,
            bounds=bounds,
            begin_date=str(self.period[0]),
            end_date=str(self.period[1]),
            rotate_lon=self.rotate_ds,
        )

        return AggData(
            variable=key,
            cat_param=cp,
            cat_grid=cg,
            da=ds_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_agg_data(self, key: str, poly_id: Union[int, None] = None) -> AggData:
        """Prepare ClimRCatData data for aggregation methods.

        Args:
            key (str): _description_
            poly_id (int): ID of the row of the geodataframe

        Returns:
            AggData: _description_
        """
        cp, cg = self._create_odapcats(key=key)

        feature = self.gdf

        ds_ss = _get_data_via_catalog(
            cat_params=cp,
            cat_grid=cg,
            bounds=self.gdf_bounds,
            begin_date=str(self.period[0]),
            end_date=str(self.period[1]),
            rotate_lon=self.rotate_ds,
        )

        return AggData(
            variable=key,
            cat_param=cp,
            cat_grid=cg,
            da=ds_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_wght_data(self) -> WeightData:
        """Prepare and return WeightData for weight generation."""
        # For weight generation we just need param and grid dict from one variable
        # passed to CatParms and CatGrids.
        cp, cg = self._create_odapcats(key=self.keys[0])
        self.ds_ss = _get_data_via_catalog(
            cat_params=cp,
            cat_grid=cg,
            bounds=self.gdf_bounds,
            begin_date=str(self.period[0]),
            rotate_lon=self.rotate_ds,
        )
        tsrt = time.perf_counter()
        gdf_grid = _get_cells_poly(
            xr_a=self.ds_ss,
            x=cg.X_name,
            y=cg.Y_name,
            crs_in=cg.proj,
        )
        tend = time.perf_counter()
        print(f"grid cells generated in {tend-tsrt:0.4f} seconds")

        return WeightData(
            feature=self.gdf, id_feature=self.id_feature, grid_cells=gdf_grid
        )

    def get_feature_id(self) -> str:
        """Return id_feature."""
        return self.id_feature

    def get_vars(self) -> list[str]:
        """Return list of param_dict keys, proxy for varnames."""
        return list(self.cat_dict.keys())

    def _check_input_dict(self: "ClimRCatData") -> None:
        """Check input cat_dict."""
        if len(self.cat_dict) < 1:
            raise ValueError("param_dict should have at least 1 key,value pair")

    def _check_id_feature(self: "ClimRCatData") -> None:
        """Check id_feature in gdf."""
        if self.id_feature not in self.gdf.columns[:]:
            raise ValueError(
                f"shp_poly_idx: {self.id_feature} not in gdf"
                f" columns: {self.gdf.columns}"
            )

    def _create_odapcats(self: "ClimRCatData", key: str):
        key_dict = self.cat_dict.get(key)
        cp = CatParams(
            id=key_dict.get("id"),
            URL=key_dict.get("URL"),
            varname=key_dict.get("varname"),
            long_name=key_dict.get("description"),
            T_name=key_dict.get("T_name"),
            units=key_dict.get("units"),
        )
        cg = CatGrids(
            X_name=key_dict.get("X_name"),
            Y_name=key_dict.get("Y_name"),
            proj=key_dict.get("crs"),
            resX=key_dict.get("resX"),
            resY=key_dict.get("resY"),
            toptobottom=key_dict.get("toptobottom"),
        )
        return cp, cg


class ODAPCatData(UserData):
    """Instance of UserData using OPeNDAP catalog data."""

    def __init__(
        self,
        *,  # all arguments below must be defined as a keyword argument
        param_dict: dict[str, dict[str, Any]],
        grid_dict: dict[str, dict[str, Any]],
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        id_feature: str,
        period: List[str],
    ) -> None:
        """Initialize ODAPCatData class.

        This class uses a parameter and grid json catalog developed by Mike Johnson
        and available here:

        Param: https://mikejohnson51.github.io/opendap.catalog/cat_params.json
        Grids: https://mikejohnson51.github.io/opendap.catalog/cat_grids.json

        These can be queried in pandas to return the dictionary associated with a
        specific source and variable as in the OPENDaP Catalog examples. The param_dict
        and grid_dict arguments are composed of a key defined by the variable name
        and a dictionary of the corresponding param and grid json string from the
        OPENDaP Catelog.

        Args:
            param_dict (dict[str, dict]): Parameter metadata from OPeNDAP catalog.
            grid_dict (dict[str, dict]): Grid metadata from OPeNDAP catalog.
            f_feature (Union[str, Path, gpd.GeoDataFrame]): GeoDataFself.rotate_dsrame or any
                path-like object that can be read by geopandas.read_file().
            id_feature (str): Header in GeoDataFrame to use as index for weights.
            period (List[str]): List containing date strings defining start and end
                time slice for aggregation.
        """
        logger.info("Initializing ODAPCatData")
        logger.info("  - loading data")
        self.param_dict = param_dict
        self.grid_dict = grid_dict
        self.f_feature = f_feature
        self.id_feature = id_feature
        self.period = pd.to_datetime(period)
        self._check_input_dicts()
        self.keys = self.get_vars()
        self.gdf = _read_shp_file(self.f_feature)
        cp = self._create_catparam(key=self.keys[0])
        cg = self._create_catgrid(key=self.keys[0])
        logger.info("  - checking latitude bounds")
        is_intersect, is_degrees, is_0_360 = _check_for_intersection(
            cat_params=cp, cat_grid=cg, gdf=self.gdf
        )
        self.gdf, self.gdf_bounds = _get_shp_file(
            shp_file=self.f_feature, cat_grid=cg, is_degrees=is_degrees
        )
        self._check_id_feature()
        self.rotate_ds = bool((not is_intersect) & is_degrees & (is_0_360))

    def get_source_subset(self, key: str) -> xr.DataArray:
        """get_source_subset Get data subset from source by key.

        _extended_summary_

        Args:
            key (str): _description_

        Returns:
            xr.DataArray: _description_
        """
        cat_params = CatParams(**self.param_dict[key])
        cat_grid = CatGrids(**self.grid_dict[key])
        # run check on intersection of shape features and gridded data
        return _get_data_via_catalog(
            cat_params=cat_params,
            cat_grid=cat_grid,
            bounds=self.gdf_bounds,
            begin_date=self.period[0],
            end_date=self.period[1],
            rotate_lon=self.rotate_ds,
        )

    def get_feature_id(self) -> str:
        """Return id_feature."""
        return self.id_feature

    def get_vars(self) -> list[str]:
        """Return list of param_dict keys, proxy for varnames."""
        return list(self.param_dict.keys())

    def prep_interp_data(self, key: str, poly_id: int) -> AggData:
        """Prep AggData from UserData.

        Args:
            key (str): Name of the xarray grided data variable
            poly_id (int): ID number of the geodataframe geometry to clip the
                gridded data to

        Returns:
            AggData: An instance of the AggData class
        """
        cp = self._create_catparam(key=key)
        cg = self._create_catgrid(key=key)

        # Select a feature and make sure it remains a geodataframe
        feature = self.gdf[
            self.gdf.loc[:, "geometry"] == self.gdf.loc[:, "geometry"][poly_id]
        ]

        # Reproject to grid crs and get bounding box
        crs = cg.proj
        x_cell_size = cg.resX
        y_cell_size = cg.resY
        bbox = box(*feature.to_crs(crs).total_bounds)
        bounds = np.asarray(
            bbox.buffer(2 * max(x_cell_size, y_cell_size)).bounds  # type: ignore
        )
        # Clip grid by x, y and time
        ds_ss = _get_data_via_catalog(
            cat_params=cp,
            cat_grid=cg,
            bounds=bounds,
            begin_date=str(self.period[0]),
            end_date=str(self.period[1]),
            rotate_lon=self.rotate_ds,
        )

        return AggData(
            variable=key,
            cat_param=cp,
            cat_grid=cg,
            da=ds_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_agg_data(self, key: str, poly_id: Union[int, None] = None) -> AggData:
        """Prepare ODAPCatData data for aggregation methods.

        Args:
            key (str): _description_
            poly_id (int): ID of the row of the geodataframe

        Returns:
            AggData: _description_
        """
        cp = self._create_catparam(key=key)
        cg = self._create_catgrid(key=key)

        feature = self.gdf

        ds_ss = _get_data_via_catalog(
            cat_params=cp,
            cat_grid=cg,
            bounds=self.gdf_bounds,
            begin_date=str(self.period[0]),
            end_date=str(self.period[1]),
            rotate_lon=self.rotate_ds,
        )

        return AggData(
            variable=key,
            cat_param=cp,
            cat_grid=cg,
            da=ds_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_wght_data(self) -> WeightData:
        """Prepare and return WeightData for weight generation."""
        # For weight generation we just need param and grid dict from one variable
        # passed to CatParms and CatGrids.
        cp = self._create_catparam(key=self.keys[0])
        cg = self._create_catgrid(key=self.keys[0])
        self.ds_ss = _get_data_via_catalog(
            cat_params=cp,
            cat_grid=cg,
            bounds=self.gdf_bounds,
            begin_date=str(self.period[0]),
            rotate_lon=self.rotate_ds,
        )
        tsrt = time.perf_counter()
        gdf_grid = _get_cells_poly(
            xr_a=self.ds_ss,
            x=cg.X_name,
            y=cg.Y_name,
            crs_in=cg.proj,
        )
        tend = time.perf_counter()
        print(f"grid cells generated in {tend-tsrt:0.4f} seconds")

        return WeightData(
            feature=self.gdf, id_feature=self.id_feature, grid_cells=gdf_grid
        )

    def _check_id_feature(self: "ODAPCatData") -> None:
        """Check id_feature in gdf."""
        if self.id_feature not in self.gdf.columns[:]:
            raise ValueError(
                f"shp_poly_idx: {self.id_feature} not in gdf columns: {self.gdf.columns}"
            )

    def _create_catgrid(self: "ODAPCatData", key: str) -> CatGrids:
        """Create CatGrids."""
        return CatGrids(**self.grid_dict.get(key))  # type: ignore

    def _create_catparam(self: "ODAPCatData", key: str) -> CatParams:
        """Create CatParams."""
        return CatParams(**self.param_dict.get(key))  # type: ignore

    def _check_input_dicts(self: "ODAPCatData") -> None:
        """Check input dicts are of equal length and with at least one entry."""
        if len(self.param_dict) != len(self.grid_dict):
            raise ValueError(
                "Mismatch in key,value pairs. param_dict and grid_dict \
                should have the same number of keys."
            )
        if len(self.param_dict) < 1:
            raise ValueError("param_dict should have at least 1 key,value pair")


class UserCatData(UserData):
    """Instance of UserData using minium input variables to map to ODAPCatData."""

    def __init__(
        self,
        ds: Union[str, xr.Dataset],
        proj_ds: Any,
        x_coord: str,
        y_coord: str,
        t_coord: str,
        var: List[str],
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        proj_feature: Any,
        id_feature: str,
        period: List[str],
    ) -> None:
        """__init__ Contains data preperation methods based on UserData.

        _extended_summary_

        Args:
            ds (Union[str, Path, xr.Dataset]): _description_
            proj_ds (Any): _description_
            x_coord (str): _description_
            y_coord (str): _description_
            t_coord (str): _description_
            var (List[str]): _description_
            f_feature (Union[str, Path, gpd.GeoDataFrame]): _description_
            proj_feature (Any): _description_
            id_feature (str): _description_
            period (List[str]): _description_

        Raises:
            TypeError: _description_
        """
        logger.info("Initializing UserCatData")
        logger.info("  - loading data")
        self.ds = _get_xr_dataset(ds=ds)
        self.f_feature = _get_geodataframe(f_feature=f_feature)
        self.proj_ds = proj_ds
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.t_coord = t_coord
        # self.period = pd.to_datetime(period)
        self.period = period
        if not isinstance(var, List):
            raise TypeError(f"Input var {var} should be a list of variables")
        self.var = var
        self.proj_feature = proj_feature
        self.id_feature = id_feature

        self.gdf_bounds = _get_shp_bounds_w_buffer(
            gdf=self.f_feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )
        logger.info("  - checking latitude bounds")
        is_intersect, is_degrees, is_0_360 = _check_for_intersection_nc(
            ds=self.ds,
            x_name=self.x_coord,
            y_name=self.y_coord,
            proj=self.proj_ds,
            gdf=self.f_feature,
        )

        if bool((not is_intersect) & is_degrees & (is_0_360)):  # rotate
            logger.info("  - rotating into -180 - 180")
            self.ds.coords[self.x_coord] = (
                self.ds.coords[self.x_coord] + 180
            ) % 360 - 180
            self.ds = self.ds.sortby(self.ds[self.x_coord])

        # calculate toptobottom (order of latitude coords)
        self.ttb = _get_top_to_bottom(self.ds, self.y_coord)
        logger.info("  - getting gridded data subset")
        self.weight_subset_dict = build_subset(
            bounds=self.gdf_bounds,
            xname=self.x_coord,
            yname=self.y_coord,
            tname=self.t_coord,
            toptobottom=self.ttb,
            date_min=self.period[0],
        )
        self.agg_subset_dict = build_subset(
            bounds=self.gdf_bounds,
            xname=self.x_coord,
            yname=self.y_coord,
            tname=self.t_coord,
            toptobottom=self.ttb,
            date_min=self.period[0],
            date_max=self.period[1],
        )

    @classmethod
    def __repr__(cls) -> str:
        """Print class name."""
        return f"Class is {cls.__name__}"

    def get_source_subset(self, key: str) -> xr.DataArray:
        """get_source_subset Get source subset by key.

        _extended_summary_

        Args:
            key (str): _description_

        Returns:
            xr.DataArray: _description_
        """
        return self.ds[key].sel(**self.agg_subset_dict)

    def get_feature_id(self) -> str:
        """Return id_feature."""
        return self.id_feature

    def get_vars(self) -> list[str]:
        """Return list of vars in data."""
        return self.var

    def prep_interp_data(self, key: str, poly_id: int) -> AggData:
        """Prep AggData from UserData.

        Args:
            key (str): Name of the xarray grided data variable
            poly_id (int): ID number of the geodataframe geometry to clip the
                gridded data to

        Returns:
            AggData: An instance of the AggData class
        """
        # Open grid and clip to geodataframe and time window
        data_ss: xr.DataArray = self.ds[key].sel(**self.agg_subset_dict)  # type: ignore
        cplist = self._get_user_catparams(key=key, da=data_ss)
        cglist = self._get_user_catgrids(key=key, da=data_ss)
        # Create param and grid dictionaries
        param_dict = dict(zip([key], cplist))  # noqa B905
        grid_dict = dict(zip([key], cglist))  # noqa B905

        # Select a feature and make sure it remains a geodataframe
        feature = self.f_feature[
            self.f_feature.loc[:, "geometry"]
            == self.f_feature.loc[:, "geometry"][poly_id]
        ]

        # Reproject the feature to grid crs and get a buffered bounding box
        crs = grid_dict.get(key)["proj"]
        x_cell_size = grid_dict.get(key)["resX"]
        y_cell_size = grid_dict.get(key)["resY"]
        bbox = box(*feature.to_crs(crs).total_bounds)
        bounds = np.asarray(
            bbox.buffer(2 * max(x_cell_size, y_cell_size)).bounds  # type: ignore
        )

        # Clip grid to time window and line geometry bbox buffer
        ss_dict = build_subset(
            bounds=bounds,
            xname=grid_dict[key]["X_name"],
            yname=grid_dict[key]["Y_name"],
            tname=param_dict[key]["T_name"],
            toptobottom=self.ttb,
            date_min=str(self.period[0]),
            date_max=str(self.period[1]),
        )

        ds_ss = data_ss.sel(**ss_dict)

        return AggData(
            variable=key,
            cat_param=CatParams(**param_dict.get(key)),  # type: ignore
            cat_grid=CatGrids(**grid_dict.get(key)),  # type: ignore
            da=ds_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_agg_data(self, key: str) -> AggData:
        """Prep AggData from UserData."""
        logger.info("Agg Data preparation - beginning")
        data_ss: xr.DataArray = self.ds[key].sel(**self.agg_subset_dict)  # type: ignore
        cplist = self._get_user_catparams(key=key, da=data_ss)
        cglist = self._get_user_catgrids(key=key, da=data_ss)
        logger.info("  - creating param and grid dicts")
        param_dict = dict(zip([key], cplist))  # noqa B905
        grid_dict = dict(zip([key], cglist))  # noqa B905

        feature = self.f_feature
        logger.info("  - returning AggData")
        return AggData(
            variable=key,
            cat_param=CatParams(**param_dict.get(key)),  # type: ignore
            cat_grid=CatGrids(**grid_dict.get(key)),  # type: ignore
            da=data_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def _get_user_catgrids(self, key: str, da: xr.DataArray) -> list[dict[str, Any]]:
        """Get CatGrids from UserData."""
        cg = CatGrids(
            X_name=self.x_coord,
            Y_name=self.y_coord,
            proj=self.proj_ds,
            resX=max(np.diff(da[self.x_coord].values)),
            resY=max(np.diff(da[self.y_coord].values)),
            toptobottom=_get_top_to_bottom(da, self.y_coord),
        )
        return [cg.dict()]

    def _get_ds_var_attrs(self, da: xr.DataArray, attr: str) -> Any:
        """Return var attributes.

        Args:
            da (xr.DataArray): _description_
            attr (str): _description_

        Returns:
            Any: _description_
        """
        try:
            return da.attrs.get(attr)
        except KeyError:
            return "None"

    def _get_user_catparams(self, key: str, da: xr.DataArray) -> list[dict[str, Any]]:
        """Get CatParams from UserData."""
        cp = CatParams(
            URL="",
            varname=key,
            long_name=str(self._get_ds_var_attrs(da, "long_name")),
            T_name=self.t_coord,
            units=str(self._get_ds_var_attrs(da, "units")),
        )
        return [cp.dict()]

    def prep_wght_data(self) -> WeightData:
        """Prepare and return WeightData for weight generation."""
        logger.info("Weight Data preparation - beginning")
        data_ss_wght = self.ds.sel(**self.weight_subset_dict)  # type: ignore
        logger.info("  - calculating grid-cell polygons")
        start = time.perf_counter()
        grid_poly = _get_cells_poly(
            xr_a=data_ss_wght,
            x=self.x_coord,
            y=self.y_coord,
            crs_in=self.proj_ds,
        )
        end = time.perf_counter()
        print(
            f"Generating grid-cell polygons finished in {round(end-start, 2)} second(s)"
        )
        logger.info(
            f"Generating grid-cell polygons finished in {round(end-start, 2)} second(s)"
        )
        return WeightData(
            feature=self.f_feature, id_feature=self.id_feature, grid_cells=grid_poly
        )


class UserTiffData(UserData):
    """Instance of UserData for zonal stats processing of geotiffs."""

    def __init__(
        self,
        var: str,
        ds: Union[str, xr.DataArray, xr.Dataset],
        proj_ds: Any,
        x_coord: str,
        y_coord: str,
        bname: str,
        band: int,
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        id_feature: str,
        proj_feature: Any,
    ) -> None:
        """__init__ Initialize UserTiffData.

        UserTiffData is a structure that aids calculating zonal stats.

        Args:
            var (str): _description_
            ds (Union[str, xr.Dataset]): _description_
            proj_ds (Any): _description_
            x_coord (str): _description_
            y_coord (str): _description_
            bname (str): _description_
            band (int): _description_
            f_feature (Union[str, Path, gpd.GeoDataFrame]): _description_
            id_feature (str): _description_
            proj_feature (Any): _description_
        """
        self.varname = var
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.bname = bname
        self.band = band
        self.ds = _get_rxr_dataset(ds)
        self.toptobottom = _get_top_to_bottom(self.ds, self.y_coord)
        self.proj_ds = proj_ds
        self.f_feature = _get_geodataframe(f_feature)
        self.id_feature = id_feature
        self.proj_feature = proj_feature
        self.f_feature = self.f_feature.sort_values(self.id_feature).dissolve(
            by=self.id_feature, as_index=False
        )
        self.f_feature.reset_index()

        self._check_xname()
        self._check_yname()
        self._check_band()
        self._check_crs()
        self.toptobottom = _get_top_to_bottom(data=self.ds, y_coord=self.y_coord)

    def get_source_subset(self, key: str) -> xr.DataArray:
        """get_source_subset Get subset of source data.

        _extended_summary_

        Args:
            key (str): _description_

        Returns:
            xr.DataArray: _description_
        """
        bb_feature = _get_shp_bounds_w_buffer(
            gdf=self.f_feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )

        subset_dict = build_subset_tiff(
            bounds=bb_feature,
            xname=self.x_coord,
            yname=self.y_coord,
            toptobottom=self.toptobottom,
            bname=self.bname,
            band=self.band,
        )

        return self.ds.sel(**subset_dict)  # type: ignore

    def get_vars(self) -> list[str]:
        """Return list of varnames."""
        return [self.varname]

    def get_feature_id(self) -> str:
        """Get Feature id."""
        return self.id_feature

    def prep_wght_data(self) -> WeightData:
        """Prepare data for weight generation."""
        pass

    def prep_agg_data(self, key: str) -> AggData:
        """Prepare data for aggregation or zonal stats."""
        bb_feature = _get_shp_bounds_w_buffer(
            gdf=self.f_feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )

        subset_dict = build_subset_tiff(
            bounds=bb_feature,
            xname=self.x_coord,
            yname=self.y_coord,
            toptobottom=self.toptobottom,
            bname=self.bname,
            band=self.band,
        )

        data_ss: xr.DataArray = self.ds.sel(**subset_dict)  # type: ignore
        # tstrt = time.perf_counter()
        # data_ss = data_ss.rio.interpolate_na(method='nearest')
        # tend = time.perf_counter()
        # print(f"fill missing data using nearest method in {tend - tstrt:0.4f} seconds")
        cplist = self._get_user_catparams(da=data_ss)
        cglist = self._get_user_catgrids(da=data_ss)
        param_dict = dict(zip([key], [cplist]))  # noqa B905
        grid_dict = dict(zip([key], [cglist]))  # noqa B905

        return AggData(
            variable=key,
            cat_param=CatParams(**param_dict.get(key)),  # type: ignore
            cat_grid=CatGrids(**grid_dict.get(key)),  # type: ignore
            da=data_ss,
            feature=self.f_feature.copy(),
            id_feature=self.id_feature,
            period=["None", "None"],
        )

    def _check_xname(self: "UserTiffData") -> None:
        """Validate xname."""
        if self.x_coord not in self.ds.coords:
            raise ValueError(f"xname:{self.x_coord} not in {self.ds.coords}")

    def _check_yname(self: "UserTiffData") -> None:
        """Validate yname."""
        if self.y_coord not in self.ds.coords:
            raise ValueError(f"yname:{self.y_coord} not in {self.ds.coords}")

    def _check_band(self: "UserTiffData") -> None:
        """Validate band name."""
        if self.bname not in self.ds.coords:
            raise ValueError(
                f"band:{self.bname} not in {self.ds.coords} or {self.ds.data_vars}"
            )

    def _check_crs(self: "UserTiffData") -> None:
        """Validate crs."""
        crs = CRS.from_user_input(self.proj_ds)
        if not isinstance(crs, CRS):
            raise ValueError(f"ds_proj:{self.proj_ds} not in valid")
        crs2 = CRS.from_user_input(self.proj_feature)
        if not isinstance(crs2, CRS):
            raise ValueError(f"ds_proj:{self.proj_feature} not in valid")

    def _get_user_catgrids(self: "UserTiffData", da: xr.DataArray) -> dict[str, Any]:
        """Get CatGrids from UserData."""
        cg = CatGrids(
            X_name=self.x_coord,
            Y_name=self.y_coord,
            proj=self.proj_ds,
            resX=max(np.diff(da[self.x_coord].values)),
            resY=max(np.diff(da[self.y_coord].values)),
            toptobottom=self.toptobottom,
        )
        return cg.dict()

    def _get_user_catparams(self: "UserTiffData", da: xr.DataArray) -> dict[str, Any]:
        """Get CatParams from UserData."""
        cp = CatParams(
            URL="",
            varname=self.varname,
            long_name=self._get_ds_var_attrs(da, "long_name"),
            T_name="",
            units=self._get_ds_var_attrs(da, "units"),
        )
        return cp.dict()

    def _get_ds_var_attrs(self: "UserTiffData", da: xr.DataArray, attr: str) -> str:
        """Return var attributes.

        Args:
            da (xr.DataArray): _description_
            attr (str): _description_

        Returns:
            str: _description_
        """
        try:
            return str(da.attrs.get(attr))
        except KeyError:
            return "na"
