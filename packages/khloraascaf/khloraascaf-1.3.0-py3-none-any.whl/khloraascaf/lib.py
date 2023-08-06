# -*- coding=utf-8 -*-

"""Khloraa scaffolding library."""

from typing import Literal


# DOCU main documentation and docstrings
# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
RegionCodeT = Literal[0, 1, 2]

RegionIDT = Literal['sc', 'ir', 'dr']


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                 Region Codes                                 #
# ---------------------------------------------------------------------------- #
SC_CODE: RegionCodeT = 0
"""Single copy region integer code."""

IR_CODE: RegionCodeT = 1
"""Inverted repeat integer code."""

DR_CODE: RegionCodeT = 2
"""Direct repeat integer code."""

# ---------------------------------------------------------------------------- #
#                              Region Identifiers                              #
# ---------------------------------------------------------------------------- #
SC_REGION_ID: RegionIDT = 'sc'
"""Single copy region identifier."""

IR_REGION_ID: RegionIDT = 'ir'
"""Inverted repeat identifier."""

DR_REGION_ID: RegionIDT = 'dr'
"""Direct repeat identifier."""

# ---------------------------------------------------------------------------- #
#                       Region Codes From To Identifiers                       #
# ---------------------------------------------------------------------------- #
REGION_CODE_TO_ID: tuple[RegionIDT, RegionIDT, RegionIDT] = (
    SC_REGION_ID, IR_REGION_ID, DR_REGION_ID,
)
REGION_ID_TO_CODE: dict[RegionIDT, RegionCodeT] = {
    SC_REGION_ID: SC_CODE,
    IR_REGION_ID: IR_CODE,
    DR_REGION_ID: DR_CODE,
}
