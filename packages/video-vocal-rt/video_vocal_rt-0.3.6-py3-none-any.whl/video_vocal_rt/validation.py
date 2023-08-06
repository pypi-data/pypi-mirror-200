import os

def is_dir(dir_path: str) -> str:
    """
    Determines if a given string represents a valid directory path.

    Args:
        dir_path (str): The directory path to be checked.

    Returns:
        str: The original directory path string if it is valid.

    Raises:
        ValueError: If the provided string does not represent a valid directory path.
    """
    if not os.path.isdir(dir_path):
        raise ValueError(f"{dir_path} is not a valid directory path")
    
    return dir_path


def str_to_int(value: str, positive: bool = True) -> int:
    """
    Converts a given string to an integer and enforces that it is positive if specified.

    Args:
        value (str): The string to be converted to an integer.
        positive (bool, optional): If True (default), the resulting integer must be positive. 

    Returns:
        int: The resulting integer.

    Raises:
        ValueError: If the provided string cannot be converted to an integer or if the resulting 
            integer is not positive when it should be.
    """
    try: 
        value = int(value)  
    except ValueError:
        raise ValueError(f"{value} is not a valid integer")
    
    if positive and value <= 0:
        raise ValueError(f"{value} is not a positive integer")
    
    return value