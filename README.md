# Depot v0.9
## Shared variables for parallel python processes

## How to use
1. Run the server 
```
depot start
```
2. Import DepotClient and use set and get to manipulate variables, which are accesible across the processes.
```
>>> from depot import DepotClient
>>> d_client = DepotClient()
>>> d_client.set("key", "value")
>>> d_client.get("key")
value
```

## Installation

```
$ pip install python-depot
```
