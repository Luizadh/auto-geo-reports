
from typing import Optional, Tuple, Dict, Any
import math
import geopandas as gpd
from shapely.geometry.base import BaseGeometry
import pandas as pd


def find_best_match(
    principal_geom: BaseGeometry,
    candidates_gdf: gpd.GeoDataFrame,
    weights: Optional[Dict[str, float]] = None,
    debug: bool = False,
    return_all_scores: bool = False,
) -> Tuple[Optional[gpd.GeoSeries], Optional[Dict[str, Any]]]:
   
   
    if weights is None:
        weights = {"coverage": 0.55, "centroid": 0.35, "area": 0.10}

   
    total_w = sum(weights.values())
    if abs(total_w - 1.0) > 1e-6:
       
        weights = {k: v / total_w for k, v in weights.items()}

    if candidates_gdf is None or len(candidates_gdf) == 0:
        return None, None

   
    area_p = principal_geom.area
    if area_p <= 0:
        raise ValueError("Principal geometry has zero area")

    minx, miny, maxx, maxy = principal_geom.bounds
    diag = math.hypot(maxx - minx, maxy - miny)
    scale = max(diag, 1e-6)

    rows = []

    for idx, candidate in candidates_gdf.iterrows():
        cand_geom = candidate.geometry
       
        if cand_geom is None or cand_geom.is_empty:
            continue

       
        try:
            inter = principal_geom.intersection(cand_geom)
            area_i = inter.area
        except Exception:
            area_i = 0.0

        coverage = max(0.0, min(1.0, area_i / area_p))

        
        d = principal_geom.centroid.distance(cand_geom.centroid)
        norm_d = min(1.0, d / scale)
        centroid_sim = 1.0 - norm_d

        
        area_c = cand_geom.area
        rel_diff = min(1.0, abs(area_c - area_p) / area_p)
        area_sim = 1.0 - rel_diff

        score = (
            weights["coverage"] * coverage
            + weights["centroid"] * centroid_sim
            + weights["area"] * area_sim
        )

        rows.append(
            {
                "index": idx,
                "coverage": coverage,
                "centroid_sim": centroid_sim,
                "area_sim": area_sim,
                "score": score,
            }
        )

        
        if coverage >= 0.8 and centroid_sim >= 0.8:
            best_idx = idx
            best_metrics = rows[-1]
            best_row = candidates_gdf.loc[best_idx]
            info = {**best_metrics, "candidate_index": best_idx}
            if debug:
                print("Early accept candidate", best_idx, info)
            if return_all_scores:
                scores_df = pd.DataFrame(rows).set_index("index")
                info["scores_df"] = scores_df
            return best_row, info

    
    scores_df = pd.DataFrame(rows).set_index("index")
    if scores_df.empty:
        return None, None

    best_idx = scores_df["score"].idxmax()
    best_metrics = scores_df.loc[best_idx].to_dict()
    best_row = candidates_gdf.loc[best_idx]

    info = {**best_metrics, "candidate_index": best_idx}

    if debug:
        print("Best candidate index:", best_idx)
        print(scores_df.sort_values("score", ascending=False).head(5))

    if return_all_scores:
        info["scores_df"] = scores_df

    return best_row, info



if __name__ == "__main__":
    print("lotMatcher module loaded. Call find_best_match(principal_geom, candidates_gdf)")
