# Dash Record Navigator

Advanced Dash widget to navigate within records with 4 buttons:
    *fast_backward*, *step_backward*, *step_forward*, *fast_forward*

![layout](widget.png)

See: [https://github.com/plotly/dash](https://github.com/plotly/dash)

## 1. RecordNavigator(name, limit, ascending, titles)

### 1.1 Argument

- `name`: name of each `RecordNavigator` instance.

### 1.2 Keyword arguments

- `limit`: number of displayed records, default value: 10
- `ascending`: bool, default value: True
    - True: records are first to last
    - False: records are last to first
- `titles`: tuple with 4 tooltips for each button, default value:
    - `('first', 'previous', 'next', 'last')`
    - reverse if ascending is False

## 2. Methods

- html(color)`
    - generates 4 buttons as part of Dash layout
    - to be used in Dash layout definition
    - keyword arguments:
        - `color`: HTML color for buttons
- `which_button(fast_backward_ts, step_backward_ts, step_forward_ts, fast_forward_ts, extra_ts=-1)`
    - arguments: `n_clicks_timestamp` of each 4 buttons
    - keyword argument extra_ts: `n_clicks_timestamp` of some other button
    - returns the integer corresponding to which button has been clicked last or `None` if extra button
    - to be used in Dash callbacks with `Input({'index': ALL, 'role': ALL, 'name': <name of RecordNavigator instance>}, 'n_clicks_timestamp')`
- `get_bounds(btn, current_state, record_count, limit=None)`
    - arguments:
        - `btn`: integer corresponding to which button has been clicked, see *which_button()* method
        - `current_state`: variable or tuple of variables that are used to select the displayed records;
        if the current state differs from the stored one, FIRST is used
        - `record_count`: number of records or callable which returns the number of records:
        use an integer if it is immediate to compute (e.g., DataFrame: `len(df.loc[...])`;
        use a zero argument lambda if computation requires some time
        (e.g., SQL: `SELECT COUNT(*) FROM (...);`)
        - `limit`: keyword argument which overwrites the instance variable `_limit`
    - returns a tuple `(limit, offset)` which is used to select which records should be displayed
    - names "*limit*" and "*offset*" are related to SQL statements:
    `"SELECT ... LIMIT {} OFFSET {};".format(limit, offset)`
    - for DataFrame: `df.loc[...].iloc[offset:offset+limit]`
    - to be used in Dash callbacks

## Examples

See examples in `app_dataframe.py` and `app_database.py` files

## Version
0.1.1

## License
For the Python code: same as plotly/dash (MIT).
