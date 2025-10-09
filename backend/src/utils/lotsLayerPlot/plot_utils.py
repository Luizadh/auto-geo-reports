from geopandas import GeoSeries


def plot_lots(ax, matched_lot, lots_clip_buffered, patheffects):

  
    GeoSeries([matched_lot.geometry]).plot(
        ax=ax, facecolor="none", edgecolor="red", linewidth=2, zorder=3
    )

  
    if not lots_clip_buffered.empty:
        lots_clip_buffered.plot(
            ax=ax, facecolor="none", edgecolor="yellow", linewidth=1, zorder=2
        )
        for _, row in lots_clip_buffered.iterrows():
            if "num_lote" in row and row["num_lote"] is not None:
                cx, cy = row.geometry.centroid.x, row.geometry.centroid.y
                ax.text(
                    cx,
                    cy,
                    str(row["num_lote"]),
                    color="black",
                    fontsize=7,
                    ha="center",
                    va="center",
                    zorder=4,
                    path_effects=[patheffects.withStroke(linewidth=1.5, foreground="yellow")],
                )
