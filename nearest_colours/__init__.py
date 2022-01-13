import colorsys
from pathlib import Path
from typing import List, Literal, Union

import numpy as np
import pandas as pd
from colour import Color

__version__ = "1.0.0"
ColorSpace = Literal["hsv", "rgb", "yiq", "hls"]
Profile = Literal["x11", "w3c"]


def nearest_x11(color: Union[Color, str], n: int = 1, space: ColorSpace = "hls") -> List[Color]:
    return _nearest(Color(color), n, space, color_table=_x11_colors)


def nearest_w3c(color: Union[Color, str], n: int = 1, space: ColorSpace = "hls") -> List[Color]:
    return _nearest(Color(color), n, space, color_table=_w3c_colors)


def _nearest(color: Color, n: int = 1, space: ColorSpace = "hls", *, color_table: pd.DataFrame) -> List[Color]:
    if space == "rgb":
        color_point = color.rgb
    else:
        color_point = getattr(colorsys, f"rgb_to_{space}")(*color.rgb)

    unique_colors = color_table.groupby("hex").first()
    points = unique_colors[space].values.astype(float)
    points_sq_dist = np.sum((points - color_point)**2, axis=1)
    argsort = np.argsort(points_sq_dist)
    ranked_colors = unique_colors.iloc[argsort]
    n_nearest = ranked_colors.iloc[:n]
    result = n_nearest["color", ""].tolist()

    return result


def _load_colors(profile: Profile) -> pd.DataFrame:
    _package_dir = Path(__file__).parent
    table = pd.read_csv(_package_dir / f"{profile}.csv")

    columns = pd.MultiIndex.from_tuples([
        ("name", ""),
        ("hex", ""),
        ("color", ""),
        *(
            (space, letter)
            for space in ["rgb", "hls", "hsv", "yiq"]
            for letter in space
        )
    ])
    colors = pd.DataFrame(columns=columns)

    colors["name", ""] = table["name"]
    colors["hex", ""] = table["hex"]
    colors["color", ""] = table["hex"].apply(Color)

    for i, row in colors.iterrows():
        rgb = row["color", ""].rgb

        colors.loc[i, "rgb"] = rgb
        colors.loc[i, "hsv"] = colorsys.rgb_to_hsv(*rgb)
        colors.loc[i, "hls"] = colorsys.rgb_to_hls(*rgb)
        colors.loc[i, "yiq"] = colorsys.rgb_to_yiq(*rgb)

    return colors


_w3c_colors = _load_colors("w3c")
_x11_colors = _load_colors("x11")
