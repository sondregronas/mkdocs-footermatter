from importlib.metadata import version, PackageNotFoundError

from mkdocs_footermatter.plugin import FootermatterPlugin

try:
    __version__ = version('mkdocs-footermatter')
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass