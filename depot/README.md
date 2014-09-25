# Depot v1.0
## Shared variables for parallel python processes


## Installation

```
$ pip install python-depot
```

## Usage
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
3. Use the same key from any process while the server is running, and it persists the value saved from the purticular instance.

__depot__ can be considered as a pure python implementation of __redis__, using multiprocessing.Manager

## License

3-clause BSD License


