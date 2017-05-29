import os, sys, platform
from os.path import expanduser
#
py_vinfo = sys.version_info
if type(sys.version_info) == type(()):
    print 'This python is not 2.7 version'
    print 'Use Python 2.7'
    assert False
#
ZONE_UNIT_KM = 0.5
#
path_merge = lambda path1, path2 : os.path.join(path1, path2)
#
tc_data = path_merge(os.path.dirname(os.path.realpath(__file__)), 'z_data')
geo_dpath = path_merge(tc_data, 'geo')