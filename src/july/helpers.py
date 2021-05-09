import calendar
import numpy as np
import matplotlib.pyplot as plt
from july.colormaps import cmaps_dict
from matplotlib.pyplot import Axes
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.ticker import ScalarFormatter
from typing import List, Any, Optional, Union
from datetime import date


def date_grid(
    dates: List[date], data: List[Any], horizontal: bool, dtype: str = "float64"
) -> np.ndarray:
    # Array with columns (iso year, iso week number, iso weekday).
    iso_dates = np.array([day.isocalendar() for day in dates])
    # Unique weeks, as defined by the tuple (iso year, iso week).
    unique_weeks = sorted(list(set([tuple(row) for row in iso_dates[:, :2]])))

    # Get dict that maps week tuple to week index in grid.
    weeknum2idx = {week: i for i, week in enumerate(unique_weeks)}
    week_coords = np.array([weeknum2idx[tuple(week)] for week in iso_dates[:, :2]])
    day_coords = iso_dates[:, 2] - 1

    # Define shape of grid.
    n_weeks = len(unique_weeks)
    n_days = 7

    # Create grid and fill with data.
    grid = np.empty((n_weeks, n_days), dtype=dtype)
    grid = np.nan * grid if dtype == "float64" else grid
    grid[week_coords, day_coords] = data

    if horizontal:
        return grid.T

    return grid


def cal_heatmap(
    cal: np.ndarray,
    dates: List[date],
    horizontal: bool,
    cmap: Union[str, LinearSegmentedColormap, ListedColormap] = "Greens",
    value_label: bool = False,
    date_label: bool = False,
    weekday_label: bool = True,
    month_label: bool = True,
    year_label: bool = True,
    month_grid: bool = False,
    colorbar: bool = False,
    frame_on: bool = False,
    value_format: str = "int",
    title: Optional[str] = None,
    cmin: Optional[int] = None,
    cmax: Optional[int] = None,
    cbar_label_format: Optional[str] = None,
    ax: Optional[Axes] = None,
):
    if not ax:
        figsize = (12, 5) if horizontal else (5, 12)
        fig, ax = plt.subplots(figsize=figsize, dpi=100)
    else:
        fig = ax.get_figure()

    if isinstance(cmap, str):
        cmap = cmaps_dict[cmap]

    if value_label and date_label:
        raise ValueError(
            "Maximum one of 'value_label' and 'date_label' can be "
            f"set as 'True'. Got: 'value_label'={value_label} and"
            f"'date_label'={date_label}."
        )

    pc = ax.pcolormesh(cal, edgecolors=ax.get_facecolor(), linewidth=0.25, cmap=cmap)
    pc.set_clim(cmin or np.nanmin(cal), cmax or np.nanmax(cal))
    ax.invert_yaxis()
    ax.set_aspect("equal")
    bbox = ax.get_position()

    if value_label:
        add_value_label(ax, cal, value_format)
    if date_label:
        add_date_label(ax, dates, horizontal)
    else:
        ax.set_xticklabels("")
    if weekday_label:
        add_weekday_label(ax, horizontal)
    if month_label:
        add_month_label(ax, dates, horizontal)
    if year_label:
        add_year_label(ax, dates, horizontal)
    if month_grid:
        add_month_grid(ax, dates, cal, horizontal)
    if colorbar:
        add_colorbar(pc, fig, ax, bbox, cbar_label_format)
    if title:
        ax.set_title(title)

    ax.set_frame_on(frame_on)
    return ax


def add_value_label(ax, cal, value_format):
    if value_format == "int":
        val_format = "{:0.0f}"
    elif value_format == "decimal":
        val_format = "{:0.1f}"
    else:
        raise ValueError(
            "Argument 'value_format' must be equal to either "
            f"'int' or 'float'. Got: {value_format}."
        )

    for (i, j), z in np.ndenumerate(cal):
        if np.isfinite(z):
            ax.text(j + 0.5, i + 0.5, val_format.format(z), ha="center", va="center")


def add_date_label(ax, dates: List[date], horizontal: bool) -> None:
    days = [day.day for day in dates]
    day_grid = date_grid(dates, days, horizontal)

    for (i, j), z in np.ndenumerate(day_grid):
        if np.isfinite(z):
            ax.text(j + 0.5, i + 0.5, int(z), ha="center", va="center")


def add_weekday_label(ax, horizontal: bool) -> None:
    if horizontal:
        ax.tick_params(axis="y", which="major", pad=8)
        ax.set_yticks([x + 0.5 for x in range(0, 7)])
        ax.set_yticklabels(
            calendar.weekheader(width=1).split(" "),
        )
    else:
        ax.tick_params(axis="x", which="major", pad=4)
        ax.set_xticks([x + 0.5 for x in range(0, 7)])
        ax.set_xticklabels(
            calendar.weekheader(width=1).split(" "),
        )
        ax.xaxis.tick_top()


