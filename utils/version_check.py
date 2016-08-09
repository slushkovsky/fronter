import sys
import warnings
import logging

if sys.version_info < (3, 0) :
    logging.error("Sorry, requires Python 3.5")
    exit(1)

if sys.version_info < (3, 5) :
    warnings.warn("We recomend you Python 3.5")