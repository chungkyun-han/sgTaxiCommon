import os, sys, platform
from os.path import expanduser
#
py_vinfo = sys.version_info
if type(sys.version_info) == type(()):
    print 'This python is not 2.7 version'
    assert False
#
ZONE_UNIT_KM = 0.5

tc_data = '%s/%s' % (os.path.dirname(os.path.realpath(__file__)), 'z_data')