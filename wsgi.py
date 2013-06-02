import os
import sys

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

# Add working directory to paths
sys.path.append(os.path.dirname(__file__))

import bottle
import bridgebeam
# ... build or import your bottle application here ...
# Do NOT use bottle.run() with mod_wsgi

from bridgebeam import application
