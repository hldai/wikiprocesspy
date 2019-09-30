from platform import platform
from os.path import join

if platform().startswith('Windows'):
    PLATFORM = 'Windows'
    RES_DIR = 'd:/data/res'
else:
    PLATFORM = 'Linux'
    RES_DIR = '/home/hldai/data/res'
