# -*- coding=utf-8 -*-

"""Scaffolding module."""


from collections.abc import Callable
from pathlib import Path
from typing import Optional, Type

from pulp import LpProblem, LpStatusOptimal

from khloraascaf.exceptions import (
    CombineScaffoldingError,
    RepeatScaffoldingError,
    ScaffoldingError,
    SingleCopyScaffoldingError,
    UnfeasibleDR,
    UnfeasibleIR,
    UnfeasibleSC,
    WrongRegionCode,
)
from khloraascaf.ilp.pulp_max_dirf import intersected_dirf_model
from khloraascaf.ilp.pulp_max_invf import nested_invf_model
from khloraascaf.ilp.pulp_max_presscore import best_presscore_model
from khloraascaf.ilp.pulp_to_solver import (
    fmt_solver_log_name,
    solve_pulp_problem,
)
from khloraascaf.ilp.pulp_var_db import (
    PuLPVarDirFModel,
    PuLPVarInvFModel,
    PuLPVarModelT,
)
from khloraascaf.inputs import (
    INSTANCE_NAME_DEF,
    MULT_UPB_DEF,
    OUTDEBUG_DEF,
    OUTDIR_DEF,
    PRESSCORE_UPB_DEF,
    SOLVER_CBC,
    IdCT,
    MultT,
    PresScoreT,
)
from khloraascaf.lib import (
    DR_CODE,
    IR_CODE,
    REGION_CODE_TO_ID,
    SC_CODE,
    RegionCodeT,
)
from khloraascaf.multiplied_doubled_contig_graph import (
    MDCGraph,
    MDCGraphIDContainer,
    OccOrCT,
    first_forward_occurence,
    mdcg_with_id_from_input_files,
)
from khloraascaf.outputs import (
    fmt_contigs_of_regions_filename,
    fmt_map_of_regions_filename,
    generate_output_directory,
    write_contigs_of_regions,
    write_map_of_regions,
)
from khloraascaf.result import ScaffoldingResult, path_to_regions
from khloraascaf.run_metadata import (
    bump_debug_to_yaml,
    bump_io_config_to_yaml,
    bump_solutions_to_yaml,
)
from khloraascaf.utils_debug import (
    fmt_found_repeated_fragments_filename,
    fmt_vertices_of_regions_filename,
    write_found_repeated_fragments,
    write_vertices_of_regions,
)


# DOCU constants, functions
# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
# FIXME use constant args something like that
__HEIGHT_LIM = 2
__OTHER_REPEAT_CODE = {IR_CODE: DR_CODE, DR_CODE: IR_CODE}


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                        From User's Files Main Function                       #
# ---------------------------------------------------------------------------- #
# pylint: disable=too-many-arguments
def scaffolding(
        contig_attrs: Path,
        contig_links: Path,
        contig_starter: IdCT,
        multiplicity_upperbound: MultT = MULT_UPB_DEF,
        presence_score_upperbound: PresScoreT = PRESSCORE_UPB_DEF,
        solver: str = SOLVER_CBC,
        outdir: Path = OUTDIR_DEF,
        instance_name: str = INSTANCE_NAME_DEF,
        debug: bool = OUTDEBUG_DEF) -> Path:
    """Computes the scaffolding.

    Parameters
    ----------
    contig_attrs : Path
        Contigs' attributes file path
    contig_links : Path
        Contigs' links file path
    contig_starter : IdCT
        Starter contig's identifier
    multiplicity_upperbound : MultT, optional
        Multiplicities upper bound, by default `MULT_UPB_DEF`
    presence_score_upperbound : PresScoreT, optional
        Presence score upper bound, by default `PRESSCORE_UPB_DEF`
    solver : str, optional
        MILP solver to use ('cbc' or 'gurobi'), by default `SOLVER_CBC`
    outdir : Path, optional
        Output directory path, by default `OUTDIR_DEF`
    instance_name : str, optional
        Instance name, by default `INSTANCE_NAME_DEF`
    debug : bool, optional
        Output debug or not, by default False

    Returns
    -------
    Path
        Result output directory path

    Raises
    ------
    ScaffoldingError
        If the scaffolding fails

    Notes
    -----
    A uniquely named directory will be created to store the result files.
    """
    # ------------------------------------------------------------------------ #
    # Manage options
    # ------------------------------------------------------------------------ #
    # REFACTOR find less confusable name for outdir / output_dir / outdir_gen...
    outdir_gen = outdir / generate_output_directory(instance_name)
    outdir_gen.mkdir()

    bump_io_config_to_yaml(
        outdir_gen, contig_attrs, contig_links, contig_starter,
        multiplicity_upperbound, presence_score_upperbound,
        solver, outdir, instance_name, debug,
    )

    # ------------------------------------------------------------------------ #
    # Generate scaffolding data from input files
    # ------------------------------------------------------------------------ #
    # DOCU verify docstring
    mdcg, id_container = mdcg_with_id_from_input_files(
        contig_attrs, contig_links,
        multiplicity_upperbound=multiplicity_upperbound,
        presence_score_upperbound=presence_score_upperbound,
    )

    # ------------------------------------------------------------------------ #
    # Find the solutions
    # ------------------------------------------------------------------------ #
    # TODO what to do if several optimal solutions?
    #   * solution should be a list of results?
    #   * how to tell which results was selected?
    #   * metadata on the outputs (human reading)?
    try:
        solutions = combine_scaffolding_problems(
            mdcg, first_forward_occurence(
                id_container.contig_to_vertex(contig_starter)),
            solver, outdir_gen, instance_name,
            debug=debug,
        )
    except CombineScaffoldingError as exc:
        # TODO logging exception
        raise ScaffoldingError(outdir_gen) from exc

    if not solutions:
        # TODO print 'No solution found'
        return outdir

    for solution in solutions:
        # TODO print 'n solutions found'
        __solution_scaffolding(
            solution, outdir_gen, id_container, debug, instance_name)
    # TOTEST output directory returned (especially when auto-generated)
    return outdir_gen


