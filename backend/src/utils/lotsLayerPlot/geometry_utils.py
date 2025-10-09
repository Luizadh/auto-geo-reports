import geopandas as gpd
from geopandas import GeoSeries
from shapely import wkt
from shapely.geometry import box


def load_lots(lots_path: str, raster_crs):
    
    return gpd.read_file(lots_path).to_crs(raster_crs)


def convert_to_raster_crs(wkt_geom: str, raster_crs):
    
    geom = wkt.loads(wkt_geom)
    geom_series = GeoSeries([geom], crs="EPSG:29193")
    return geom_series.to_crs(raster_crs).iloc[0]


def calculate_bbox(matched_lot, buffer_distance: float, aspect_ratio: float, height_ratio: float):

    minx, miny, maxx, maxy = matched_lot.geometry.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2

    lot_width = (maxx - minx) + buffer_distance * 2
    lot_height = (maxy - miny) + buffer_distance * 2

    desired_width = max(lot_width, lot_height * aspect_ratio)
    desired_height = desired_width * height_ratio

    return box(
        cx - desired_width / 2,
        cy - desired_height / 2,
        cx + desired_width / 2,
        cy + desired_height / 2,
    )
