# Lucas's Book Balancer

A way to track my finances and also show off some Object-Oriented Programming design

## Goals

1. Favor composition over inheritance while avoiding an over-engineered solution
    - Abstract classes should be structured in a way that modularizes functionality, allowing case-specific logic to be injected without affecting adjacent components
2. Class interface methods should be intuitive and self-sufficient
    - The user should have to directly call as few different methods as possible during runtime

## Usage

1. Add statements in CSV format to each relevant subdirectory of `statements` with a matching naming convention
    - Ex. `YYYY-MM.csv`

2. Adjust config constants in `book_balancer.py` as needed

3. Execute

```
python book_balancer.py
```

## To-Do's

1. Rewrite logic to take advantage of numpy arrays and/or Pandas DataFrames
2. Add comments to each logical block and docstrings where necessary
3. Implement tracking of credits and deposits
4. Simplify dependency hand-off between internal methods
5. Make I/O more agnostic to statement file names
