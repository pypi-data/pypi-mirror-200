"""Testing ancillary functions."""
from typing import Any

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import pytest
import xarray as xr
from pyproj import CRS
from pyproj.exceptions import CRSError

from gdptools.data.odap_cat_data import CatGrids
from gdptools.data.odap_cat_data import CatParams
from gdptools.utils import _buffer_line
from gdptools.utils import _check_for_intersection
from gdptools.utils import _get_cells_poly
from gdptools.utils import _get_crs
from gdptools.utils import _get_data_via_catalog
from gdptools.utils import _get_line_vertices
from gdptools.utils import _get_shp_file
from gdptools.utils import _interpolate_sample_points


@pytest.mark.parametrize(
    "crs",
    [
        "epsg:4326",
        4326,
        "+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs",
    ],
)
def test__get_crs(crs: Any) -> None:
    """Test the get_crs function."""
    crs = _get_crs(crs)
    assert isinstance(crs, CRS)


@pytest.mark.parametrize(
    "crs",
    [
        "espg:4326",
        43,
        "+a=6378137 +f=0.00335281066474748 +pm=0 +no_defs",
    ],
)
def test__get_bad_crs(crs: Any) -> None:
    """Test the get_crs function."""
    with pytest.raises(CRSError):
        crs = _get_crs(crs)


@pytest.fixture
def catparam() -> CatParams:
    """Return parameter json."""
    cat_params = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
    params = pd.read_json(cat_params)
    _id = "gridmet"  # noqa
    _varname = "daily_maximum_temperature"  # noqa
    tc = params.query("id == @_id & varname == @_varname")
    return CatParams(**tc.to_dict("records")[0])


@pytest.fixture
def catgrid() -> CatGrids:
    """Return grid json."""
    cat_grid = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
    grids = pd.read_json(cat_grid)
    _gridid = 176  # noqa
    tc = grids.query("grid_id == @_gridid")
    return CatGrids(**tc.to_dict("records")[0])


@pytest.fixture
def gdf() -> gpd.GeoDataFrame:
    """Create xarray dataset."""
    return gpd.read_file("./tests/data/hru_1210_epsg5070.shp")


@pytest.fixture
def is_degrees(gdf, catparam, catgrid) -> bool:  # type: ignore
    """Check if coords are in degrees."""
    is_degrees: bool
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        cat_params=catparam, cat_grid=catgrid, gdf=gdf
    )
    return is_degrees


@pytest.fixture
def bounds(gdf, catgrid, is_degrees) -> npt.NDArray[np.double]:  # type: ignore
    """Get bounds."""
    bounds: npt.NDArray[np.double]
    gdf, bounds = _get_shp_file(gdf, catgrid, is_degrees)
    return bounds


@pytest.fixture
def xarray(catparam, catgrid, bounds) -> xr.DataArray:  # type: ignore
    """Create xarray dataset."""
    data: xr.DataArray = _get_data_via_catalog(catparam, catgrid, bounds, "2020-01-01")
    return data


def test__get_cells_poly(catparam, catgrid, bounds) -> None:  # type: ignore
    """Test _get_cells_poly."""
    ds: xr.DataArray = _get_data_via_catalog(catparam, catgrid, bounds, "2020-01-01")
    print(ds)
    assert isinstance(ds, xr.DataArray)
    gdf = _get_cells_poly(xr_a=ds, x="lon", y="lat", crs_in=4326)
    assert isinstance(gdf, gpd.GeoDataFrame)


def test_interpolate_sample_points() -> None:
    """Test the interpolate function."""
    lines = gpd.read_file("./tests/data/test_lines.json")
    line = lines.loc[[1]].geometry.copy()
    test_geom = line.geometry.to_crs(5070)
    x, y, dist = _interpolate_sample_points(test_geom, 500, 6931, 5070)
    assert x[0] == pytest.approx(244302.78752828587, 0.001)
    assert y[2] == pytest.approx(2090852.4680706703, 0.001)
    assert dist[1] == 500.0


def test_buffer_line() -> None:
    """Test the buffer line function."""
    lines = gpd.read_file("./tests/data/test_lines.json")
    buffered_lines = _buffer_line(lines.geometry, 500, lines.crs, 5070)
    assert buffered_lines[0].area == pytest.approx(0.0014776797476285766, 0.0001)
    assert buffered_lines[0].length == pytest.approx(0.269159, 0.0001)
    assert buffered_lines[1].area == pytest.approx(0.00024249232348514231, 0.0001)
    assert buffered_lines[1].length == pytest.approx(0.066633, 0.0001)


def test_get_line_vertices() -> None:
    """Test the get line vertices function."""
    lines = gpd.read_file("./tests/data/test_lines.json")
    x, y, dist = _get_line_vertices(lines.loc[[1]], 4269)
    assert len(x) == 133
    assert y[10] == pytest.approx(41.78631166847265, 0.0001)
    assert dist[20] == pytest.approx(174.60046645386024, 0.0001)


# def test_cal_point_stats() -> None:
#     """Test the calculate point stats function."""
#     pts_gdf = gpd.read_file("./tests/data/test_points.json")
#     pts_stats = _cal_point_stats(pts_gdf, "all")
#     assert len(pts_stats) == 5
#     pts_stats = _cal_point_stats(pts_gdf, "mean")
#     assert pts_stats["mean"] == pytest.approx(-2.685338, 0.0001)
#     pts_stats = _cal_point_stats(pts_gdf, "median")
#     assert pts_stats["median"] == pytest.approx(-2.6819770336151123, 0.0001)
#     pts_stats = _cal_point_stats(pts_gdf, "std")
#     assert pts_stats["std"] == pytest.approx(0.02053731493651867, 0.0001)
#     pts_stats = _cal_point_stats(pts_gdf, "min")
#     assert pts_stats["min"] == pytest.approx(-2.709066152572632, 0.0001)
#     pts_stats = _cal_point_stats(pts_gdf, "max")
#     assert pts_stats["max"] == pytest.approx(-2.6563093662261963, 0.0001)
