"""Initialize the security_service subpackage of pade_python package"""

# allow absolute import from the root folder
# whatever its name is.
import sys  # don't remove required for error handling
import os

# Import from sibling directory ..\security_service
OS_NAME = os.name

sys.path.append("..")

if OS_NAME.lower() == "nt":
    print("windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))

import pade_python.security_service.security_core