def add_month_label(ax, dates: List[date], horizontal: bool) -> None:
    month_years = [(day.year, day.month) for day in dates]
    month_years_str = list(map(str, month_years))
    month_year_grid = date_grid(dates, month_years_str, horizontal, dtype="object")

    unique_month_years = sorted(set(month_years))

    month_locs = {}
    for month in unique_month_years:
        # Get 'avg' x, y coordinates of elements in grid equal to month_year.
        yy, xx = np.nonzero(month_year_grid == str(month))
        month_locs[month] = (
            xx.max() + 1 + xx.min() if horizontal else yy.max() + 1 + yy.min()
        ) / 2

    # Get month label for each unique month_year.
    month_labels = [calendar.month_abbr[x[1]] for x in month_locs.keys()]

    if horizontal:
        ax.set_xticks([*month_locs.values()])
        ax.set_xticklabels(month_labels, ha="center")
    else:
        ax.set_yticks([*month_locs.values()])
        ax.set_yticklabels(month_labels, rotation=90, va="center")


def add_year_label(ax, dates, horizontal):
    years = [day.year for day in dates]
    year_grid = date_grid(dates, years, horizontal)
    unique_years = sorted(set(years))

    year_locs = {}
    for year in unique_years:
        yy, xx = np.nonzero(year_grid == year)
        year_locs[year] = (
            xx.max() + 1 + xx.min() if horizontal else yy.max() + 1 + yy.min()
        ) / 2

    if horizontal:
        for year, loc in year_locs.items():
            ax.annotate(
                year,
                (loc / year_grid.shape[1], 1),
                (0, 12),
                xycoords="axes fraction",
                textcoords="offset points",
                fontsize="large",
                va="center",
                ha="center",
            )
    else:
        for year, loc in year_locs.items():
            ax.annotate(
                year,
                (0, 1 - loc / len(year_grid)),
                (-40, 0),
                xycoords="axes fraction",
                textcoords="offset points",
                fontsize="large",
                rotation=90,
                va="center",
            )


def add_colorbar(pc, fig, ax, bbox, cbar_label_format):
    adj_bbox = ax.get_position()
    height_diff = adj_bbox.height - bbox.height
    # Specify location and dimensions: [left, bottom, width, height].
    # This part is still not perfect when month_grid is True.
    cax = fig.add_axes(
        [
            bbox.x1 + 0.015,
            adj_bbox.y0 + height_diff / 2,
            0.015,
            bbox.height,
        ]
    )
    cbar_label_format = cbar_label_format or ScalarFormatter()
    plt.colorbar(pc, cax=cax, format=cbar_label_format)


def get_month_outline(dates, month_grid, horizontal, month):
    # This code is so ugly I'm amazed that it works.
    day_grid = date_grid(dates, dates, horizontal=False, dtype="object")
    if horizontal:
        month_grid = month_grid.T

    nrows, ncols = month_grid.shape
    coords_list = []
    for y in range(nrows):
        for x in range(ncols):
            if np.isfinite(month_grid[y, x]):
                if day_grid[y, x].month == month:
                    coords_list.append((x, y))

    sorted_coords = np.array(coords_list)
    min_y = sorted_coords[:, 1].min()
    max_y = sorted_coords[:, 1].max()
    upper_left = sorted_coords[0]
    upper_right = np.array([7, min_y])
    lower_right = np.array([7, max_y])
    lower_right2 = sorted_coords[-1] + np.array([1, 1])

    lower_right1 = (
        lower_right2
        if np.array_equal(lower_right, lower_right2)
        else lower_right2 - np.array([0, 1])
    )
    lower_left = np.array([0, sorted_coords[:, 1].max() + 1])
    corner_last = upper_left + np.array([0, 1])
    second_last = np.copy(corner_last)
    second_last[0] = 0

    coords = np.array(
        [
            upper_left,
            upper_right,
            lower_right,
            lower_right1,
            lower_right2,
            lower_left,
            second_last,
            corner_last,
            upper_left,
        ]
    )

    return coords[:, [1, 0]] if horizontal else coords


def add_month_grid(ax, dates, month_grid, horizontal):
    months = set([d.month for d in dates])
    for month in months:
        coords = get_month_outline(
            dates, month_grid, horizontal=horizontal, month=month
        )
        ax.plot(coords[:, 0], coords[:, 1], color="black", linewidth=1)

    # Pad axes so plotted line appears uniform also along edges.
    ax.set_xlim(ax.get_xlim()[0] - 0.1, ax.get_xlim()[1] + 0.1)
    ax.set_ylim(ax.get_ylim()[0] + 0.1, ax.get_ylim()[1] - 0.1)

    fig = ax.get_figure()
    # Set frame in facecolor instead of turning off frame to keep cbar alignment.
    for pos in ["top", "bottom", "right", "left"]:
        ax.spines[pos].set_edgecolor(fig.get_facecolor())
    return ax


def get_calendar_title(years: List[int]):
    if len(years) == 1:
        return f"Calendar {years[0]}"
    elif len(years) == 2:
        return f"Calendar {years[0]} and {years[1]}"
    elif len(years) > 2:
        word_str = "Calendar "
        for year in years[:-1]:
            word_str += f"{year}, "
        return word_str + f", and {years[-1]}"
