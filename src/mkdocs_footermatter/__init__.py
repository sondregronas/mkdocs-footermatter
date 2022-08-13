from pkg_resources import DistributionNotFound, get_distribution

from mkdocs_footermatter.plugin import FootermatterPlugin

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    pass
