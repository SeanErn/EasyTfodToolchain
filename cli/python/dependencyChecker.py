from sys import exit
from platform import python_version_tuple
from pkg_resources import get_distribution

def package_installed() -> bool:
    try:
       pkg_resources.get_distribution(package_name)
       return True
    except pkg_resources.DistributionNotFound:
       return False

def meets_min_requirements() -> bool:
    if (int(python_version_tuple()[1]) >= 11) and (get_distribution("textual")):
        return True
    else:
        return False