import calendar
import datetime
from datetime import datetime as dt
from datetime import timedelta
from typing import Union, List, Any, Tuple, Optional


def date_converter(date: Union[str, datetime.date, datetime.datetime]) -> datetime.date:
    if isinstance(date, str):
        return dt.strptime(date, "%Y-%m-%d").date()
    elif isinstance(date, datetime.datetime):
        return date.date()
    elif isinstance(date, datetime.date):
        # Check this last, as isinstance(<datetime object>, datetime.date) is True.
        return date
    else:
        raise ValueError(
            "Expected 'date' to be type: [str, datetime.date, datetime.datetime]. "
            f"Got: {type(date)}."
        )


def date_range(
    start_date: Union[str, datetime.date], end_date: Union[str, datetime.date]
) -> List[datetime.date]:
    start_date = date_converter(start_date)
    end_date = date_converter(end_date)
    rng_diff = end_date - start_date
    return [start_date + timedelta(days=x) for x in range(0, rng_diff.days + 1)]


def preprocess_inputs(
    dates: List[Union[datetime.date, str]], data: List[Any]
) -> Tuple[List[datetime.date], List[Union[int, Any]]]:
    # Convert any strings to datetime.
    dates = [
        dt.strptime(d, "%Y-%m-%d").date() if isinstance(d, str) else d for d in dates
    ]
    # Strip any datetimes to date.
    dates = [d.date() if isinstance(d, datetime.datetime) else d for d in dates]
    # Sort dates and values by dates.
    sorted_by_date = sorted([*zip(dates, data)], key=lambda x: x[0])
    # Dict mapping date to value.
    data_dict = dict(sorted_by_date)
    # Fill in date range if not complete.
    dates = date_range(list(data_dict.keys())[0], list(data_dict.keys())[-1])
    # Fill in zero for added dates.
    data = [data_dict.get(date, 0) for date in dates]

    return dates, data


def preprocess_month(
    dates: List[datetime.date], data: List[Any], month: Optional[int] = None
) -> Tuple[List[datetime.date], List[Union[int, Any]]]:
    # Set month for filtering
    month = month or dates[0].month
    # Sort dates and values by date.
    sorted_by_date = sorted([*zip(dates, data)], key=lambda x: x[0])

    if len(set([d.year for d in dates if d.month == month])) != 1:
        raise ValueError(
            f"More than one year with month {month} in input 'dates'. "
            f"Month '{month}' is not uniquely defined."
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
        first_date = datetime.date(year, month, 1)
        last_date = datetime.date(year, month, last_day)
        dates = date_range(first_date, last_date)
        # Fill in zero for added dates.
        data = [data_dict.get(date, 0) for date in dates]
    else:
        dates = list(data_dict.keys())
        data = list(data_dict.values())

    return dates, data
