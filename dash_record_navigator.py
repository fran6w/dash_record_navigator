import dash_html_components as html


class RecordNavigator:
    """
# Dash Record Navigator

Advanced Dash widget to navigate within records with 4 buttons:
    *fast_backward*, *step_backward*, *step_forward*, *fast_forward*.
Go-between Dash layout, callbacks and model.

See: [https://github.com/plotly/dash](https://github.com/plotly/dash)

## RecordNavigator()

### Argument

- `name`: dedicated name for each RecordNavigator instance.

### Keyword arguments

- `limit`: number of displayed records, default value: 10
- `ascending`: bool, default value: True
    - True: records are first to last
    - False: records are last to first
- `titles`: tuple with 4 tooltips for each button, default value: `('first', 'previous', 'next', 'last')`, reverse if ascending is False

## Class attributes
Integers representing which button has been clicked:

- FIRST
- PREVIOUS
- NEXT
- LAST

## Attributes

Dash id for each button:

- `fast_backward_id`
- `step_backward_id`
- `step_forward_id`
- `fast_forward_id`

## Methods

- `html()`
    - generates 4 buttons as part of Dash layout
    - method to be used in Dash layout definition

- `which_button(fast_backward_ts, step_backward_ts, step_forward_ts, fast_forward_ts)`
    - arguments:
        - n_clicks_timestamp of each 4 buttons
    - returns the integer corresponding to which button has been clicked
    - method to be used in Dash callbacks

- `get_bounds(btn, current_state, record_count, limit=None)`
    - arguments:
        - *btn*: integer corresponding to which button has been clicked, see *which_button()* method
        - *current_state*: variable or tuple of variables that are used to select the displayed records. If the current_state differs from the stored one, FIRST is used
        - *record_count*: number of records or callable which returns the number of records. Use integer if it is immediate to compute (e.g., DataFrame: len(df.loc[...]). Use zero argument lambda if computation requires some time (e.g., SQL: `SELECT COUNT(*) FROM (...);`) since it is only used when *btn* is *LAST*.
        - *limit*: keyword argument which overwrites the instance variable *_limit*
    - returns a tuple (limit, offset) which is used to select which records should be displayed
    - names "*limit*" and "*offset*" are related to SQL statements: `"SELECT ... LIMIT {} OFFSET {};".format(limit, offset)`
    - For DataFrame: `df.loc[...].iloc[offset:offset+limit]`
    - method to be used in Dash callbacks

## Examples

See use examples in `app_dataframe.py` and `app_database.py` files:

- `html()` is used in app layout
- `which_button()` is used in callback
- `get_bounds()` is used further in callback

## License
For the Python code: same as plotly/dash (MIT).
    """

    FIRST = 0
    PREVIOUS = 1
    NEXT = 2
    LAST = 3
    TITLES = ('first', 'previous', 'next', 'last')

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

    def html(self):
        div = html.Div([
                html.A(html.I(className="fa fa-fast-backward"),
                       id=self.fast_backward_id,
                       n_clicks_timestamp=0,
                       title=self._titles[0],
                       style={'margin-right': '20px',
                              'text-decoration': 'none'}),
                html.A(html.I(className="fa fa-step-backward"),
                       id=self.step_backward_id,
                       n_clicks_timestamp=-1,
                       title=self._titles[1],
                       style={'margin-right': '20px',
                              'text-decoration': 'none'}),
                html.A(html.I(className="fa fa-step-forward"),
                       id=self.step_forward_id,
                       n_clicks_timestamp=-1,
                       title=self._titles[2],
                       style={'margin-right': '20px',
                              'text-decoration': 'none'}),
                html.A(html.I(className="fa fa-fast-forward"),
                       id=self.fast_forward_id,
                       n_clicks_timestamp=-1,
                       title=self._titles[3],
                       style={'text-decoration': 'none'})
              ],
             style={'margin-top': '5px'})
        return div

    def which_button(self, fast_backward_ts, step_backward_ts, step_forward_ts, fast_forward_ts):
        btn_list = [(fast_backward_ts, self.FIRST),
                    (step_backward_ts, self.PREVIOUS),
                    (step_forward_ts, self.NEXT),
                    (fast_forward_ts, self.LAST)]
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
