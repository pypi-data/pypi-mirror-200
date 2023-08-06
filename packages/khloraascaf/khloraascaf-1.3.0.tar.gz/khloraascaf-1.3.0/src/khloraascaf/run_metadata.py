# -*- coding=utf-8 -*-

"""Module for the RunMetadata class."""

from collections.abc import Iterable
from pathlib import Path
from typing import Optional

from pulp import LpStatus, LpStatusOptimal
from revsymg.index_lib import IndexT
from yaml import dump  # type: ignore

from khloraascaf.cli import (
    ARG_CONTIG_ATTRS,
    ARG_CONTIG_LINKS,
    ARG_CONTIG_STARTER,
    OPT_INSTANCE_NAME,
    OPT_MULT_UPB,
    OPT_OUTDEBUG,
    OPT_OUTDIR,
    OPT_PRESSCORE_UPB,
    OPT_SOLVER,
)
from khloraascaf.inputs import STR_ORIENT, IdCT, MultT, PresScoreT
from khloraascaf.lib import (
    DR_REGION_ID,
    IR_REGION_ID,
    REGION_CODE_TO_ID,
    RegionCodeT,
)
from khloraascaf.multiplied_doubled_contig_graph import (
    CIND_IND,
    COCC_IND,
    COR_IND,
    OccOrCT,
)
from khloraascaf.outputs import (
    CONTIGS_OF_REGIONS_PREFIX,
    MAP_OF_REGIONS_PREFIX,
    ORIENT_INT_STR,
    fmt_contigs_of_regions_filename,
    fmt_map_of_regions_filename,
)
from khloraascaf.utils_debug import (
    FOUND_REPFRAG_PREFIX,
    VERTICES_OF_REGIONS_PREFIX,
    fmt_found_repeated_fragments_filename,
    fmt_vertices_of_regions_filename,
)


# DOCU metadata run YAML all
# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                     Files                                    #
# ---------------------------------------------------------------------------- #
# DOCU run metadata file
YAML_EXT = 'yaml'
"""Extension for YAML files"""

IO_CONFIG_METADATA_PREFIX = 'io_config'
"""Prefix of the IO config metadata file name."""

SOLUTIONS_METADATA_PREFIX = 'solutions'
"""Prefix of the solutions metadata file name."""

DEBUG_METADATA_PREFIX = 'all_scaffolding'
"""Prefix of the all scaffolding metadata file name."""

# ---------------------------------------------------------------------------- #
#                                     YAML                                     #
# ---------------------------------------------------------------------------- #
KEY_ILP_COMBINATION = 'ilp_combination'
KEY_STARTER_VERTEX = 'starter_vertex'
KEY_OPT_VALUE = 'opt_value'
KEY_ILP_STATUS = 'ilp_status'


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                               String Formatter                               #
# ---------------------------------------------------------------------------- #
def vertex_to_str(vertex: OccOrCT) -> str:
    """Transform a vertex to a string.

    Parameters
    ----------
    vertex : OccOrCT
        Vertex

    Returns
    -------
    str
        String representation
    """
    return (
        f'{vertex[CIND_IND]}'
        f'\t{ORIENT_INT_STR[vertex[COR_IND]]}'
        f'\t{vertex[COCC_IND]}'
    )


def str_to_vertex(vertex_str: str) -> OccOrCT:
    """Transform a vertex string to the vertex.

    Parameters
    ----------
    vertex_str : str
        Vertex string

    Returns
    -------
    OccOrCT
        Vertex
    """
    str_list = vertex_str.split('\t')
    return (
        IndexT(str_list[CIND_IND]),
        STR_ORIENT[str_list[COR_IND]],  # type: ignore
        IndexT(str_list[COCC_IND]),
    )


