import numpy as np
import calendar
from typing import List, Any
from datetime import date
from july.helpers import date_grid, cal_heatmap, add_date_label, get_month_outline
from july.utils import preprocess_inputs, preprocess_month


def calendar_heatmap(
    dates,
    data,
    flip=False,
    title=None,
    cmap="Greens",
    colorbar=False,
    date_label=False,
    weekday_label=True,
    month_label=False,
    year_label=False,
    month_grid=False,
    cmin=None,
    cmax=None,
    ax=None,
):
    dates, data = preprocess_inputs(dates, data)
    cal = date_grid(dates, data, flip)
    ax = cal_heatmap(
        cal=cal,
        dates=dates,
        flip=flip,
        title=title,
        cmap=cmap,
        colorbar=colorbar,
        date_label=date_label,
        weekday_label=weekday_label,
        month_label=month_label,
        year_label=year_label,
        month_grid=month_grid,
        cmin=cmin,
        cmax=cmax,
        ax=ax,
    )

    return ax


def month_plot(
    dates: List[date],
    data: List[Any],
    flip: bool = False,
    month: int = None,
    date_label: bool = False,
    cal_mode: bool = False,
    ax=None,
):
    month = month or dates[0].month
    dates, data = preprocess_month(dates, data, month=month)
    month_grid = date_grid(dates, data, flip=flip)
    weeknum_grid = date_grid(dates, [d.isocalendar()[1] for d in dates], flip=flip)
    weeknum_labels = [int(x) for x in np.unique(weeknum_grid) if np.isfinite(x)]

    if cal_mode:
        # Pad all grids to have six rows so they align when plotted side by side.
        while len(month_grid) < 6:
            month_grid = np.vstack([month_grid, 7 * [np.nan]])
            weeknum_labels.append("")

    ax = cal_heatmap(
        cal=month_grid,
        dates=dates,
        flip=flip,
        year_label=False,
        month_label=False,
        ax=ax,
    )

    if date_label:
        add_date_label(ax, dates, flip)

    ax.tick_params(axis="y", pad=8)
    if flip:
        ax.set_xticks([i + 0.5 for i in range(month_grid.shape[1])])
        ax.set_xticklabels(weeknum_labels)
    else:
        ax.set_yticks([i + 0.5 for i in range(month_grid.shape[0])])
        ax.set_yticklabels(weeknum_labels)

    outline_coords = get_month_outline(dates, month_grid, flip, month)
    ax.plot(outline_coords[:, 0], outline_coords[:, 1], color="black", linewidth=2)
    ax.set_xlim(ax.get_xlim()[0] - 0.1, ax.get_xlim()[1] + 0.1)
    ax.set_ylim(ax.get_ylim()[0] + 0.1, ax.get_ylim()[1] - 0.1)
    ax.set_title(calendar.month_name[month], fontname="monospace", fontsize=14, pad=20)
    ax.set_frame_on(False)

    return ax