# ---------------------------------------------------------------------------- #
#                             Combining Scaffolding                            #
# ---------------------------------------------------------------------------- #
def combine_scaffolding_problems(mdcg: MDCGraph, starter_vertex: OccOrCT,
                                 solver: str, outdir: Path, instance_name: str,
                                 debug: bool = OUTDEBUG_DEF) -> (
        tuple[ScaffoldingResult, ...]):
    """Find a priority between the optimisation problems.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    solver : str
        MILP solver to use ('cbc' or 'gurobi')
    outdir : Path
        Output directory path
    instance_name : str
        Instance's name
    debug : bool, optional
        Output debug or not, by default False

    Returns
    -------
    tuple of ScaffoldingResult
        Best ILP results

    Raises
    ------
    CombineScaffoldingError
        The scaffolding combination has failed

    Warnings
    --------
    Files in the output directory can be erased.
    """
    # Si list vide
    #   * faire IR
    #       * mettre IR solution
    #   * faire DR
    #       * si opt value
    #           * ==, rajouter
    #           * >, reinitialiser liste avec solution
    #           * <, ne pas mettre
    # Sinon, pour chaque solution
    #   * faire complement (IR <-> DR)
    #       * si opt value
    #           * ==, rajouter
    #           * >, reinitialiser liste avec solution
    #           * <, ne pas mettre
    #
    # Pour l'instant limité par __HEIGHT_LIM
    # ------------------------------------------------------------------------ #
    # Repeat scaffolding
    # ------------------------------------------------------------------------ #
    opti_results: tuple[ScaffoldingResult, ...] = ()
    height = 0
    while not height or (height < __HEIGHT_LIM and opti_results):
        try:
            opti_results = combine_repeat_scaffolding(
                opti_results, mdcg, starter_vertex,
                solver, outdir, instance_name, debug,
            )
        except RepeatScaffoldingError as exc:
            # TODO logging logging.critical(str(exc))
            raise CombineScaffoldingError() from exc
        height += 1

    # ------------------------------------------------------------------------ #
    # Single copy regions scaffolding
    # ------------------------------------------------------------------------ #
    try:
        opti_results = combine_singlecopy_scaffolding(
            opti_results, mdcg, starter_vertex,
            solver, outdir, instance_name, debug,
        )
    except SingleCopyScaffoldingError as exc:
        # TODO logging exception here
        raise CombineScaffoldingError() from exc

    return opti_results


