"""Test scripts for stats methods."""
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
import xarray as xr

from gdptools import AggGen
from gdptools import UserCatData
from gdptools import WeightGen

gm_vars = ["aet"]


@pytest.fixture()
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    return gpd.read_file("./tests/data/capecod_huc12.shp").dissolve(
        by=["huc12", "tohuc", "name", "hutype", "humod", "noncontrib", "states"],
        aggfunc="sum",
        as_index=False,
        dropna=False,
    )


@pytest.fixture()
def get_xarray() -> xr.Dataset:
    """Create xarray dataset."""
    return xr.open_dataset("./tests/data/rasters/climate/terraclim_aet_capecod.nc")


@pytest.fixture()
def get_out_path(tmp_path: Path) -> Path:
    """Get temp file path."""
    return tmp_path


data_crs = 4326
x_coord = "lon"
y_coord = "lat"
t_coord = "time"
sdate = "1980-01-01"
edate = "1980-12-01"
var = ["aet"]
shp_crs = 4326
shp_poly_idx = "huc12"
wght_gen_crs = 6931
stats_agg_file_prefix = "extra_stats_test"

stats_test_dict = {
    "mean": np.array(
        [
            101.16062306991417,
            101.89667307594982,
            101.2733032241714,
            np.nan,
            100.9036416305431,
            101.91529811292946,
            101.03068109986368,
            98.46565574058324,
            93.07121115331904,
            92.45570806658066,
            90.48008765075167,
            np.nan,
            np.nan,
            np.nan,
            101.40248301493793,
            101.8873294510659,
            99.50107851056474,
            100.4309934822545,
            100.62063622592113,
            np.nan,
            np.nan,
            101.69107103850423,
            102.24948948225652,
            100.47079170743466,
            98.34781450367866,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            101.68587686693002,
            101.56572558541157,
            102.0937536384102,
            101.76418440396608,
            102.42196633387192,
            101.6329372224863,
            98.96916760272836,
        ]
    ),
    "masked_mean": np.array(
        [
            101.16062306991417,
            101.8966730759498,
            101.2733032241714,
            100.05816974966501,
            100.9036416305431,
            101.91529811292946,
            101.03068109986368,
            98.46565574058326,
            93.07121115331904,
            92.45570806658064,
            90.48008765075167,
            78.49760907203974,
            89.34413144809446,
            96.99061669351724,
            101.40248301493793,
            101.88732945106588,
            99.50107851056474,
            100.4309934822545,
            100.62063622592113,
            101.78268552575857,
            102.62499140614398,
            101.69107103850423,
            102.24948948225654,
            100.47079170743463,
            98.34781450367868,
            94.55486649072155,
            94.7903818181858,
            95.65744527770667,
            82.02395986050959,
            101.68587686693002,
            101.56572558541158,
            102.0937536384102,
            101.76418440396608,
            102.4219663338719,
            101.6329372224863,
            98.96916760272835,
        ]
    ),
    "std": np.array(
        [
            1.0003892091786877,
            0.7911563045720997,
            0.4080304233840606,
            np.nan,
            1.0277142628879288,
            0.2986934885356372,
            0.785698687017503,
            1.6931545704992268,
            0.33980162501226735,
            0.12425810081148257,
            5.242918161308443,
            np.nan,
            np.nan,
            np.nan,
            0.3387121300010567,
            0.36494767602363687,
            0.3573982816668527,
            0.7416486484984715,
            0.40021744002823045,
            np.nan,
            np.nan,
            1.3413452046562988,
            0.31630355993647824,
            0.9006479322725042,
            0.7652429313689281,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            0.4111362583884137,
            0.35439110939858265,
            0.35941018152546117,
            0.23746710411094515,
            0.30436852468370656,
            0.644496557408004,
            0.9845920100477381,
        ]
    ),
    "masked_std": np.array(
        [
            1.0003892091786877,
            0.7911563045720997,
            0.40803042338406065,
            0.0,
            1.0277142628879288,
            0.2986934885356372,
            0.785698687017503,
            1.6931545704992266,
            0.33980162501226735,
            0.12425810081148257,
            5.242918161308443,
            0.0,
            0.0,
            0.0,
            0.3387121300010567,
            0.3649476760236368,
            0.3573982816668527,
            0.7416486484984716,
            0.40021744002823045,
            0.0,
            0.0,
            1.3413452046562986,
            0.31630355993647824,
            0.9006479322725042,
            0.7652429313689281,
            0.0,
            0.0,
            0.0,
            0.0,
            0.4111362583884137,
            0.35439110939858265,
            0.3594101815254612,
            0.23746710411094518,
            0.3043685246837065,
            0.644496557408004,
            0.9845920100477382,
        ]
    ),
    "median": np.array(
        [
            100.82842196786066,
            101.23837483583792,
            101.20000457763672,
            np.nan,
            101.0,
            101.91479809636478,
            101.09722857030859,
            98.86751802787622,
            93.06084296788131,
            92.49999999999999,
            92.54549538306044,
            np.nan,
            np.nan,
            np.nan,
            101.40000152587892,
            101.95304013047449,
            99.50000000000001,
            100.23945256161842,
            100.38619739913449,
            np.nan,
            np.nan,
            101.51268995728205,
            102.109293676929,
            100.45373990713483,
            98.21821701589663,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            101.5,
            101.5999984741211,
            101.92392929593039,
            101.70000457763672,
            102.5,
            101.74013077612062,
            99.18139949193211,
        ]
    ),
    "masked_median": np.array(
        [
            100.82842196786066,
            101.23837483583792,
            101.20000457763672,
            99.99452043575974,
            101.0,
            101.91479809636478,
            101.09722857030859,
            98.86751802787622,
            93.06084296788131,
            92.49999999999999,
            92.54549538306044,
            76.80000305175783,
            92.62609799393533,
            97.20000457763673,
            101.40000152587892,
            101.95304013047449,
            99.50000000000001,
            100.23945256161842,
            100.38619739913449,
            101.7000045776367,
            102.55093792104813,
            101.51268995728205,
            102.109293676929,
            100.45373990713483,
            98.21821701589663,
            94.37313426431211,
            94.81362099399115,
            95.70000457763672,
            84.94948170709594,
            101.5,
            101.5999984741211,
            101.92392929593039,
            101.70000457763672,
            102.5,
            101.74013077612062,
            99.18139949193211,
        ]
    ),
    "count": np.array(
        [
            18.0,
            11.0,
            19.0,
            16.0,
            17.0,
            13.0,
            14.0,
            16.0,
            6.0,
            8.0,
            10.0,
            10.0,
            32.0,
            58.0,
            14.0,
            21.0,
            11.0,
            19.0,
            7.0,
            18.0,
            20.0,
            20.0,
            12.0,
            23.0,
            8.0,
            16.0,
            17.0,
            15.0,
            22.0,
            17.0,
            19.0,
            18.0,
            9.0,
            15.0,
            12.0,
            19.0,
        ]
    ),
    "masked_count": np.array(
        [
            18.0,
            11.0,
            19.0,
            15.0,
            17.0,
            13.0,
            14.0,
            16.0,
            6.0,
            8.0,
            10.0,
            9.0,
            31.0,
            56.0,
            14.0,
            21.0,
            11.0,
            19.0,
            7.0,
            16.0,
            19.0,
            20.0,
            12.0,
            23.0,
            8.0,
            14.0,
            16.0,
            13.0,
            18.0,
            17.0,
            19.0,
            18.0,
            9.0,
            15.0,
            12.0,
            19.0,
        ]
    ),
    "min": np.array(
        [
            98.5999984741211,
            101.0,
            99.5,
            np.nan,
            93.20000457763672,
            101.0,
            98.80000305175781,
            90.5,
            92.30000305175781,
            92.30000305175781,
            76.70000457763672,
            np.nan,
            np.nan,
            np.nan,
            100.4000015258789,
            100.5999984741211,
            98.70000457763672,
            98.5,
            100.20000457763672,
            np.nan,
            np.nan,
            98.9000015258789,
            101.4000015258789,
            98.4000015258789,
            94.9000015258789,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            101.20000457763672,
            101.20000457763672,
            101.4000015258789,
            101.30000305175781,
            101.80000305175781,
            100.5,
            94.9000015258789,
        ]
    ),
    "masked_min": np.array(
        [
            98.5999984741211,
            101.0,
            99.5,
            98.5999984741211,
            93.20000457763672,
            101.0,
            98.80000305175781,
            90.5,
            92.30000305175781,
            92.30000305175781,
            76.70000457763672,
            76.70000457763672,
            75.80000305175781,
            94.0999984741211,
            100.4000015258789,
            100.5999984741211,
            98.70000457763672,
            98.5,
            100.20000457763672,
            100.20000457763672,
            99.70000457763672,
            98.9000015258789,
            101.4000015258789,
            98.4000015258789,
            94.9000015258789,
            92.80000305175781,
            93.70000457763672,
            92.70000457763672,
            66.80000305175781,
            101.20000457763672,
            101.20000457763672,
            101.4000015258789,
            101.30000305175781,
            101.80000305175781,
            100.5,
            94.9000015258789,
        ]
    ),
    "max": np.array(
        [
            103.0999984741211,
            103.0999984741211,
            101.80000305175781,
            np.nan,
            102.0999984741211,
            102.5,
            102.5,
            100.0999984741211,
            93.5999984741211,
            93.5999984741211,
            92.9000015258789,
            np.nan,
            np.nan,
            np.nan,
            102.0999984741211,
            102.5,
            100.30000305175781,
            101.9000015258789,
            101.4000015258789,
            np.nan,
            np.nan,
            103.9000015258789,
            103.0,
            102.5,
            99.5999984741211,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            103.0999984741211,
            102.5,
            102.9000015258789,
            102.20000457763672,
            102.9000015258789,
            102.9000015258789,
            101.0,
        ]
    ),
    "masked_max": np.array(
        [
            103.0999984741211,
            103.0999984741211,
            101.80000305175781,
            101.30000305175781,
            102.0999984741211,
            102.5,
            102.5,
            100.0999984741211,
            93.5999984741211,
            93.5999984741211,
            92.9000015258789,
            92.20000457763672,
            94.9000015258789,
            99.5,
            102.0999984741211,
            102.5,
            100.30000305175781,
            101.9000015258789,
            101.4000015258789,
            103.5,
            103.9000015258789,
            103.9000015258789,
            103.0,
            102.5,
            99.5999984741211,
            96.5,
            96.70000457763672,
            96.70000457763672,
            88.0,
            103.0999984741211,
            102.5,
            102.9000015258789,
            102.20000457763672,
            102.9000015258789,
            102.9000015258789,
            101.0,
        ]
    ),
}


