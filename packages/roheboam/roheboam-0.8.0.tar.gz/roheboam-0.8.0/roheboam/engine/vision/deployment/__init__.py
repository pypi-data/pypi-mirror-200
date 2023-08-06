from .mlflow import *
from .mlflow import lookup as mlflow_lookup
from .seldon import *
from .seldon import lookup as seldon_lookup

lookup = {**seldon_lookup, **mlflow_lookup}