def combine_repeat_scaffolding(opti_results: tuple[ScaffoldingResult, ...],
                               mdcg: MDCGraph, starter_vertex: OccOrCT,
                               solver: str, outdir: Path,
                               instance_name: str,
                               debug: bool) -> tuple[ScaffoldingResult, ...]:
    """Combine repeat scaffolding.

    Parameters
    ----------
    opti_results : tuple of ScaffoldingResult
        Best scaffolding results
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    solver : str
        Solver to use
    outdir : Path
        Output directory path
    instance_name : str
        Instance name
    debug : bool
        To output debug files or not

    Returns
    -------
    tuple of ScaffoldingResult
        Best scaffolding results

    Raises
    ------
    RepeatScaffoldingError
        If one of the repeat solve fails during the combination
    """
    best_opt_value = 0.0
    new_results: list[ScaffoldingResult] = []

    for opti_result in (opti_results if opti_results else (None,)):

        l_scaffolding_to_apply: list[RegionCodeT] = (
            [IR_CODE, DR_CODE] if opti_result is None
            else [__OTHER_REPEAT_CODE[opti_result.last_ilp()]]
        )

        for region_code in l_scaffolding_to_apply:
            try:
                result = scaffolding_region(
                    region_code, mdcg, starter_vertex,
                    solver, outdir, instance_name,
                    fix_result=opti_result,
                    debug=debug,
                )
            except (UnfeasibleIR, UnfeasibleDR) as exc:
                # TODO logging print(exc, file=sys.stderr)
                raise RepeatScaffoldingError() from exc

            if result.opt_value() > best_opt_value:
                best_opt_value = result.opt_value()
                new_results = [result]
            elif result.opt_value() == best_opt_value > 0:
                new_results.append(result)

    return tuple(new_results) if new_results else opti_results


def combine_singlecopy_scaffolding(opti_results: tuple[ScaffoldingResult, ...],
                                   mdcg: MDCGraph, starter_vertex: OccOrCT,
                                   solver: str, outdir: Path,
                                   instance_name: str, debug: bool) -> (
        tuple[ScaffoldingResult, ...]):
    """Combine best previous results with single copy scaffolding.

    Parameters
    ----------
    opti_results : tuple of ScaffoldingResult
        Best scaffolding results
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    solver : str
        Solver to use
    outdir : Path
        Output directory path
    instance_name : str
        Instance name
    debug : bool
        To output debug files or not

    Returns
    -------
    tuple of ScaffoldingResult
        Best scaffolding results

    Raises
    ------
    SingleCopyScaffoldingError
        One of the single copy region scaffolding has failed
    """
    best_opt_value = 0.0
    new_results = []
    for opti_result in (opti_results if opti_results else (None,)):
        try:
            result = scaffolding_region(
                SC_CODE, mdcg, starter_vertex,
                solver, outdir, instance_name,
                fix_result=opti_result,
                debug=debug,
            )
        except UnfeasibleSC as exc:
            # TODO logging here print(exc, file=sys.stderr)
            raise SingleCopyScaffoldingError() from exc

        if result.opt_value() > best_opt_value:
            best_opt_value = result.opt_value()
            new_results = [result]
        elif result.opt_value() == best_opt_value:
            new_results.append(result)

    return tuple(new_results)


# ---------------------------------------------------------------------------- #
#                         Specific Regions Scaffolding                         #
# ---------------------------------------------------------------------------- #
def scaffolding_region(region_code: RegionCodeT,
                       mdcg: MDCGraph, starter_vertex: OccOrCT,
                       solver: str, outdir: Path, instance_name: str,
                       fix_result: Optional[ScaffoldingResult] = None,
                       debug: bool = OUTDEBUG_DEF) -> ScaffoldingResult:
    """Scaffolding of a specific region.

    Parameters
    ----------
    region_code : RegionCodeT
        Code of the region to scaffold
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    solver : str
        MILP solver to use ('cbc' or 'gurobi')
    outdir : Path
        Output directory path
    instance_name : str
        Instance's name
    fix_result : ScaffoldingResult, optional
        Previous scaffolding result, by default None
    debug : bool, optional
        Output debug or not, by default False

    Returns
    -------
    ScaffoldingResult
        Scaffolding result

    Raises
    ------
    WrongRegionCode
        The given code of the regions is wrong
    UnfeasibleIR
        The combinatorial problem is unfeasible
    UnfeasibleDR
        The combinatorial problem is unfeasible
    UnfeasibleSC
        The combinatorial problem is unfeasible

    Warnings
    --------
    Files in the output directory can be erased.
    """
    # ------------------------------------------------------------------------ #
    # ILP codes
    # ------------------------------------------------------------------------ #
    if fix_result is not None:
        ilp_codes = tuple(fix_result.ilp_codes()) + (region_code,)
    else:
        ilp_codes = (region_code,)

    # ------------------------------------------------------------------------ #
    # Instantiate functions and exceptions
    # ------------------------------------------------------------------------ #
    model_fn: Callable[..., tuple[LpProblem, PuLPVarModelT]]
    unfeasible_exc: Type[Exception]
    if region_code == IR_CODE:
        model_fn = nested_invf_model
        unfeasible_exc = UnfeasibleIR
    elif region_code == DR_CODE:
        model_fn = intersected_dirf_model
        unfeasible_exc = UnfeasibleDR
    elif region_code == SC_CODE:
        model_fn = best_presscore_model
        unfeasible_exc = UnfeasibleSC
    else:
        raise WrongRegionCode(region_code)

    prob, var = model_fn(mdcg, starter_vertex, fix_result=fix_result)

    log_path = None
    if debug:
        log_path = outdir / fmt_solver_log_name(
            solver, instance_name,
            (REGION_CODE_TO_ID[code] for code in ilp_codes),
        )
    solve_pulp_problem(prob, solver, log_path=log_path)

    if prob.status != LpStatusOptimal:
        if debug:
            bump_debug_to_yaml(
                outdir, instance_name, ilp_codes,
                starter_vertex, prob.status, None,
            )
        raise unfeasible_exc(prob.status, ilp_codes)

    result = path_to_regions(mdcg, starter_vertex, ilp_codes,
                             prob, var, fix_result)

    # ------------------------------------------------------------------------ #
    # Debug
    # ------------------------------------------------------------------------ #
    if debug:
        __region_scaffolding_debug(instance_name, outdir, var, result)
        bump_debug_to_yaml(
            outdir, instance_name, result.ilp_codes(),
            starter_vertex, result.status(), result.opt_value(),
        )
    return result


