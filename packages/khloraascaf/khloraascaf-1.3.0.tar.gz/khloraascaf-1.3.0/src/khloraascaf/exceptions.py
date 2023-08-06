# -*- coding=utf-8 -*-

"""Scaffolding exceptions module."""

from collections.abc import Iterable
from pathlib import Path

from pulp import LpStatus

from khloraascaf.lib import REGION_CODE_TO_ID, RegionCodeT


# ============================================================================ #
#                                    CLASSES                                   #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                               Scaffolding Error                              #
# ---------------------------------------------------------------------------- #
class ScaffoldingError(Exception):
    """Scaffolding error exception."""

    def __init__(self, outdir: Path):
        """The Initialiser."""
        super().__init__()
        self.__outdir: Path = outdir

    def __str__(self) -> str:
        """Exception message."""
        return (
            'Scaffolding fails\n'
            f'\tSee output directory: {self.__outdir}'
        )


class RepeatScaffoldingError(Exception):
    """If the repeat scaffolding solving fails during the combination."""

    def __str__(self) -> str:
        """Exception message."""
        return 'Repeat scaffolding has failed'


class SingleCopyScaffoldingError(Exception):
    """If the single copy scaffolding solving fails during the combination."""

    def __str__(self) -> str:
        """Exception message."""
        return 'Single copy scaffolding has failed'


class CombineScaffoldingError(Exception):
    """Scaffolding combination error exception."""

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return 'The scaffolding combination has failed'


# ---------------------------------------------------------------------------- #
#                                 Region Types                                 #
# ---------------------------------------------------------------------------- #
class WrongRegionCode(Exception):
    """Wrong region code exception."""

    def __init__(self, region_code: int):
        """The Initializer."""
        super().__init__()
        self.__region_code = region_code

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return f'The region code {self.__region_code} is not correct'


# ---------------------------------------------------------------------------- #
#                                    Solver                                    #
# ---------------------------------------------------------------------------- #
class WrongSolverName(Exception):
    """Wrong solver name exception."""

    def __init__(self, solver: str):
        """The Initializer."""
        super().__init__()
        self.__solver = solver

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return f'The solver name {self.__solver} is not correct'


# ---------------------------------------------------------------------------- #
#                                Unfeasible ILP                                #
# ---------------------------------------------------------------------------- #
class _UnfeasibleILP(Exception):
    """ILP problem unfeasible exception."""

    _PROBLEM_ID = 'THE PROBLEM'

    def __init__(self, status: int, ilp_codes: Iterable[RegionCodeT]):
        super().__init__()
        self.__status: int = status
        self.__ilp_codes: tuple[RegionCodeT, ...] = tuple(ilp_codes)

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return (
            f'The {self._PROBLEM_ID} problem is unfeasible:\n'
            '\t* ILP codes: '
            + '-'.join(REGION_CODE_TO_ID[code] for code in self.__ilp_codes)
            + '\n'
            f'\t* Status: {LpStatus[self.__status]}'
        )


class UnfeasibleIR(_UnfeasibleILP):
    """IR optimisation problem unfeasible exception."""

    _PROBLEM_ID = 'Find the best inverted repeats'


class UnfeasibleDR(_UnfeasibleILP):
    """DR optimisation problem unfeasible exception."""

    _PROBLEM_ID = 'Find the best direct repeats'


class UnfeasibleSC(_UnfeasibleILP):
    """SC optimisation problem unfeasible exception."""

    _PROBLEM_ID = 'Find the best single copy regions'


# ---------------------------------------------------------------------------- #
#                                 Result Error                                 #
# ---------------------------------------------------------------------------- #
class NotACircuit(Exception):
    """Not a circuit exception."""

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return 'The found path is not a circuit'
