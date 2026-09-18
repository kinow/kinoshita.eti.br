#!/usr/bin/env python3

"""Create Brazilian 'caquinhos de cerâmica' for Inkscape.

The mosaic is generated as a Voronoi diagram.

Each Voronoi cell is inset by half of the requested gap,
creating a real geometric gap between neighbouring pieces.

For a 1.5 pt gap:

    left piece loses 0.75 pt
    right piece loses 0.75 pt
    total gap = 1.5 pt

No stroke is used for the gap.
"""

import math
import random
from argparse import ArgumentParser
from typing import TypeAlias

import inkex
from inkex.paths import Line, Move, Path

Point: TypeAlias = tuple[float, float]
Polygon: TypeAlias = list[Point]


def add_arguments(parser: ArgumentParser) -> None:
    """Define command-line arguments.

    Args:
        parser: Command-line argument parser.
    """
    parser.add_argument(
        "--width",
        type=float,
        default=58.0,
        help="Mosaic width in cm.",
    )

    parser.add_argument(
        "--height",
        type=float,
        default=40.0,
        help="Mosaic height in cm.",
    )

    parser.add_argument(
        "--pieces",
        type=int,
        default=180,
        help="Approximate number of ceramic pieces.",
    )

    parser.add_argument(
        "--min-size",
        type=float,
        default=3.0,
        help="Approximate minimum piece diameter in cm.",
    )

    parser.add_argument(
        "--max-size",
        type=float,
        default=5.0,
        help="Approximate maximum piece diameter in cm.",
    )

    parser.add_argument(
        "--gap",
        type=float,
        default=1.5,
        help="Actual gap between pieces in Inkscape points.",
    )

    parser.add_argument(
        "--red",
        type=str,
        default="#8B4513",
        help="Red/brown ceramic colour.",
    )

    parser.add_argument(
        "--yellow",
        type=str,
        default="#FFD700",
        help="Yellow ceramic colour.",
    )

    parser.add_argument(
        "--black",
        type=str,
        default="#000000",
        help="Black ceramic colour.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible output.",
    )


def random_colour(
        red: str,
        yellow: str,
        black: str,
) -> str:
    """Choose a ceramic colour using a 96/3/1 distribution.

    Args:
        red: Reddish ceramic colour.
        yellow: Yellow ceramic colour.
        black: Black ceramic colour.

    Returns:
        The selected colour.
    """
    value = random.random()  # NOSONAR

    if value < 0.96:
        return red

    if value < 0.99:
        return yellow

    return black


def generate_seed_points(
        width: float,
        height: float,
        pieces: int,
        min_size: float,
        max_size: float,
) -> list[Point]:
    """Generate fast, evenly distributed Voronoi seed points.

    A regular grid is used as the starting point, with random
    displacement applied to each seed to avoid an overly regular
    appearance.

    Args:
        width: Mosaic width in cm.
        height: Mosaic height in cm.
        pieces: Requested number of Voronoi cells.
        min_size: Approximate minimum piece diameter in cm.
        max_size: Approximate maximum piece diameter in cm.

    Returns:
        A list of Voronoi seed coordinates.
    """
    if pieces <= 0:
        return []

    aspect_ratio = width / height

    rows = max(
        1,
        round(
            math.sqrt(
                pieces / aspect_ratio,
            ),
        ),
    )

    columns = max(
        1,
        math.ceil(
            pieces / rows,
        ),
    )

    cell_width = width / columns
    cell_height = height / rows

    candidates: list[Point] = []

    for row in range(rows):
        for column in range(columns):
            x = (
                        column
                        + random.uniform(0.2, 0.8)
                ) * cell_width

            y = (
                        row
                        + random.uniform(0.2, 0.8)
                ) * cell_height

            candidates.append(
                (x, y),
            )

    random.shuffle(candidates)  # NOSONAR

    points = candidates[:pieces]

    # The requested sizes influence the amount of organic
    # displacement. This keeps the argument meaningful while
    # retaining the fast grid-based algorithm.
    average_size = (min_size + max_size) / 2.0

    size_factor = max(
        0.0,
        min(
            1.0,
            average_size / 5.0,
        ),
    )

    # To make the diagram less mechanical... moves the pieces a bit by a random
    # amount... Later we will clamp the coordinates (the ``max``, ``min``, below).
    # This avoids that some points are out of bounds.
    jitter = (
            min(cell_width, cell_height)
            * 0.18
            * (0.8 + 0.2 * size_factor)
    )

    result: list[Point] = []

    for x, y in points:
        x += random.uniform(
            -jitter,
            jitter,
        )

        y += random.uniform(
            -jitter,
            jitter,
        )

        x = max(
            0.0,
            min(width, x),
        )

        y = max(
            0.0,
            min(height, y),
        )

        result.append(
            (x, y),
        )

    return result


def clip_polygon(
        polygon: Polygon,
        nx: float,
        ny: float,
        limit: float,
) -> Polygon:
    """Clip a polygon against nx*x + ny*y <= limit.

    Args:
        polygon: Polygon to clip.
        nx: X component of clipping-plane normal.
        ny: Y component of clipping-plane normal.
        limit: Clipping-plane limit.

    Returns:
        The clipped polygon.
    """
    if not polygon:
        return []

    result: Polygon = []

    previous = polygon[-1]

    previous_value = (
            nx * previous[0]
            + ny * previous[1]
            - limit
    )

    previous_inside = previous_value <= 0

    for current in polygon:
        current_value = (
                nx * current[0]
                + ny * current[1]
                - limit
        )

        current_inside = current_value <= 0

        if current_inside != previous_inside:
            denominator = (
                    current_value
                    - previous_value
            )

            if denominator != 0:
                fraction = (
                        -previous_value
                        / denominator
                )

                intersection: Point = (
                    previous[0]
                    + fraction
                    * (
                            current[0]
                            - previous[0]
                    ),
                    previous[1]
                    + fraction
                    * (
                            current[1]
                            - previous[1]
                    ),
                )

                result.append(
                    intersection,
                )

        if current_inside:
            result.append(current)

        previous = current
        previous_value = current_value
        previous_inside = current_inside

    return result


