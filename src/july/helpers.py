import numpy as np
from typing import List, Any
from datetime import date


def date_grid(dates: List[date], data: List[Any], flip: bool, dtype: str = "float64"):
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
