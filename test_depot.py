__author__ = 'atm'
from depot import DepotClient

d = DepotClient()
d.set("old", "World")
val = d.get("new")