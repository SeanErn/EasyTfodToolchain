from sys import exit
from platform import python_version_tuple
import pkg_resources

def package_installed(package_name: str) -> bool:
    try:
       pkg_resources.get_distribution(package_name)
       return True
    except pkg_resources.DistributionNotFound:
       return False

def meets_min_requirements() -> bool:
    if (int(python_version_tuple()[1]) >= 11) and package_installed("textual"):
        return True
    else:
        return False