import keyword
from typing import Set

from classiq.interface.generator.arith import arithmetic_expression_parser

SUPPORTED_VAR_NAMES_REG = "[A-Za-z][A-Za-z0-9]*"

SUPPORTED_FUNC_NAMES: Set[str] = {"or", "and"}.union(
    arithmetic_expression_parser.SUPPORTED_FUNC_NAMES
)
FORBIDDEN_LITERALS: Set[str] = set(keyword.kwlist) - SUPPORTED_FUNC_NAMES
