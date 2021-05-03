![July](figs/july.png)
# July
A small library for creating beautiful heatmaps of daily data. 

### Features
- Get rid of all the overhead and matplotlib tweaking every time you want to plot data in calendar format.
- Generate GitHub activity overview-like plots of your daily data.
- Plot daily data in calendar format (month or year).
- Automatic handling of missing dates in input date range.
- `July` is not pandas centric. In fact, it doesn't use pandas at all, nor does it require you to. Only numpy arrays and native Python data structures are used internally.
- Though pd.DateTimeIndex and pd.Timestamp are both accepted as the `dates` input. They are both subclassing `datetime`, and will be stripped down to `date`.


### Install
```
$ pip install july
```

### Usage
```
import july
```

### Why "July"?
The obvious names like `calplot` and `calendarplot` were all already taken by similar packages, and thus, the quest for a new name began. 

The reasoning was roughly as follows:
- **Q**: What is this package doing?
- **A**: It creates heatmaps of daily data, grouped by month and year.
- **Q**: Heat... month... year... Every year is the hottest year ever nowadays, but what is the hottest month?
- **A**: :sparkles: :sparkles: :sparkles: July :sparkles: :sparkles: :sparkles:  

Also, July is my favourite month by a light year. It's the only month when the weather in Oslo gets close to being consistently bearable.

### TODO:
- Add examples and example figures to README.
- Fix slight misalignment of plot and cbar when `date_grid` and `colourbar` are used in conjunction.
- Add some sort of config file/dict/class to make plots more customisable.
- Add wrapper around calendar plot to simply plot calendar for a given month.
- Add and enforce flake8.
- Add Makefile.
- Set up CI.
- Document everything...
- Add type hints. Consider adding mypy to enforce them.
