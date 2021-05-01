from july.helpers import date_grid, cal_heatmap
from july.utils import preprocess_inputs


def calendar_heatmap(
    dates,
    data,
    flip=False,
    cmap="Greens",
    colorbar=False,
    date_label=False,
    weekday_label=True,
    month_label=False,
    year_label=False,
    ax=None,
):
    dates, data = preprocess_inputs(dates, data)
    cal = date_grid(dates, data, flip)
    ax = cal_heatmap(
        cal=cal,
        dates=dates,
        flip=flip,
        cmap=cmap,
        colorbar=colorbar,
        date_label=date_label,
        weekday_label=weekday_label,
        month_label=month_label,
        year_label=year_label,
        ax=ax,
    )
    return ax
