'''
    pyCoDa init script
'''

__title__ = "pyCoDaMath"
__author__ = "Christian Brinch"
__email__ = "cbri@food.dtu.dk"
__copyright__ = "Copyright 2019 C. Brinch"
__version__ = 1.0
__all__ = ['pycoda', 'extra', 'plot', 'pca']

from . import pycoda, pca
pycoda.init()
