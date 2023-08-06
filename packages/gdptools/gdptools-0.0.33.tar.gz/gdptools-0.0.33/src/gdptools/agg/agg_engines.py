"""Aggregation engines."""
import time
from abc import ABC
from abc import abstractmethod
from collections import namedtuple
from collections.abc import Generator
from typing import Any
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

import dask
import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import xarray as xr
from joblib import delayed
from joblib import Parallel
from joblib import parallel_backend

from gdptools.agg.stats_methods import Count
from gdptools.agg.stats_methods import MACount
from gdptools.agg.stats_methods import MAMax
from gdptools.agg.stats_methods import MAMin
from gdptools.agg.stats_methods import MAWeightedMean
from gdptools.agg.stats_methods import MAWeightedMedian
from gdptools.agg.stats_methods import MAWeightedStd
from gdptools.agg.stats_methods import Max
from gdptools.agg.stats_methods import Min
from gdptools.agg.stats_methods import StatsMethod
from gdptools.agg.stats_methods import WeightedMean
from gdptools.agg.stats_methods import WeightedMedian
from gdptools.agg.stats_methods import WeightedStd
from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import ODAPCatData
from gdptools.data.user_data import UserCatData
from gdptools.data.user_data import UserData
from gdptools.data.user_data import UserTiffData
from gdptools.utils import _cal_point_stats
from gdptools.utils import _dataframe_to_geodataframe
from gdptools.utils import _get_default_val
from gdptools.utils import _get_interp_array
from gdptools.utils import _get_line_vertices
from gdptools.utils import _get_weight_df
from gdptools.utils import _interpolate_sample_points

# from gdptools.utils import _interp_array_to_gdf


AggChunk = namedtuple("AggChunk", ["ma", "wghts", "def_val", "index"])

STAT_TYPES = Union[
    Type[MAWeightedMean],
    Type[WeightedMean],
    Type[MAWeightedStd],
    Type[WeightedStd],
    Type[MAWeightedMedian],
    Type[WeightedMedian],
    Type[MACount],
    Type[Count],
    Type[MAMin],
    Type[Min],
    Type[MAMax],
    Type[Max],
]


