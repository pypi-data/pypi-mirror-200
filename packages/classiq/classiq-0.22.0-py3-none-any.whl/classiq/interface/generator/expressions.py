from typing import Dict

import pydantic
from sympy import Expr, sympify

from classiq.interface.generator.function_params import validate_expression_str
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)


class Expression(HashablePydanticBaseModel):
    expr: str

    _sympy_expr: Expr = pydantic.PrivateAttr()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._sympy_expr = sympify(self.expr)

    def is_int_constant(self) -> bool:
        return self._sympy_expr.is_Integer

    def to_int_value(self) -> int:
        if not self.is_int_constant():
            raise ValueError("Expression is not an integer constant")
        return int(self._sympy_expr)

    def is_numeric_constant(self) -> bool:
        return self._sympy_expr.is_Number

    def to_float_value(self) -> float:
        if not self.is_numeric_constant():
            raise ValueError("Expression is not a number constant")
        return float(self._sympy_expr)

    def substitute(self, substitutions: Dict[str, "Expression"]) -> "Expression":
        return Expression(
            expr=str(
                self._sympy_expr.subs(
                    {
                        name: expression._sympy_expr
                        for name, expression in substitutions.items()
                    }
                )
            )
        )

    @pydantic.validator("expr")
    def validate_expression(cls, expr: str) -> str:
        validate_expression_str("expression", expr)
        return expr

    class Config:
        frozen = True
