# coding: utf-8
__author__ = "Francis Wolinski"

import dash_html_components as html
from dash.dependencies import Input


class RecordNavigator:
    """
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

- `html(color)`
    - generates 4 buttons as part of Dash layout
    - to be used in Dash layout definition
    - keyword arguments:
        - `color`: HTML color for buttons

- `inputs()`
    - generates 4 input statements for each button
    - to be used in Dash callback definition

- `which_button(fast_backward_ts, step_backward_ts, step_forward_ts, fast_forward_ts, extra_ts)`
    - arguments: `n_clicks_timestamp` of each 4 buttons
    - extra_ts: `n_clicks_timestamp` of some other button
    - returns the integer corresponding to which button has been clicked last, or None if other button
    - to be used in Dash callbacks

- `get_bounds(btn, current_state, record_count, limit=None)`
    - arguments:
        - `btn`: integer corresponding to which button has been clicked, see *which_button()* method
        - `current_state`: variable or tuple of variables that are used to select the displayed records;
        if the current state differs from the stored one, FIRST is used
        - `record_count`: number of records or callable which returns the number of records:
        use integer if it is immediate to compute (e.g., DataFrame: len(df.loc[...]);
        use zero argument lambda if computation requires some time
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
    """

    FIRST = 0
    PREVIOUS = 1
    NEXT = 2
    LAST = 3
    TITLES = ('first', 'previous', 'next', 'last')
    # Font Awesome buttons
    FA_BUTTONS = ('fast-backward', 'step-backward', 'step-forward', 'fast-forward')
    # Initial button timestamps
    TIMESTAMPS = (0, -1, -1, -1)

    def __init__(self, name, limit=10, ascending=True, titles=None):
        self._name = name
        self.fast_backward_id = f'btn-fast-backward-{self._name}'
        self.step_backward_id = f'btn-step-backward-{self._name}'
        self.step_forward_id = f'btn-step-forward-{self._name}'
        self.fast_forward_id = f'btn-fast-forward-{self._name}'

        self._limit = limit
        self._offset = 0
        self._state = None
        self._titles = (self.TITLES if ascending else self.TITLES[::-1]) if titles is None else titles

    def html(self, color='#00BFFF'):
        children = [
                    html.A(html.I(className=f"fa fa-{btn}"),
                           id=self._btn_id(btn),
                           n_clicks_timestamp=ts,
                           title=title,
                           style={'margin-right': '20px',
                                  'text-decoration': 'none',
                                  'color': color})
                    for (btn, ts, title) in zip(self.FA_BUTTONS, self.TIMESTAMPS, self._titles)]
        div = html.Div(children,
                       style={'margin-top': '5px'})
        return div

    def inputs(self):
        inputs = [Input(self._btn_id(btn), 'n_clicks_timestamp') for btn in self.FA_BUTTONS]
        return inputs

    def which_button(self, fast_backward_ts, step_backward_ts, step_forward_ts, fast_forward_ts, extra_ts=-1):
        btn_list = [(fast_backward_ts, self.FIRST),
                    (step_backward_ts, self.PREVIOUS),
                    (step_forward_ts, self.NEXT),
                    (fast_forward_ts, self.LAST),
                    (extra_ts, None)]
        _, btn = max(btn_list, key=lambda x: int(x[0]))

        return btn

    def get_bounds(self, btn, current_state, record_count, limit=None):
        if limit is None:
            limit = self._limit
        # fast-backward
        if (btn == self.FIRST) or btn is None or (current_state != self._state):
            self._offset = 0
        # step-backward
        elif btn == self.PREVIOUS:
            self._offset -= limit
        # step-forward
        elif btn == self.NEXT:
            self._offset += limit
        # fast-forward
        elif btn == self.LAST:
            self._offset = (record_count() if callable(record_count) else record_count) - limit

        if self._offset < 0:
            self._offset = 0

        self._state = current_state

        return limit, self._offset

    def _btn_id(self, btn):
        return f'btn-{btn}-{self._name}'
