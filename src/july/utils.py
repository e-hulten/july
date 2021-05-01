from datetime import datetime as dt
from datetime import date, timedelta
from typing import Union, List, Any, Tuple


def date_range(start_date: Union[str, date], end_date: Union[str, date]) -> List[date]:
    if not isinstance(start_date, date):
        start_date = dt.strptime(start_date, "%Y-%m-%d")
    if not isinstance(end_date, date):
        end_date = dt.strptime(end_date, "%Y-%m-%d")

    rng_diff = end_date - start_date
    return [start_date + timedelta(days=x) for x in range(0, rng_diff.days + 1)]


def preprocess_inputs(
    dates: List[Union[date, str]], data: List[Any]
) -> Tuple[List[date], List[Union[int, Any]]]:
    # Sort dates and values by dates.
    sorted_by_date = sorted([*zip(dates, data)], key=lambda x: x[0])
    # Dict mapping date to value.
    data_dict = dict(sorted_by_date)
    # Fill in date range if not complete.
    dates = date_range(dates[0], dates[-1])
    # Fill in zero for added dates.
    data = [data_dict.get(date, 0) for date in dates]

    return dates, data
