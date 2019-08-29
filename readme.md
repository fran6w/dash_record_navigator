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
- `titles`: tuple with 4 tiptools for each button, default value: `('first', 'previous', 'next', 'last')`, reverse if ascending is False

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
		- *btn*: integer corresponding to which button has been clicked, see *get_bounds()* method
		- *current_state*: variable or tuple of variables that are used to select the displayed records. If the current_state differs from the stored one, FIRST is used
		- *record_count*: number of records or callable which returns the number of records. Use integer if it is immediate to compute (e.g., DataFrame: `len(df.loc[...])`. Use zero argument lambda if computation requires some time (e.g., SQL: `SELECT COUNT(*) FROM (...);`) since it is only used when *btn* is *LAST*.
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
