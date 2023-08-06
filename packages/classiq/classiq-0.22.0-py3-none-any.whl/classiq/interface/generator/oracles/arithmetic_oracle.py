import ast
import re
from typing import Dict, List, Sequence

import numexpr  # type: ignore[import]
import numpy as np
import pydantic

from classiq.interface.generator.arith import number_utils
from classiq.interface.generator.arith.arithmetic import Arithmetic
from classiq.interface.generator.arith.arithmetic_expression_template import (
    ArithmeticExpressionTemplate,
    UncomputationMethods,
)
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.generated_circuit_data import IOQubitMapping
from classiq.interface.generator.oracles.oracle_template import (
    ArithmeticIODict,
    OracleTemplate,
)

from classiq.exceptions import ClassiqArithmeticError

_ARITHMETIC_EXPRESSION_RESULT_NAME: str = "expression_result"


class ArithmeticOracle(OracleTemplate[float], ArithmeticExpressionTemplate):
    uncomputation_method: UncomputationMethods = UncomputationMethods.optimized

    @pydantic.validator("expression")
    def _validate_compare_expression(cls, expression: str) -> str:
        ast_obj = ast.parse(expression, "", "eval")
        if not isinstance(ast_obj, ast.Expression):
            raise ValueError("Must be an expression")
        if not isinstance(ast_obj.body, (ast.Compare, ast.BoolOp)):
            raise ValueError("Must be a comparison expression")
        return expression

    def get_arithmetic_expression_params(self) -> Arithmetic:
        return Arithmetic(
            max_fraction_places=self.max_fraction_places,
            expression=self.expression,
            definitions=self.definitions,
            uncomputation_method=self.uncomputation_method,
            qubit_count=self.qubit_count,
            simplify=self.simplify,
            output_name=_ARITHMETIC_EXPRESSION_RESULT_NAME,
            target=RegisterUserInput(size=1),
            inputs_to_save=set(self.definitions.keys()),
        )

    def _get_register_transputs(self) -> ArithmeticIODict:
        return {
            name: register
            for name, register in self.definitions.items()
            if name in self._get_literal_set()
            and isinstance(register, RegisterUserInput)
        }

    def is_good_state(self, state: str, indices: IOQubitMapping) -> bool:
        expression = self._simplify_negations_of_boolean_variables(
            expression=self.expression, input_definitions=self.inputs
        )
        input_values = self.state_to_problem_result(state, indices=indices)
        for var_name, value in input_values.items():
            expression = re.sub(r"\b" + var_name + r"\b", str(value), expression)
        try:
            return bool(numexpr.evaluate(expression).item())
        except TypeError:
            raise ClassiqArithmeticError(
                f"Cannot evaluate expression {expression}"
            ) from None

    @staticmethod
    def _simplify_negations_of_boolean_variables(
        expression: str, input_definitions: Dict[str, RegisterUserInput]
    ) -> str:
        for var_name in input_definitions:
            if getattr(input_definitions[var_name], "size", 0) == 1:
                expression = re.sub(
                    rf"~\s*{var_name}\b", f"(1 - {var_name})", expression
                )
        return expression

    def state_to_problem_result(
        self, state: str, indices: IOQubitMapping
    ) -> Dict[str, float]:
        input_values: Dict[str, float] = {}
        state_as_array = np.array(list(state))
        for var_name, var_indices in indices.items():
            var = self.inputs[var_name]
            var_string = "".join(
                state_as_array[sorted(_reverse_endianness(var_indices, len(state)))]
            )
            var_value = number_utils.binary_to_float_or_int(
                var_string, var.fraction_places, var.is_signed
            )
            input_values[var_name] = var_value
        return input_values


def _reverse_endianness(indices: Sequence[int], state_length: int) -> List[int]:
    return [state_length - 1 - index for index in indices]