def __region_scaffolding_debug(instance_name: str, outdir: Path,
                               var: PuLPVarModelT, result: ScaffoldingResult):
    """Write debug files and metadata.

    Parameters
    ----------
    instance_name : str
        Instance name
    outdir : Path
        Output directory path
    result : ScaffoldingResult
        Scaffolding result
    """
    # ------------------------------------------------------------------------ #
    # The order of vertices for each region
    # ------------------------------------------------------------------------ #
    vertices_of_regions_path = (
        outdir / fmt_vertices_of_regions_filename(
            instance_name,
            (REGION_CODE_TO_ID[code] for code in result.ilp_codes()),
        )
    )
    write_vertices_of_regions(result, vertices_of_regions_path)

    # ------------------------------------------------------------------------ #
    # The map of regions (debug version)
    # ------------------------------------------------------------------------ #
    map_of_regions_path = (
        outdir / fmt_map_of_regions_filename(
            instance_name,
            (REGION_CODE_TO_ID[code] for code in result.ilp_codes()),
        )
    )
    write_map_of_regions(result, map_of_regions_path)

    # ------------------------------------------------------------------------ #
    # The repeated fragments
    # ------------------------------------------------------------------------ #
    if isinstance(var, (PuLPVarInvFModel, PuLPVarDirFModel)):
        repeat_fragments_path = (
            outdir / fmt_found_repeated_fragments_filename(
                instance_name,
                (REGION_CODE_TO_ID[code] for code in result.ilp_codes()),
            )
        )
        write_found_repeated_fragments(var, repeat_fragments_path)


def __solution_scaffolding(solution: ScaffoldingResult, outdir_gen: Path,
                           id_container: MDCGraphIDContainer, debug: bool,
                           instance_name: str):
    """Output the solution in files and in YAML.

    Parameters
    ----------
    solution : ScaffoldingResult
        Scaffolding result
    outdir_gen : Path
        Generated output directory path
    id_container : MDCGraphIDContainer
        Container connecting contig identifiers and vertex indices
    debug : bool
        Debugging option
    instance_name : str
        Instance name
    """
    # -------------------------------------------------------------------- #
    # Write the solution in files
    # -------------------------------------------------------------------- #
    #
    # The order of oriented contigs for each region
    #
    contigs_of_regions_path = (
        outdir_gen / fmt_contigs_of_regions_filename(
            instance_name,
            (REGION_CODE_TO_ID[code] for code in solution.ilp_codes()),
        )
    )
    write_contigs_of_regions(
        solution, contigs_of_regions_path,
        id_container=id_container,
    )
    #
    # The order of oriented regions
    #
    if not debug:  # already generated if debug is True
        map_of_regions_path = (
            outdir_gen / fmt_map_of_regions_filename(
                instance_name,
                (REGION_CODE_TO_ID[code] for code in solution.ilp_codes()),
            )
        )
        write_map_of_regions(solution, map_of_regions_path)

    bump_solutions_to_yaml(outdir_gen, instance_name, solution.ilp_codes())
