from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __import__('pkg_resources').declare_namespace(__name__)
