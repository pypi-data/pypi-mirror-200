import abc
from typing import Dict, Generic, List, Optional, TypeVar

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import ArithmeticIODict, FunctionParams
from classiq.interface.generator.generated_circuit_data import IOQubitMapping

ProblemResultType = TypeVar("ProblemResultType")


class OracleTemplate(abc.ABC, FunctionParams, Generic[ProblemResultType]):
    def get_power_order(self) -> Optional[int]:
        return 2

    @abc.abstractmethod
    def _get_register_transputs(self) -> ArithmeticIODict:
        pass

    def _create_ios(self) -> None:
        self._inputs = self._get_register_transputs()
        self._outputs = {**self._inputs}

    @abc.abstractmethod
    def is_good_state(self, state: str, indices: IOQubitMapping) -> bool:
        pass

    @abc.abstractmethod
    def state_to_problem_result(
        self, state: str, indices: IOQubitMapping
    ) -> Dict[str, ProblemResultType]:
        pass

    def variables(self) -> List[RegisterUserInput]:
        return list(self._inputs.values())
