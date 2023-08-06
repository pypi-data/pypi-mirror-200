def hms_to_s(hms):
    """
    convert a duration expressed in hours, minutes, seconds into seconds
    
    arguments:
    - hms: duration (h, m, s) - tuple
        - h: hours - int | float
        - m: minutes - int | float
        - s: seconds - int | float
    
    returns:
    - s: duration in seconds - type: float
    or
    - None

    examples:
    >>> s = hms_to_s((1., 23., 45.))
    """
    
    if not isinstance(hms, tuple):
        return None
    elif not len(hms) == 3:
        return None
    else:
        h, m, s = hms
    
    if not (isinstance(h, (int, float)) and isinstance(m, (int, float)) and isinstance(s, (int, float))):
        return None
    elif not (0 <= h and 0 <= m and 0 <= s):
            return None
    else:
         return float(h*3600. + m*60. + s)