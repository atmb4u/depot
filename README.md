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


## License

3-clause BSD License