class AggEngine(ABC):
    """Abstract aggregation class."""

    def calc_agg_from_dictmeta(
        self,
        user_data: UserData,
        weights: Union[str, pd.DataFrame],
        stat: STAT_TYPES,
        jobs: int = -1,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Abstract Base Class for calculating aggregations from dictionary metadata.

        _extended_summary_

        Args:
            user_data (UserData): _description_
            weights (Union[str, gpd.GeoDataFrame]): _description_
            stat (STAT_TYPES): _description_
            jobs (int): _description_. Defaults to -1.

        Returns:
            Tuple[gpd.GeoDataFrame, List[NDArray[np.double]]]: _description_
        """
        self.usr_data = user_data
        self.id_feature = user_data.get_feature_id()
        self.vars = user_data.get_vars()
        self.stat = stat
        self.period = None
        self.wghts = _get_weight_df(weights, self.id_feature)
        self._jobs = jobs

        return self.agg_w_weights()

    @abstractmethod
    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Abstract method for calculating weights."""
        pass


class SerialAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        # tname = list(data.cat_param.values())[0]["T_name"]
        tname = data.cat_param.T_name
        tstrt = str(data.da.coords[tname].values[0])
        tend = str(data.da.coords[tname].values[-1])
        return [tstrt, tend]

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend-tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend -tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "SerialAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate aggregation.

        Args:
            key (str): _description_
            data (AggData): _description_

        Returns:
            Tuple[gpd.GeoDataFrame, NDArray[np.double]]: _description_
        """
        cp = data.cat_param
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(data.id_feature).dissolve(by=data.id_feature)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        # print(da)
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(
            n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval
        )

        # mdata = np.ma.masked_array(da.values, np.isnan(da.values))  # type: ignore
        mdata = da.values  # type: ignore

        for i in np.arange(len(geo_index)):
            try:
                weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
            except KeyError:
                continue
            tw = weight_id_rows.wght.values
            i_ind = np.array(weight_id_rows.i.values).astype(int)
            j_ind = np.array(weight_id_rows.j.values).astype(int)

            val_interp[:, i] = self.stat(
                array=mdata[:, i_ind, j_ind], weights=tw, def_val=dfval
            ).get_stat()

        return gdf, val_interp


class ParallelAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        # tname = list(data.cat_param.values())[0]["T_name"]
        tname = data.cat_param.T_name
        tstrt = str(data.da.coords[tname].values[0])
        tend = str(data.da.coords[tname].values[-1])
        return [tstrt, tend]

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend-tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend -tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "ParallelAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate aggregation.

        Args:
            key (str): _description_
            data (AggData): _description_

        Returns:
            Tuple[gpd.GeoDataFrame, NDArray[np.double]]: _description_
        """
        cp = data.cat_param
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(data.id_feature).dissolve(by=data.id_feature)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        # geo_index_chunk = np.array_split(geo_index, self._jobs)
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        # print(da)
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(
            n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval
        )

        # mdata = np.ma.masked_array(da.values, np.isnan(da.values))  # type: ignore
        mdata = da.values  # type: ignore

        chunks = get_weight_chunks(
            unique_geom_ids=unique_geom_ids, mdata=mdata, dfval=dfval
        )

        worker_out = get_stats_parallel(
            n_jobs=self._jobs,
            stat=self.stat,
            bag=bag_generator(jobs=self._jobs, chunks=chunks),
        )

        for index, val in worker_out:
            val_interp[:, index] = val

        return gdf, val_interp


def _stats(
    bag: List[AggChunk], method: StatsMethod
) -> Tuple[npt.NDArray[np.int_], npt.NDArray[Union[np.int_, np.double]]]:
    vals = np.zeros((bag[0].ma.shape[0], len(bag)), dtype=bag[0].ma.dtype)
    index = np.zeros(len(bag), dtype=np.int_)
    for idx, b in enumerate(bag):
        index[idx] = b.index
        vals[:, idx] = method(
            array=b.ma, weights=b.wghts, def_val=b.def_val
        ).get_stat()  # type: ignore
    return (index, vals)


def get_stats_parallel(
    n_jobs: int,
    stat: STAT_TYPES,
    bag: Generator[List[AggChunk], None, None],
) -> Any:
    """Get stats values."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(
            delayed(_stats)(chunk, method=stat) for chunk in bag
        )
    return worker_out


def get_weight_chunks(
    unique_geom_ids: gpd.GeoDataFrame.groupby,
    # mdata: np.ma.MaskedArray,  # type: ignore
    mdata: npt.NDArray,  # type: ignore
    dfval: Union[np.int_, np.double],
) -> List[AggChunk]:
    """Chunk data for parallel aggregation."""
    keys = list(unique_geom_ids.groups.keys())
    chunks = []
    for idx, key in enumerate(keys):
        weight_id_rows = unique_geom_ids.get_group(key)
        chunks.append(
            AggChunk(
                mdata[
                    :,
                    np.array(weight_id_rows.i.values).astype(int),
                    np.array(weight_id_rows.j.values).astype(int),
                ],
                weight_id_rows.wght.values,
                dfval,
                idx,
            )
        )
    return chunks


def bag_generator(
    jobs: int, chunks: List[AggChunk]
) -> Generator[List[AggChunk], None, None]:
    """Function to generate chunks."""
    chunk_size = len(chunks) // jobs + 1
    for i in range(0, len(chunks), chunk_size):
        yield chunks[i : i + chunk_size]


class DaskAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        # tname = list(data.cat_param.values())[0]["T_name"]
        tname = data.cat_param.T_name
        tstrt = str(data.da.coords[tname].values[0])
        tend = str(data.da.coords[tname].values[-1])
        return [tstrt, tend]

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend-tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend -tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "DaskAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate aggregation.

        Args:
            key (str): _description_
            data (AggData): _description_

        Returns:
            Tuple[gpd.GeoDataFrame, NDArray[np.double]]: _description_
        """
        cp = data.cat_param
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(data.id_feature).dissolve(by=data.id_feature)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        # geo_index_chunk = np.array_split(geo_index, self._jobs)
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        # print(da)
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(
            n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval
        )

        # mdata = np.ma.masked_array(da.values, np.isnan(da.values))  # type: ignore
        mdata = da.values  # type: ignore

        chunks = get_weight_chunks(
            unique_geom_ids=unique_geom_ids, mdata=mdata, dfval=dfval
        )

        worker_out = get_stats_dask(
            n_jobs=self._jobs,
            stat=self.stat,
            bag=bag_generator(jobs=self._jobs, chunks=chunks),
        )

        for index, val in worker_out[0]:
            val_interp[:, index] = val

        return gdf, val_interp


def get_stats_dask(
    n_jobs: int,
    stat: STAT_TYPES,
    bag: Generator[List[AggChunk], None, None],
) -> List[Any]:
    """Get stats values."""
    worker_out = [
        dask.delayed(_stats)(chunk, method=stat) for chunk in bag  # type: ignore
    ]
    return dask.compute(worker_out)  # type: ignore


class InterpEngine(ABC):
    """Abstract class for interpolation."""

    def run(
        self,
        user_data: Union[ODAPCatData, UserCatData, UserTiffData],
        pt_spacing: Union[float, int, None],
        stat: str,
        return_sample_geom: bool,
        calc_crs: Any,
    ) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Run InterpEngine Class.

        _extended_summary_

        Args:
            user_data (Union[ODAPCatData, UserCatData, UserTiffData]): Data Class for
                input data
            pt_spacing (Union[float, int, None]): Numerical value in meters for the
                spacing of the interpolated sample points (default is 50)
            stat (str):  A string indicating which statistics to calculate during
                the query. Options: 'all', 'mean', 'median', 'std', 'max', 'min'
                (default is 'all')
            return_sample_geom (bool): Indicates whether to return a geodataframe of
                the sample points (default is False)
            calc_crs (Any): OGC WKT string, Proj.4 string or int EPSG code.
                Determines which projection is used for the area weighted calculations

        Returns:
            Union[ Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame ]: If
                return_sample_geom is True, then it returns both a DataFrame of the
                statistics and a GeoDataFrame of the point geometries, else it returns
                the stats DataFrame
        """
        self._user_data = user_data
        self._pt_spacing = pt_spacing
        self._stat = stat
        self._return_sample_geom = return_sample_geom
        self._calc_crs = calc_crs

        return self.interp()

    @abstractmethod
    def interp(self) -> None:
        """Abstract method for interpolating point values."""
        pass


class SerialInterp(InterpEngine):
    """Serial Interpolation Class."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        # tname = list(data.cat_param.values())[0]["T_name"]
        tname = data.cat_param.T_name
        tstrt = str(data.da.coords[tname].values[0])
        tend = str(data.da.coords[tname].values[-1])
        return [tstrt, tend]

    def interp(  # noqa: C901
        self,
    ) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Abstract method for interpolating point values.

        Returns:
            Union[ Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame ]: If
                return_sample_geom is True, then it returns both a DataFrame of the
                statistics and a GeoDataFrame of the point geometries, else it returns
                the stats DataFrame

        """
        # Get each grid variable
        wvars = self._user_data.get_vars()

        stats = []
        points = []

        # Loop thru each grid variable
        for index, key in enumerate(wvars):
            # loop thru each line geometry
            for i in range(len(self._user_data.f_feature)):
                # Prep the input data
                self.interp_data: AggData = self._user_data.prep_interp_data(
                    key=key, poly_id=i
                )

                # Calculate statistics
                if self._return_sample_geom:
                    statistics, pts = self.grid_to_line_intersection(key=key)
                    if i == 0:
                        key_stats: pd.DataFrame = statistics
                        key_points: gpd.GeoDataFrame = pts
                    else:
                        key_points = pd.concat([key_points, pts])
                else:
                    statistics = self.grid_to_line_intersection(key=key)
                    if i == 0:
                        key_stats: pd.DataFrame = statistics
                if i > 0:
                    key_stats = pd.concat([key_stats, statistics])

            if self._return_sample_geom:
                if index == 0:
                    stats = key_stats
                    points = key_points
                else:
                    stats = pd.concat([stats, key_stats])
                    points = pd.concat([points, key_points])
            elif index == 0:
                points = key_points
            else:
                points = pd.concat([points, key_points])

        if self._return_sample_geom:
            return stats, points

        # return just stats
        else:
            return stats

    def grid_to_line_intersection(
        self: "InterpEngine", key: Union[str, None] = None
    ) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Function for extracting grid values and stats for polyline geometry.

        _extended_summary_

        Args:
            key (Union[str, None], optional): Name of the variable in the xarray
                dataset. Defaults to None.

        Returns:
            Union[ Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame ]: If
                return_sample_geom is True, then it returns both a DataFrame of the
                statistics and a GeoDataFrame of the point geometries, else it returns
                the stats DataFrame
        """
        data_array = self.interp_data.da
        varname = self.interp_data.cat_param.varname
        spacing = self._pt_spacing

        # Get crs and coord names for gridded data
        try:
            grid_proj = self._user_data.grid_dict[key]["proj"]
            x_coord = self._user_data.grid_dict[key]["X_name"]
            y_coord = self._user_data.grid_dict[key]["Y_name"]

        except Exception:
            grid_proj = self._user_data.proj_ds
            x_coord = self._user_data.x_coord
            y_coord = self._user_data.y_coord

        # Reproject line to the grid's crs
        line = self.interp_data.feature.copy()
        geom = line.geometry.to_crs(grid_proj)

        # Either find line vertices
        if spacing == 0:
            x, y, dist = _get_line_vertices(geom, grid_proj)

        # Or interpolate sample points
        else:
            x, y, dist = _interpolate_sample_points(
                geom=geom, spacing=spacing, calc_crs=self._calc_crs, crs=grid_proj
            )

        poly_id_array = np.full(
            len(dist), self.interp_data.feature[self._user_data.id_feature].values[0]
        )
        # Set coordinate system
        data_array = (
            data_array.rio.write_crs(grid_proj)  # self.interp_data.da
            .rio.set_spatial_dims(
                x_dim=x_coord,
                y_dim=y_coord,
            )
            .rio.reproject(grid_proj)
        )

        interp_dataarray: xr.DataArray = data_array.to_dataset().interp(
            x=("pt", x), y=("pt", y)
        )
        interp_dataarray = xr.merge(
            [interp_dataarray, xr.DataArray(dist, dims=["pt"], name="dist")]
        )
        interp_dataarray = xr.merge(
            [
                interp_dataarray,
                xr.DataArray(poly_id_array, dims=["pt"], name="feature_id"),
            ]
        )

        interp_geo_df = _dataframe_to_geodataframe(
            interp_dataarray.to_dataframe(), crs=grid_proj
        )
        interp_geo_df.rename(columns={varname: "values"}, inplace=True)
        id_feature_array = np.full(len(interp_geo_df), varname)
        interp_geo_df["varname"] = id_feature_array

        # prefer date, feature id and varname, up front of dataframe.
        t_coord = self.interp_data.cat_param.T_name
        out_vals: dict[str, float] = {"date": interp_dataarray[t_coord].values}
        out_vals[self._user_data.id_feature] = np.full(
            out_vals[list(out_vals.keys())[0]].shape[0],
            self.interp_data.feature[self._user_data.id_feature].values[0],
        )
        out_vals["varname"] = np.full(
            out_vals[list(out_vals.keys())[0]].shape[0],
            self.interp_data.cat_param.varname,
        )
        out_vals |= _cal_point_stats(
            data_array=interp_dataarray[self.interp_data.cat_param.varname],
            stat=self._stat,
        )
        stats_df = pd.DataFrame().from_dict(out_vals)

        if self._return_sample_geom:
            return stats_df, interp_geo_df

        # Return just the stats
        else:
            return stats_df


# Todo: create parallel method
# class ParallelInterp
