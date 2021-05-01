import calendar
import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import ArrayLike
from typing import List, Tuple, Any, Optional
from datetime import date
from datetime import datetime as dt


def date_grid(
    dates: List[date], data: List[Any], flip: bool, dtype: str = "float64"
) -> ArrayLike:
    # Array with columns (iso year, iso week number, iso weekday).
    iso_dates = np.array([day.isocalendar for day in dates])
    # Unique weeks, as defined by the tuple (iso year, iso week).
    unique_weeks = sorted(list(set([tuple(row) for row in iso_dates[:, :2]])))

    # Get dict that maps week tuple to week index in grid.
    weeknum2idx = {week: i for i, week in enumerate(unique_weeks)}
    week_coords = np.array([weeknum2idx[week] for week in iso_dates[:, :2]])
    day_coords = iso_dates[:, 2] - 1

    # Define shape of grid.
    n_weeks = len(unique_weeks)
    n_days = 7

    # Create grid and fill with data.
    grid = np.empty((n_weeks, n_days), dtype=dtype)
    grid = np.nan * grid if dtype == "float64" else grid
    grid[week_coords, day_coords] = data

    if flip:
        return grid.T

    return grid


def cal_heatmap(
    cal: ArrayLike,
    dates,
    flip: bool,
    cmap: str = "Greens",
    colorbar: bool = False,
    date_label: bool = False,
    month_label: bool = False,
    # grid_lines=True,
    ax: Optional[Tuple[int]] = None,
):
    if not ax:
        figsize = (10, 5) if flip else (5, 10)
        fig, ax = plt.subplots(figsize=figsize, dpi=100)

    pc = ax.pcolormesh(cal, edgecolors="white", linewidth=0.25, cmap=cmap)
    ax.invert_yaxis()
    ax.set_aspect("equal")

    if colorbar:
        bbox = ax.get_position()
        # Specify location and dimensions: [left, bottom, width, height].
        cax = fig.add_axes([bbox.x1 + 0.015, bbox.y0, 0.015, bbox.height])
        plt.colorbar(pc, cax=cax)

    if date_label:
        add_date_label(ax, dates, flip)
    if month_label:
        add_month_label(ax, dates, flip)
    if flip:
        ax.set_yticks([x + 0.5 for x in range(0, 7)])
        ax.set_yticklabels(calendar.weekheader(width=1).split(" "))
    else:
        ax.set_xticks([x + 0.5 for x in range(0, 7)])
        ax.set_xticklabels(calendar.weekheader(width=1).split(" "))
        ax.xaxis.tick_top()

    ax.tick_params(axis="both", which="both", length=0)

    return ax


def add_date_label(ax, dates: List[date], flip: bool) -> None:
    days = [day.day for day in dates]
    grid = date_grid(dates, days, flip)

    for i, j in np.ndindex(grid.shape):
        try:
            ax.text(j + 0.5, i + 0.5, int(date_grid[i, j]), ha="center", va="center")
        except ValueError:
            # If date_grid[i, j] is nan.
            pass


def add_month_label(ax, dates: List[date], flip: bool) -> None:
    # Uniquely define months with string tuple (YYYY, MM).
    month_years = [(day.year, day.month) for day in dates]
    # Convert tuples to string. Get grid with entries "(YYYY, MM)".
    month_years_str = list(map(str, month_years))
    month_year_grid = date_grid(dates, month_years_str, flip, dtype="object")

    unique_month_years = sorted(set(month_years))

    month_locs = {}
    for month in unique_month_years:
        # Get 'avg' x, y coordinates of elements in grid equal to month_year.
        yy, xx = np.nonzero(month_year_grid == str(month))
        month_locs[month] = (xx.max() + xx.min() if flip else yy.max() + yy.min()) / 2

    # Get month label for each unique month_year.
    month_labels = [calendar.month_abbr[x[1]] for x in month_locs.keys()]

    if flip:
        ax.set_xticks([*month_locs.values()])
        ax.set_xticklabels(month_labels, fontsize=14)
    else:
        ax.set_yticks([*month_locs.values()])
        ax.set_yticklabels(month_labels, fontsize=14, rotation=90)
