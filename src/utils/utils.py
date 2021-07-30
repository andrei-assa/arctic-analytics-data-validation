"""General utilities for this repository."""
from pathlib import Path

def get_project_root():
    """
    Returns the project root directory.

    Returns:
        [type]: [description]
    """
    return str((Path(__file__)).parent.parent.absolute())