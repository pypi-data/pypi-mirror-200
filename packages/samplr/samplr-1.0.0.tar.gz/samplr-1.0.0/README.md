# ***S A M P L R***
`@samplr` is a tiny decorator that provides options for returning a subset of items from a list. It also prints useful information about this sampling process to the terminal for debugging.

# Installation
Install `samplr` using pip:

```python
pip install samplr
```

# Usage
To use, decorate a function that returns a list with `@samplr()`. For example:

```python
from samplr import samplr

@samplr(count=3)
def get_data():
    # ... code that returns a list of 10 items of data ...
```

`get_data()` will now return a list containing just the first 3 items of the original return list, instead of all 100.

The arguments of `samplr()` are:

- `count` (optional, default `'all'`): The number of items to return. This can be an integer or the string 'all'.
    - If `count` is a positive integer, the decorated function's returned list will be that length.

    - If `count` is 'all', all items will be returned.

    - If `count` is a negative integer that many items will be ommited from the returned list.

    *Also note:*

    - If `count` > len(original_list), count = 'all'

    - If `count` < -len(original_list), count = 0

- `sample_type` (optional, default `'head'`): The method for selecting the subset of items. The available options are:

    - `'head'`: Select the first *`count`* items in the list.

    - `'tail'`: Select the last *`count`* items in the list.

    - `'random'`: Sample a random subset of *`count`* items from the list.

- `expand` (optional, default `True`): Whether to expand each item in the console print output. Helps with the readability of deeply nested objects.

- `info` (optional, default `True`): Whether to output to the console additional information about the sampling process.



# Examples
1. An example of using `@samplr` to select a random subset of 3 items from a list returned by a function:

```python
from samplr import samplr

@samplr(count=3, sample_type='random')
def get_data():
    return [
        {'name': 'Alice', 'age': 32},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 41},
        {'name': 'David', 'age': 19},
        {'name': 'Eve', 'age': 56},
        {'name': 'Frank', 'age': 28},
        {'name': 'Grace', 'age': 39},
        {'name': 'Heidi', 'age': 22},
        {'name': 'Isaac', 'age': 47},
        {'name': 'Jen', 'age': 31},
    ]

sampled_data = get_data()
```

This will return a list of items and output something like this to the terminal:

```python
◆   ◇   ◆  S A M P L R  ◆   ◇   ◆

◇ @samplr(count = 3, sample_type = random)
  get_data()
◆ items returned: 3/10

◇ 0: : {
    "name": "Alice",
    "age": 32
}
◆ 3: : {
    "name": "David",
    "age": 19
}
◇ 4: : {
    "name": "Eve",
    "age": 56
}

◆   ◇   ◆  end  ◆   ◇   ◆
```

*Note the enumeration in the printout shows each item's index in the original list.*

---
2. An example of using `@samplr` to exclude the last 2 items (with `expand` and `info` set to `False`):

```python
@samplr(count=-2, sample_type='tail', expand=False, info=False)
def get_data():
    return ["zero", "one", "two", "three", "four", "five", "six"]
```
This returns a list of length 5, and outputs a shorter statement to the terminal:

```python
◆ 0: : "zero"
◇ 1: : "one"
◆ 2: : "two"
◆ 3: : "three"
◆ 4: : "four"
```

---