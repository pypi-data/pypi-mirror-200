import importlib.resources

__version__ = '1.0.2'

with importlib.resources.path('maphis', '__main__.py') as p:
    MAPHIS_PATH = p.parent