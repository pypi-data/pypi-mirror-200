# Function Logger and Timer
This is a Python package that provides decorators for logging function execution and timing function execution.

## Installation
You can install the package using pip:
'pip install log_exc_decorator'

## Usage
### Logging function execution
To log function execution, use the elog decorator. Here's an example:

`from log_exc_decorator import elog`

```python
@elog
def my_function():
    # your code here
    pass
```
This will log the start and end of my_function, as well as any exceptions that may occur.

### Timing function execution
To time function execution, use the timeit decorator. Here's an example:

```python
from log_exc_decorator import timeit

@timeit
def my_function():
    # your code here
    pass
```
This will time how long it takes to execute my_function and log the elapsed time.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
Apache