import sys

PY2 = False
PY3 = False

if sys.version_info[0] == 2:
    PY2 = True
elif sys.version_info[0] == 3:
    PY3 = True
