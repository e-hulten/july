import calendar
from datetime import datetime as dt
from datetime import date, datetime, timedelta
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
    # Convert strings to datetime.
    dates = [dt.strptime(d, "%Y-%m-%d") if isinstance(d, str) else d for d in dates]
    # Strip datetimes to date.
    dates = [d.date() if isinstance(d, datetime) else d for d in dates]
    # Sort dates and values by dates.
    sorted_by_date = sorted([*zip(dates, data)], key=lambda x: x[0])
    # Dict mapping date to value.
    data_dict = dict(sorted_by_date)
    # Fill in date range if not complete.
    dates = date_range(dates[0], dates[-1])
    # Fill in zero for added dates.
    data = [data_dict.get(date, 0) for date in dates]

    return dates, data


def preprocess_month(dates, data, month=None):
    # Set month for filtering
    month = month or dates[0].month
    # Strip datetimes to date.
    dates = [d.date() if isinstance(d, datetime) else d for d in dates]

    # Sort dates and values by date.
    sorted_by_date = sorted([*zip(dates, data)], key=lambda x: x[0])

    if len(set([d.year for d in dates if d.month == month])) != 1:
        raise ValueError(
            f"More than one year with month {month} in input 'dates'. "
            "Month is not uniquely defined."
        )

    # Filter relevant month.
    month_list = [(day, val) for day, val in sorted_by_date if day.month == month]
    # Dict mapping date to value.
    data_dict = dict(month_list)

    year = list(data_dict.keys())[0].year
    # Get last day of month.
    last_day = calendar.monthrange(year, month)[1]

    # Fill in date range if range is not complete.
    if len(data_dict) != last_day:
        first_date = date(year, month, 1)
        last_date = date(year, month, last_day)
        dates = date_range(first_date, last_date)
        # Fill in zero for added dates.
        data = [data_dict.get(date, 0) for date in dates]
    else:
        dates = list(data_dict.keys())
        data = list(data_dict.values())

    return dates, data
