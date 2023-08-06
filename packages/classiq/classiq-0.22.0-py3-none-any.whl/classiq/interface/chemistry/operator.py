from functools import reduce
from typing import Any, Dict, List, Tuple

import numpy as np
import pydantic
from more_itertools import all_equal

from classiq.interface.generator.complex_type import Complex
from classiq.interface.helpers.custom_pydantic_types import (
    PydanticPauliList,
    PydanticPauliMonomial,
    PydanticPauliMonomialStr,
)
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)
from classiq.interface.helpers.versioned_model import VersionedModel


class PauliOperator(HashablePydanticBaseModel, VersionedModel):
    """
    Specification of a Pauli sum operator.
    """

    pauli_list: PydanticPauliList = pydantic.Field(
        description="A list of tuples each containing a pauli string comprised of I,X,Y,Z characters and a complex coefficient; for example [('IZ', 0.1), ('XY', 0.2)].",
    )
    is_hermitian: bool = pydantic.Field(default=False)

    def show(self) -> str:
        if self.is_hermitian:
            return "\n".join(
                f"{summand[1].real:+.3f} * {summand[0]}" for summand in self.pauli_list
            )
        return "\n".join(
            f"+({summand[1]:+.3f}) * {summand[0]}" for summand in self.pauli_list
        )

    @pydantic.validator("pauli_list", each_item=True)
    def _validate_pauli_monomials(
        cls, monomial: Tuple[PydanticPauliMonomialStr, complex]
    ) -> Tuple[PydanticPauliMonomialStr, complex]:
        _PauliMonomialLengthValidator(  # type: ignore[call-arg]
            monomial=monomial
        )  # Validate the length of the monomial.
        parsed_monomial = _PauliMonomialParser(string=monomial[0], coeff=monomial[1])  # type: ignore[call-arg]
        return (parsed_monomial.string, parsed_monomial.coeff)

    @pydantic.validator("pauli_list")
    def _validate_pauli_list(cls, pauli_list: PydanticPauliList) -> PydanticPauliList:
        if not all_equal(len(summand[0]) for summand in pauli_list):
            raise ValueError("Pauli strings have incompatible lengths.")
        return pauli_list

    @pydantic.root_validator
    def _validate_hermitianity(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        pauli_list = values.get("pauli_list", [])
        values["is_hermitian"] = all(
            np.isclose(complex(summand[1]).real, summand[1]) for summand in pauli_list
        )
        if values.get("is_hermitian", False):
            values["pauli_list"] = [
                (summand[0], complex(summand[1].real)) for summand in pauli_list
            ]
        return values

    def __mul__(self, coefficient: complex) -> "PauliOperator":
        multiplied_ising = [
            (monomial[0], monomial[1] * coefficient) for monomial in self.pauli_list
        ]
        return self.__class__(pauli_list=multiplied_ising)

    @property
    def num_qubits(self) -> int:
        return len(self.pauli_list[0][0])

    def to_matrix(self) -> np.ndarray:
        return sum(
            summand[1] * to_pauli_matrix(summand[0]) for summand in self.pauli_list
        )  # type: ignore[return-value]

    @staticmethod
    def _extend_pauli_string(
        pauli_string: PydanticPauliMonomialStr, num_extra_qubits: int
    ) -> PydanticPauliMonomialStr:
        return "I" * num_extra_qubits + pauli_string

    def extend(self, num_extra_qubits: int) -> "PauliOperator":
        new_pauli_list = [
            (self._extend_pauli_string(pauli_string, num_extra_qubits), coeff)
            for (pauli_string, coeff) in self.pauli_list
        ]
        return self.copy(update={"pauli_list": new_pauli_list}, deep=True)

    class Config:
        frozen = True


# This class validates the length of a monomial.
@pydantic.dataclasses.dataclass
class _PauliMonomialLengthValidator:
    monomial: PydanticPauliMonomial


@pydantic.dataclasses.dataclass
class _PauliMonomialParser:
    string: PydanticPauliMonomialStr
    coeff: Complex


_PAULI_MATRICES = {
    "I": np.array([[1, 0], [0, 1]]),
    "X": np.array([[0, 1], [1, 0]]),
    "Y": np.array([[0, -1j], [1j, 0]]),
    "Z": np.array([[1, 0], [0, -1]]),
}


def to_pauli_matrix(pauli_op: PydanticPauliMonomialStr) -> np.ndarray:
    return reduce(np.kron, [_PAULI_MATRICES[pauli] for pauli in reversed(pauli_op)])


class PauliOperators(VersionedModel):
    operators: List[PauliOperator]
