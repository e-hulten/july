![July](https://github.com/e-hulten/july/blob/master/figs/july.png?raw=true)
# July
A small library for creating beautiful heatmaps of daily data. 

### Features
- Get rid of the eternal matplotlib tweaking every time you want to plot data in proper calendar format.
- Generate GitHub activity overview-like heatmaps of your daily data.
- Automatic handling of missing dates in input date range.
- `July` does not rely only pandas (though it accepts it). Only numpy arrays and native Python data structures are used internally.
- Accepted date formats: `datetime.datetime`, `datetime.date`, `str`, `pd.DatetimeIndex`


### Install
```
$ pip install july
```

### Usage
```
import numpy as np
import matplotlib.pyplot as plt
import july
from july.utils import date_range

dates = date_range("2020-01-01", "2020-12-31")
data = np.random.randint(0, 14, len(dates))
```
```
# GitHub Activity like plot (for someone with consistently random work patterns).
july.heatmap(dates, data, title='Github Activity', cmap="github")
```
![GitHub heatmap](https://github.com/e-hulten/july/blob/master/examples/heatmap_github.jpg?raw=true)
```
# Here, 'osl_df' is a pandas df. 
july.heatmap(osl_df.date, osl_df.temp, cmap="golden", colorbar=True, title="Average temperatures: Oslo , Norway")
```
![Golden heatmap](https://github.com/e-hulten/july/blob/master/examples/pandas_oslo_temperature_plot.jpg?raw=true)
```
# More exhaustive example using useless, but pretty colours.
july.heatmap(dates=dates, 
             data=data, 
             cmap='Pastel1',
             month_grid=True, 
             horizontal=True,
             value_label=False,
             date_label=False,
             weekday_label=True,
             month_label=True, 
             year_label=True,
             colorbar=False,
             fontfamily="sans-serif",
             fontsize=10,
             title=None,
             titlesize=14,
             dpi=100)
```
![Pastel heatmap](https://github.com/e-hulten/july/blob/master/examples/heatmap_pastel.jpg?raw=true)

```
# Month plot with dates.
july.month_plot(dates, data, month=5, date_label=True, ax=axes[0])
# Month plot with values.
july.month_plot(dates, data, month=5, value_label=True, ax=axes[1])
```
![Month plot](https://github.com/e-hulten/july/blob/master/examples/month_plot.jpg?raw=true)
```
# Calendar plot. 
july.calendar_plot(dates, data)
```
![Calendar plot](https://github.com/e-hulten/july/blob/master/examples/calendar_plot.jpg?raw=true)


### Why "July"?
**Main reason:** All the obvious names like `calplot`, `calmap`, and `calendarplot` were all already taken by similar packages. This had me looking for a new name that wouldn't get easily mixed up with the other packages.

The reasoning was roughly as follows: 
 - `Heatmap` + `month` → `Hot month` → `July` :sparkles:

Also, as a summer loving person stuck in the Northern hemisphere, July is my favourite month by a light year.

### TODO:
- Fix slight misalignment of plot and cbar when `date_grid` and `colorbar` are used in conjunction.
- Document everything...
- Add type hints. 
- Add automatic date handling for strings of more types than just `YYYY-MM-DD`.
