import pytest
from pytest import approx
from mapreader import loader
from mapreader.loader.images import mapImages
import os
from pathlib import Path

# functions


@pytest.fixture
def sample_dir():
    return Path(__file__).resolve().parent / "sample_files"


@pytest.fixture
def metadata_patchify(sample_dir):
    """Initialises mapImages object (with metadata from csv and patches).

    Returns
    -------
    list
        image_ID (of parent png image), ts_map (mapImages object), parent_list (== image_ID) and child_list (list of patches).
    """
    image_ID = "map_74488693.png"
    ts_map = loader(f"{sample_dir}/{image_ID}")
    ts_map.add_metadata(f"{sample_dir}/ts_downloaded_maps.csv")
    ts_map.sliceAll(slice_size=1000)
    parent_list = ts_map.list_parents()
    child_list = ts_map.list_children()

    return image_ID, ts_map, parent_list, child_list


# tests


# png tests (separate geo info)
def test_png_loader(sample_dir):
    image_ID = "map_74488693.png"

    ts_map = loader(f"{sample_dir}/{image_ID}")
    assert len(ts_map) == 1
    assert isinstance(ts_map, mapImages)


def test_add_metadata(sample_dir):
    image_ID = "map_74488693.png"

    ts_map = loader(f"{sample_dir}/{image_ID}")
    ts_map.add_metadata(f"{sample_dir}/ts_downloaded_maps.csv")
    assert "coord" in ts_map.images["parent"][image_ID].keys()
    assert ts_map.images["parent"][image_ID]["coord"] == approx(
        (-4.21875, -3.60352, 55.80128, 56.05977), rel=1e-3
    )


# tiff tests (no geo info)
def test_tiff_loaders(sample_dir):
    image_ID = "101101409.1_JPEG.tif"
    tiff = loader(f"{sample_dir}/{image_ID}")
    assert len(tiff) == 1
    assert isinstance(tiff, mapImages)


# geotiff tests (contains geo info)
def test_geotiff_loader(sample_dir):
    image_ID = "101200740.27_JPEG.tif"
    geotiff = loader(f"{sample_dir}/{image_ID}")
    assert len(geotiff) == 1
    assert isinstance(geotiff, mapImages)


def test_addGeoInfo(sample_dir):
    # check it works for geotiff
    image_ID = "101200740.27_JPEG.tif"
    geotiff = loader(f"{sample_dir}/{image_ID}")
    geotiff.addGeoInfo()
    assert "shape" in geotiff.images["parent"][image_ID].keys()
    assert "coord" in geotiff.images["parent"][image_ID].keys()
    assert geotiff.images["parent"][image_ID]["coord"] == approx(
        (-0.06471, -0.04852, 51.60808, 51.61590), rel=1e-3
    )

    # check nothing happens for png/tiff (no metadata)
    image_ID = "map_74488693.png"
    ts_map = loader(f"{sample_dir}/{image_ID}")
    keys = ts_map.images["parent"][image_ID].keys()
    ts_map.addGeoInfo()
    assert ts_map.images["parent"][image_ID].keys() == keys

    image_ID = "101101409.1_JPEG.tif"
    tiff = loader(f"{sample_dir}/{image_ID}")
    keys = tiff.images["parent"][image_ID].keys()
    tiff.addGeoInfo()
    assert tiff.images["parent"][image_ID].keys() == keys


# could add jpeg, IIIF, etc. here too


# test other functions
def test_sliceAll(sample_dir):
    image_ID = "map_74488693.png"
    ts_map = loader(f"{sample_dir}/{image_ID}")
    ts_map.sliceAll(slice_size=1000)
    parent_list = ts_map.list_parents()
    child_list = ts_map.list_children()
    assert len(parent_list) == 1
    assert len(child_list) == 48
    assert os.path.isfile(f"./sliced_images/patch-0-0-1000-1000-#{image_ID}#.png")


def test_shape(sample_dir):
    image_ID = "map_74488693.png"
    ts_map = loader(f"{sample_dir}/{image_ID}")
    ts_map.add_shape()
    # check shape is added for parent image (before adding shape from metadata)
    assert "shape" in ts_map.images["parent"][image_ID].keys()


def test_coord_functions(metadata_patchify, sample_dir):
    # test for png with added metadata
    image_ID, ts_map, _, child_list = metadata_patchify
    ts_map.add_center_coord()
    assert "dlon" in ts_map.images["parent"][image_ID].keys()
    assert "center_lon" in ts_map.images["child"][child_list[0]].keys()

    # test for geotiff with added geoinfo
    image_ID = "101200740.27_JPEG.tif"
    geotiff = loader(f"{sample_dir}/{image_ID}")
    geotiff.addGeoInfo()
    geotiff.add_coord_increments()
    geotiff.add_center_coord(tree_level="parent")
    assert "dlon" in geotiff.images["parent"][image_ID].keys()
    assert "center_lon" in geotiff.images["parent"][image_ID].keys()

    # test for tiff with no geo info (i.e. no coords so nothing should happen)
    image_ID = "101101409.1_JPEG.tif"
    tiff = loader(f"{sample_dir}/{image_ID}")
    keys = tiff.images["parent"][image_ID].keys()
    tiff.add_coord_increments()
    tiff.add_center_coord(tree_level="parent")
    assert tiff.images["parent"][image_ID].keys() == keys


def test_calc_pixel_stats(metadata_patchify, sample_dir):
    image_ID, ts_map, _, child_list = metadata_patchify
    ts_map.calc_pixel_stats()
    # png images should have alpha channel (i.e. "mean_pixel_A" should exist)
    assert "mean_pixel_A" in ts_map.images["child"][child_list[0]].keys()
    assert "std_pixel_A" in ts_map.images["child"][child_list[0]].keys()

    # geotiff/tiff will not have alpha channel, so only RGB returned
    image_ID = "101200740.27_JPEG.tif"
    geotiff = loader(f"{sample_dir}/{image_ID}")
    geotiff.sliceAll(slice_size=1000)
    child_list = geotiff.list_children()
    geotiff.calc_pixel_stats()
    assert "mean_pixel_RGB" in geotiff.images["child"][child_list[0]].keys()
    assert "std_pixel_RGB" in geotiff.images["child"][child_list[0]].keys()


def test_convertImages(metadata_patchify):
    _, ts_map, _, _ = metadata_patchify
    parent_df, patch_df = ts_map.convertImages()
    assert parent_df.shape == (1, 9)
    assert patch_df.shape == (48, 6)
