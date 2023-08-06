def setattr(source, name, value):
    """set attribute."""
    import builtins

    builtins.setattr(source, name, value)
    return source


def getitem(source, index):
    """Get items from a array."""

    if isinstance(source, dict):
        result = source[index]
    else:
        # list or array
        if type(index) in (int, float):
            index = [index]
        result = [source[i] for i in index]
        if len(result) == 1:
            result = result[0]
    results = (result,)
    return results


def setitem(source, index, value):
    """Set items value for a array."""
    if type(index) in (int, float):
        index = [index]
    index = [int(i) for i in index]
    if isinstance(source, list):
        for i in index:
            source[i] = value[i]
    else:
        source[index] = value
    return source


def index(source, value):
    """To find index of the all occurrence of an element in
    a given Python List or numpy array."""
    import numpy as np

    if isinstance(source, list):
        source = np.array(source)
    results = (np.where(source == value)[0],)
    return results