def inset_voronoi_cell(
        seed: Point,
        seeds: list[Point],
        width: float,
        height: float,
        inset: float,
) -> Polygon:
    """Create a Voronoi cell physically inset by inset.

    Args:
        seed: Seed point belonging to this cell.
        seeds: All Voronoi seed points.
        width: Mosaic width in cm.
        height: Mosaic height in cm.
        inset: Distance by which each cell is inset.

    Returns:
        The inset Voronoi cell.
    """
    sx, sy = seed

    polygon: Polygon = [
        (inset, inset),
        (width - inset, inset),
        (
            width - inset,
            height - inset,
        ),
        (
            inset,
            height - inset,
        ),
    ]

    for other in seeds:
        if other is seed:
            continue

        ox, oy = other

        dx = ox - sx
        dy = oy - sy

        normal_length = math.hypot(
            dx,
            dy,
        )

        if normal_length == 0:
            continue

        original_limit = (
                                 ox * ox
                                 + oy * oy
                                 - sx * sx
                                 - sy * sy
                         ) / 2.0

        inset_limit = (
                original_limit
                - inset * normal_length
        )

        polygon = clip_polygon(
            polygon,
            dx,
            dy,
            inset_limit,
        )

        if not polygon:
            break

    return polygon


def polygon_area(points: Polygon) -> float:
    """Return the absolute polygon area.

    Args:
        points: Polygon vertices.

    Returns:
        Polygon area in square centimetres.
    """
    if len(points) < 3:
        return 0.0

    area = 0.0

    for index, point in enumerate(points):
        x1, y1 = point

        x2, y2 = points[
            (index + 1) % len(points)
            ]

        area += (
                x1 * y2
                - x2 * y1
        )

    return abs(area) / 2.0


def create_piece_path(points: Polygon) -> Path:
    """Create an SVG path from polygon points.

    Args:
        points: Polygon vertices.

    Returns:
        An Inkscape SVG path.
    """
    path = Path()

    for index, (x, y) in enumerate(points):
        if index == 0:
            path.append(
                Move(x, y),
            )
        else:
            path.append(
                Line(x, y),
            )

    path.close()

    return path


def add_mosaic(
        svg: inkex.SvgDocumentElement,
        width: float,
        height: float,
        pieces: int,
        min_size: float,
        max_size: float,
        gap: float,
        red: str,
        yellow: str,
        black: str,
) -> int:
    """Generate and add the Voronoi mosaic to the SVG.

    Args:
        svg: Root SVG document.
        width: Mosaic width in cm.
        height: Mosaic height in cm.
        pieces: Approximate number of pieces.
        min_size: Approximate minimum piece diameter in cm.
        max_size: Approximate maximum piece diameter in cm.
        gap: Desired gap between pieces in points.
        red: Red/brown ceramic colour.
        yellow: Yellow ceramic colour.
        black: Black ceramic colour.

    Returns:
        Number of generated polygon pieces.
    """
    seeds = generate_seed_points(
        width,
        height,
        pieces,
        min_size,
        max_size,
    )

    # SVG user units are centimetres.
    #
    # 1 pt = 2.54 / 72 cm.
    gap_cm = (
            gap
            * 2.54
            / 72.0
    )

    # Each Voronoi cell loses half of the
    # requested gap.
    #
    # Therefore:
    #
    #     gap / 2 + gap / 2 = gap
    #
    inset = gap_cm / 2.0

    polygons: list[Polygon] = []

    for seed in seeds:
        polygon = inset_voronoi_cell(
            seed,
            seeds,
            width,
            height,
            inset,
        )

        if len(polygon) < 3:
            continue

        if polygon_area(polygon) < 0.5:
            continue

        polygons.append(
            polygon,
        )

    mosaic_group = inkex.Group()

    mosaic_group.set(
        "id",
        "caquinhos-mosaic",
    )

    guaranteed_colours = [
        red,
        yellow,
        black,
    ]

    for index, polygon in enumerate(polygons):
        element = inkex.PathElement()

        element.set(
            "d",
            str(
                create_piece_path(
                    polygon,
                ),
            ),
        )

        if index < len(guaranteed_colours):
            fill = guaranteed_colours[index]
        else:
            fill = random_colour(
                red,
                yellow,
                black,
            )

        element.style = {
            "fill": fill,
            "stroke": "none",
        }

        mosaic_group.append(
            element,
        )

    # Put the mosaic underneath the existing SVG artwork.
    svg.insert(
        0,
        mosaic_group,
    )

    return len(polygons)


class MosaicExtension(inkex.EffectExtension):
    """Inkscape extension adapter for the mosaic generator."""

    def add_arguments(self, pars) -> None:
        """Register extension command-line arguments.

        Args:
            pars: Inkscape argument parser.
        """
        add_arguments(pars)

    def effect(self) -> None:
        """Generate the mosaic and add it to the SVG document."""
        if self.options.seed is not None:
            random.seed(
                self.options.seed,
            )

        svg = self.document.getroot()

        add_mosaic(
            svg=svg,
            width=self.options.width,
            height=self.options.height,
            pieces=self.options.pieces,
            min_size=self.options.min_size,
            max_size=self.options.max_size,
            gap=self.options.gap,
            red=self.options.red,
            yellow=self.options.yellow,
            black=self.options.black,
        )


if __name__ == "__main__":
    MosaicExtension().run()
