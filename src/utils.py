def loop_recursive(d, callback):
    """Loops over all values in a dictionary recursively."""
    if(callback(d)): return d
    
    for value in d.values():
        if callback(value): return value
        
        # loop over values if value is a dict
        if isinstance(value, dict):
            result = loop_recursive(value, callback)
            if result: return result
            
        # loop over children if value is a list
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    result = loop_recursive(item, callback)
                    if result: return result
            
    return None