def test_calculate_weights(get_xarray, get_gdf, get_out_path):
    """Test calculate weights."""
    user_data = UserCatData(
        ds=get_xarray,
        proj_ds=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        var=var,
        f_feature=get_gdf,
        proj_feature=shp_crs,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tempfile.name,
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    for stat in ["mean", "std", "median", "min", "max"]:
        tmpdir = TemporaryDirectory()
        reference_array = stats_test_dict[stat]
        agg_gen = AggGen(
            user_data=user_data,
            stat_method=stat,
            agg_engine="serial",
            agg_writer="csv",
            weights=tempfile.name,
            out_path=tmpdir.name,
            file_prefix=stats_agg_file_prefix,
        )

        _ngdf, _vals = agg_gen.calculate_agg()

        assert isinstance(_ngdf, gpd.GeoDataFrame)
        assert isinstance(_vals, xr.Dataset)

        _testvals = _vals[var[0]].isel(time=5).values

        assert (
            len(reference_array[np.isnan(reference_array)])
            == len(_testvals[np.isnan(_testvals)])
            == 10
        )
        np.testing.assert_allclose(
            _testvals[~np.isnan(_testvals)],
            reference_array[~np.isnan(reference_array)],
            rtol=1e-4,
            verbose=True,
        )

        ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
        assert ofile.exists()

        outfile = pd.read_csv(ofile)
        print(outfile.head())

    for stat in [
        "masked_mean",
        "masked_std",
        "masked_median",
        "masked_min",
        "masked_max",
        "masked_count",
        "count",
    ]:
        tmpdir = TemporaryDirectory()
        reference_array = stats_test_dict[stat]
        agg_gen = AggGen(
            user_data=user_data,
            stat_method=stat,
            agg_engine="serial",
            agg_writer="csv",
            weights=tempfile.name,
            out_path=tmpdir.name,
            file_prefix=stats_agg_file_prefix,
        )

        _ngdf, _vals = agg_gen.calculate_agg()

        assert isinstance(_ngdf, gpd.GeoDataFrame)
        assert isinstance(_vals, xr.Dataset)

        _testvals = _vals[var[0]].isel(time=5).values

        assert (
            len(reference_array[np.isnan(reference_array)])
            == len(_testvals[np.isnan(_testvals)])
            == 0
        )
        np.testing.assert_allclose(
            _testvals[~np.isnan(_testvals)],
            reference_array[~np.isnan(reference_array)],
            rtol=1e-4,
            verbose=True,
        )

        ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
        assert ofile.exists()

        outfile = pd.read_csv(ofile)
        print(outfile.head())