# ---------------------------------------------------------------------------- #
#                                 YAML Outputs                                 #
# ---------------------------------------------------------------------------- #
# pylint: disable=too-many-arguments
def bump_io_config_to_yaml(output_dir: Path, contig_attrs: Path,
                           contig_links: Path, contig_starter: IdCT,
                           mult_upb: MultT, presscore_upb: PresScoreT,
                           solver: str, outdir: Path, instance_name: str,
                           debug: bool):
    """Add input metadata.

    Parameters
    ----------
    output_dir : Path
        YAML file output directory path
    contig_attrs : Path
        Contig attributes file path
    contig_links : Path
        Contig links file path
    contig_starter : IdCT
        Starter contig's identifier
    mult_upb : MultT
        Multiplicities upper bound
    presscore_upb : PresScoreT
        Presence score upper bound
    solver : str
        MILP solver to use
    outdir : Path
        Output directory path
    instance_name : str
        Instance name
    debug : bool
        Output debug or not
    """
    yaml_path = output_dir / fmt_io_config_metadata_filename()
    with open(yaml_path, 'a', encoding='utf-8') as yaml_out:
        yaml_out.write(
            dump(
                {
                    ARG_CONTIG_ATTRS: str(contig_attrs),
                    ARG_CONTIG_LINKS: str(contig_links),
                    ARG_CONTIG_STARTER: contig_starter,
                    OPT_MULT_UPB: mult_upb,
                    OPT_PRESSCORE_UPB: presscore_upb,
                    OPT_SOLVER: solver,
                    OPT_OUTDIR: str(outdir),
                    OPT_INSTANCE_NAME: instance_name,
                    OPT_OUTDEBUG: debug,
                },
                sort_keys=False,
            ),
        )


def fmt_io_config_metadata_filename() -> str:
    """Return IO config metadata file name.

    Returns
    -------
    str
        File name
    """
    return f'{IO_CONFIG_METADATA_PREFIX}.{YAML_EXT}'


def bump_solutions_to_yaml(output_dir: Path, instance_name: str,
                           ilp_codes: Iterable[RegionCodeT]):
    """Append debug metadata to the YAML file.

    Parameters
    ----------
    output_dir : Path
        YAML file output directory path
    instance_name : str
        Instance name
    ilp_codes : iterable of RegionCodeT
        ILP codes
    """
    yaml_path = output_dir / fmt_solutions_metadata_filename()

    ilp_ids = [REGION_CODE_TO_ID[code] for code in ilp_codes]
    with open(yaml_path, 'a', encoding='utf-8') as yaml_out:
        yaml_out.write(
            dump([
                {
                    KEY_ILP_COMBINATION: ilp_ids,
                    CONTIGS_OF_REGIONS_PREFIX: fmt_contigs_of_regions_filename(
                        instance_name, ilp_ids,
                    ),
                    MAP_OF_REGIONS_PREFIX: fmt_map_of_regions_filename(
                        instance_name, ilp_ids,
                    ),
                },
            ],
                sort_keys=False,
            ),
        )


def fmt_solutions_metadata_filename() -> str:
    """Return solutionsg metadata file name.

    Returns
    -------
    str
        File name
    """
    return f'{SOLUTIONS_METADATA_PREFIX}.{YAML_EXT}'


# pylint: disable=too-many-arguments
def bump_debug_to_yaml(output_dir: Path, instance_name: str,
                       ilp_codes: Iterable[RegionCodeT],
                       starter_vertex: OccOrCT, status: int,
                       opt_value: Optional[float]):
    """Append debug metadata to the YAML file.

    Parameters
    ----------
    output_dir : Path
        YAML file output directory path
    instance_name : str
        Instance name
    ilp_codes : iterable of RegionCodeT
        ILP codes
    starter_vertex : OccOrCT
        Starter vertex
    status : int
        ILP status code
    opt_value : optional float
        ILP optimal value if exists else None
    """
    ilp_ids = [REGION_CODE_TO_ID[code] for code in ilp_codes]
    dict_debug = {
        KEY_ILP_COMBINATION: ilp_ids,
        KEY_STARTER_VERTEX: vertex_to_str(starter_vertex),
        KEY_ILP_STATUS: LpStatus[status],
    }
    if status == LpStatusOptimal:
        assert opt_value is not None
        dict_debug.update(
            {
                KEY_OPT_VALUE: opt_value,
                VERTICES_OF_REGIONS_PREFIX: fmt_vertices_of_regions_filename(
                    instance_name, ilp_ids,
                ),
                MAP_OF_REGIONS_PREFIX: fmt_map_of_regions_filename(
                    instance_name, ilp_ids,
                ),
            },
        )
        if ilp_ids[-1] in (IR_REGION_ID, DR_REGION_ID):
            dict_debug.update(
                {
                    FOUND_REPFRAG_PREFIX: fmt_found_repeated_fragments_filename(
                        instance_name, ilp_ids,
                    ),
                },
            )

    yaml_path = output_dir / fmt_debug_metadata_filename()
    with open(yaml_path, 'a', encoding='utf-8') as yaml_out:
        yaml_out.write(dump([dict_debug], sort_keys=False))


def fmt_debug_metadata_filename() -> str:
    """Return debug metadata file name.

    Returns
    -------
    str
        File name
    """
    return f'{DEBUG_METADATA_PREFIX}.{YAML_EXT}'
