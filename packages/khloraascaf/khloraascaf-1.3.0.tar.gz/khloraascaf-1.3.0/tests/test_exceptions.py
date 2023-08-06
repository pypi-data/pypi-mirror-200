# -*- coding=utf-8 -*-

"""Unit testing for assembly graph."""

# pylint: disable=compare-to-zero, missing-raises-doc

from pathlib import Path

from khloraascaf.exceptions import (
    CombineScaffoldingError,
    NotACircuit,
    RepeatScaffoldingError,
    ScaffoldingError,
    SingleCopyScaffoldingError,
    UnfeasibleDR,
    UnfeasibleIR,
    UnfeasibleSC,
    WrongRegionCode,
    WrongSolverName,
)
from khloraascaf.lib import IR_CODE, SC_CODE


# ============================================================================ #
#                                TEST FUNCTIONS                                #
# ============================================================================ #
def test_scaffolding_error():
    """Test ScaffoldingError exception."""
    exc = ScaffoldingError(Path('./jaaj'))
    assert str(exc) == (
        'Scaffolding fails\n'
        '\tSee output directory: jaaj'
    )


def test_repeat_scaffolding_error():
    """Test RepeatScaffoldingError exception."""
    exc = RepeatScaffoldingError()
    assert str(exc) == 'Repeat scaffolding has failed'


def test_singlecopy_scaffolding_error():
    """Test SingleCopyScaffoldingError exception."""
    exc = SingleCopyScaffoldingError()
    assert str(exc) == 'Single copy scaffolding has failed'


def test_combine_scaffolding_error():
    """Test CombineScaffoldingError exception."""
    exc = CombineScaffoldingError()
    assert str(exc) == 'The scaffolding combination has failed'


def test_wrong_region_code():
    """Test WrongRegionCode exception."""
    exc = WrongRegionCode(IR_CODE)
    assert str(exc) == 'The region code 1 is not correct'


def test_wrong_solver_name():
    """Test WrongSolverName exception."""
    exc = WrongSolverName('wrong_solver')
    assert str(exc) == 'The solver name wrong_solver is not correct'


def test_unfeasible_ir():
    """Test UnfeasibleIR exception."""
    exc = UnfeasibleIR(
        -1, (IR_CODE, SC_CODE),
    )
    assert str(exc) == (
        'The Find the best inverted repeats problem is unfeasible:\n'
        '\t* ILP codes: ir-sc\n'
        '\t* Status: Infeasible'
    )


def test_unfeasible_dr():
    """Test UnfeasibleDR exception."""
    exc = UnfeasibleDR(
        -1, (IR_CODE, SC_CODE),
    )
    assert str(exc) == (
        'The Find the best direct repeats problem is unfeasible:\n'
        '\t* ILP codes: ir-sc\n'
        '\t* Status: Infeasible'
    )


def test_unfeasible_sc():
    """Test UnfeasibleSC exception."""
    exc = UnfeasibleSC(
        -1, (IR_CODE, SC_CODE),
    )
    assert str(exc) == (
        'The Find the best single copy regions problem is unfeasible:\n'
        '\t* ILP codes: ir-sc\n'
        '\t* Status: Infeasible'
    )


def test_not_a_circuit():
    """Test NotACircuit exception."""
    exc = NotACircuit()
    assert str(exc) == 'The found path is not a circuit'
