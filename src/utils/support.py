import sys
import os

# will be used later
def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for development and for PyInstaller.

    Returns the absolute path to a resource.

    - In development mode: Uses the current working directory (assumed to be the project root).
    - In executable mode: Uses sys._MEIPASS, where PyInstaller extracts the bundled files.

    *Note: Made with help of Copilot*
    """
    if hasattr(sys, '_MEIPASS'):  # EXE file, deploying mode
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
    else:  # Development mode
        base_path = os.getcwd()  # Assumes your working directory is set to the project root
    return os.path.normpath(os.path.join(base_path, relative_path))