import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import rasterio
from geopandas import GeoSeries
from rasterio.windows import from_bounds
from matplotlib import patheffects

from .lotMatcher import find_best_match
from .geometry_utils import convert_to_raster_crs, calculate_bbox, load_lots
from .plot_utils import plot_lots


RASTER_PATH = r"F:\geoprocessamento\base\Ortofotos VR 2022\Imagem Completa\VoltaRedonda_Completo.tif"
LOTS_PATH = r"C:\Users\Administrator\Projetos\pdfGeneratorProj\backend\data\lotesLayer\lotesLayer.gpkg"
OUTPUT_CROP_PATH = r"C:\Users\Administrator\Projetos\pdfGeneratorProj\backend\src\cuts\recorte_teste2.png"

DEFAULT_BUFFER_DISTANCE = 80
PLOT_SIZE = (8, 8)
ASPECT_RATIO = 1.2
HEIGHT_RATIO = 0.85
SAVE_DPI = 150


def highlight_lot(
    wkt_geom: str,
    buffer_distance: float = DEFAULT_BUFFER_DISTANCE,
    output_path: str = OUTPUT_CROP_PATH,
) -> None:
   

    with rasterio.open(RASTER_PATH) as src:
        raster_crs = src.crs

    lots_gdf = load_lots(LOTS_PATH, raster_crs)
    main_lot = convert_to_raster_crs(wkt_geom, raster_crs)
    

    buffered_lot = main_lot.buffer(buffer_distance)
    lots_clip = lots_gdf[lots_gdf.geometry.intersects(buffered_lot)]
    lots_clip_buffered = lots_clip.copy()
    lots_clip_buffered["geometry"] = lots_clip_buffered.geometry.intersection(buffered_lot)

  
    matched_lot, _ = find_best_match(main_lot, lots_clip)
    bbox = calculate_bbox(matched_lot, buffer_distance, ASPECT_RATIO, HEIGHT_RATIO)


    with rasterio.open(RASTER_PATH) as src:
        window = from_bounds(*bbox.bounds, transform=src.transform)
        out_image = src.read(window=window)
        out_transform = src.window_transform(window)

   
    fig, ax = plt.subplots(figsize=PLOT_SIZE)
    height, width = out_image.shape[1], out_image.shape[2]
    left, top = out_transform * (0, 0)
    right, bottom = out_transform * (width, height)

    ax.imshow(out_image.transpose(1, 2, 0), extent=(left, right, bottom, top))

    plot_lots(ax, matched_lot, lots_clip_buffered, patheffects)

    ax.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=SAVE_DPI, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    print(f"✅ Recorte do raster salvo em: {output_path}")
