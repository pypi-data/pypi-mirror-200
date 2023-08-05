"""
This python based project help generating visio drawing from the excel database.
Tested on MS-Visio Professional 2013. other version support is not tested. it may or may not work as described.

Requirements
--------------------
Database: update your data in Excel.   Two tabs are necessary, one with devices details, another with connectivity details.

MS-Visio: to generate the drawing.

Stencils: [optional] folder from where project can find visio stencils.

"""

__ver__ = "0.0.10"

# ------------------------------------------------------------------------------

from .stencils import get_list_of_stencils
from .database import DeviceData, CableMatrixData
from .gui import UserForm
from .entities import ItemObjects, Connectors
from .visio import VisioObject

from .oper import DFGen
from .devices import AdevDevices
from .cablings import ADevCablings
from .general import get_physical_if_up, get_physical_if_relevants
from .general import get_patterns, update_pattern
from .pyVig import pyVig, pyVig_gui
# ------------------------------------------------------------------------------

