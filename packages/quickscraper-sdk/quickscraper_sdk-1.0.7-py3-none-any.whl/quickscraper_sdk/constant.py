import os


BASE_URL = os.environ.get('QS_BASE_URL') or 'https://api.quickscraper.co/'
VERSION = '1.0.7'


# from importlib.metadata import version
# VERSION = version('quickscraper-sdk')
# Not working this approach with pytest, so version is defined statically
