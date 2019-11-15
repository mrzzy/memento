#
# Memento
# Backend
# Tests
#

import os
import sys
import unittest

from gevent import monkey; monkey.patch_all()

# hack to get relative imports to work
sys.path.append("..")

from backend.tests import *

if __name__ == "__main__":
    unittest.main()
