import calendar
import datetime
from datetime import datetime as dt
from datetime import timedelta
from typing import Union, List, Any, Tuple, Optional


def date_converter(date: Union[str, datetime.date, datetime.datetime]) -> datetime.date:
    """Convert input date to datetime.date format.

    Args:
        date: Date to be converted.
    Returns:
        Converted date in datetime.date format.

    Raises:
        TypeError: If input date is not type string, datetime.date, or
            datetime.datetime.
    """
    if isinstance(date, str):
        return dt.strptime(date, "%Y-%m-%d").date()
    elif isinstance(date, datetime.datetime):
        return date.date()
    elif isinstance(date, datetime.date):
        # Check this last, as isinstance(<datetime object>, datetime.date) is True.
        return date
    else:
        raise TypeError(
            "Expected 'date' to be type: [str, datetime.date, datetime.datetime]. "
            f"Got: {type(date)}."
        )


def date_range(
    start_date: Union[str, datetime.date, datetime.datetime],
    end_date: Union[str, datetime.date, datetime.datetime],
) -> List[datetime.date]:
    """Create rate of datetime.dates from start_date and end_date.

    Args:
        start_date: First date of date range.
        end_date: Last date of date range (inclusive).
    Returns:
        List of all dates in range [start_date, end_date].
    """
    start_date = date_converter(start_date)
    end_date = date_converter(end_date)
    rng_diff = end_date - start_date
    return [start_date + timedelta(days=x) for x in range(0, rng_diff.days + 1)]


def preprocess_inputs(
    dates: List[Union[str, datetime.date, datetime.datetime]], data: List[Any]
) -> Tuple[List[datetime.date], List[Any]]:
    """Preprocess input dates and input data. Incomplete date range in 'dates'
    will be filled in with missing dates. The corresponding elements in 'data' will
    be filled in with zeros.

    Args:
        dates: List (/np.array/pd.Series) of dates.
        data: List of corresponding values.
    Returns:
        dates_preprocessed: Sorted and completed list of dates in input `dates`.
        data_preprocessed: Data sorted according to input dates.
    """
    # Convert all dates to datetime.date.
    dates = [date_converter(date) for date in dates]
    # Sort dates and values by dates.
    sorted_by_date = sorted([*zip(dates, data)], key=lambda x: x[0])
    # Dict mapping date to value.
    data_dict = dict(sorted_by_date)
    # Fill in date range if not complete.
    dates_preprocessed = date_range(
        list(data_dict.keys())[0], list(data_dict.keys())[-1]
    )  # type: List[datetime.date]
    # Fill in zero for added dates.
    data_preprocessed = [data_dict.get(date, 0) for date in dates_preprocessed]

    return dates_preprocessed, data_preprocessed


def preprocess_month(
    dates: List[Union[str, datetime.date, datetime.datetime]],
    data: List[Any],
    month: Optional[int] = None,
) -> Tuple[List[datetime.date], List[Any]]:
    """Extract and preprocess one month of data from input dates and data.

    Args:
        dates: List (/np.array/pd.Series) of dates.
        data: List of corresponding values.
        month: Which month in the input dates to preprocess. Defaults to the
            month of the first element in dates.
    Returns:
        dates: Preprocessed and filtered dates for the desired month.
        data: Data for the desired month.

    Raises:
        ValueError: If month is not uniquely defined in input dates.
    """
    dates_clean, data_clean = preprocess_inputs(dates, data)
    # Set month for filtering
    month = month or dates_clean[0].month
    # Sort dates and values by date.
    sorted_by_date = sorted([*zip(dates_clean, data_clean)], key=lambda x: x[0])

    if len(set([d.year for d in dates_clean if d.month == month])) != 1:
        raise ValueError(
            f"More than one year with month {month} in input 'dates'. "
            f"Month '{month}' is not uniquely defined."
        )

    # Filter relevant month.
    month_list = [(day, val) for day, val in sorted_by_date if day.month == month]
    # Dict mapping date to value.
    data_dict = dict(month_list)
    # Get the year in question.
    year = list(data_dict.keys())[0].year
    # Get last day of month.
    last_day = calendar.monthrange(year, month)[1]

    # Fill in date range if range is not complete.
    if len(data_dict) != last_day:
        first_date = datetime.date(year, month, 1)
        last_date = datetime.date(year, month, last_day)
        dates_out = date_range(first_date, last_date)
        # Fill in zero for added dates.
        data_out = [data_dict.get(date, 0) for date in dates_out]
    else:
        dates_out = list(data_dict.keys())
        data_out = list(data_dict.values())

    return dates_out, data_out
