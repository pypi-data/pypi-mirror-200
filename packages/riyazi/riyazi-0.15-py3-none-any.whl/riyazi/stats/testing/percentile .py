def percentile(sorted_list, percent, key=lambda x: x):
    """Find the percentile of a sorted list of values.

    Arguments
    ---------
    sorted_list : list
        A sorted (ascending) list of values.
    percent : float
        A float value from 0.0 to 1.0.
    key : function, optional
        An optional function to compute a value from each element of N.

    Returns
    -------
    float
        The desired percentile of the value list.

    Examples
    --------
    >>> sorted_list = [4,6,8,9,11]
    >>> percentile(sorted_list, 0.4)
    7.0
    >>> percentile(sorted_list, 0.44)
    8.0
    >>> percentile(sorted_list, 0.6)
    8.5
    >>> percentile(sorted_list, 0.99)
    11.0
    >>> percentile(sorted_list, 1)
    11.0
    >>> percentile(sorted_list, 0)
    4.0
    """
    if not sorted_list:
        return None
    if percent == 1:
        return float(sorted_list[-1])
    if percent == 0:
        return float(sorted_list[0])
    n = len(sorted_list)
    i = percent * n
    if ceil(i) == i:
        i = int(i)
        return (sorted_list[i-1] + sorted_list[i]) / 2
    return float(sorted_list[ceil(i)-1])


