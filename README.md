# Nearest Colours

[![](https://img.shields.io/badge/version-1.0.0-green)](https://pypi.org/project/nearest-colour)
![](https://img.shields.io/badge/Python-&ge;3.8-blue)

Find the nearest W3C/X11 named colors to a given color.
This module, `nearest_colour`, provides two functions:

```python
from typing import List, Literal, Union
from colour import Color

ColorSpace = Literal["hsv", "rgb", "yiq", "hls"]

def nearest_x11(color: Union[Color, str], n: int = 1, space: ColorSpace = "hls") -> List[Color]:
    pass


def nearest_w3c(color: Union[Color, str], n: int = 1, space: ColorSpace = "hls") -> List[Color]:
    pass
```

Each will return the `n` colors that are closest (Euclidean distance) to `color` in the specified color-`space` from either the set of W3C web colors or the set of Unix X11 colors.
Web colors are [standardized by W3C][W3C colors], whereas Unix X11 colors are [defined in the X11 source-code][X11 colors].
**Note:** these two sets of colors are almost entirely overlapping, but not completely.
Colors may be provided as either [colour] `Color` objects, or as W3C colors strings.
The default color-space for distance computation is HSL, which is perceptually uniform and therefore returns colors which are perceptually closer to the given color.
A list is always returned, even if `n == 1`, and the ordering is from most similar to least similar.
If you pass a large wnough integer (say, 256), you'll get the ranking for all colors in the respective set.

[colour]: https://pypi.org/project/colour/
[X11 colors]: https://gitlab.freedesktop.org/xorg/xserver/blob/master/os/oscolor.c
[W3C colors]: https://www.w3.org/wiki/CSS/Properties/color/keywords
