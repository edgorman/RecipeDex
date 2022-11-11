
import json


class AssertionWarning(Warning):
    ...


def dict_diff(x, y):
    return "Differing keys and values: " + json.dumps({k: (x[k], y[k]) for k in x.keys() if x[k] != y[k]})
