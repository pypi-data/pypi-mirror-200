import abc
from typing import Any, ClassVar, Dict, List, Mapping, Optional, Set, Union

import pydantic

from classiq.interface.generator.function_params import (
    ArithmeticIODict,
    IOName,
    PortDirection,
)
from classiq.interface.generator.functions.classical_type import ClassicalType
from classiq.interface.generator.functions.port_declaration import PortDeclaration
from classiq.interface.helpers.custom_pydantic_types import PydanticFunctionNameStr
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)

from classiq import RegisterUserInput

UNRESOLVED_SIZE = 1000


class FunctionDeclarationList(HashablePydanticBaseModel):
    element_declaration: "FunctionDeclaration" = pydantic.Field(
        description="The expected interface of the quantum function operands"
    )


OperandDeclaration = Union["FunctionDeclaration", FunctionDeclarationList]


class FunctionDeclaration(HashablePydanticBaseModel, abc.ABC):
    """
    Facilitates the creation of a user-defined custom function
    """

    name: PydanticFunctionNameStr = pydantic.Field(
        description="The name of a custom function"
    )

    port_declarations: Dict[IOName, PortDeclaration] = pydantic.Field(
        description="The input and output ports of the function.",
        default_factory=dict,
    )

    param_decls: Dict[str, ClassicalType] = pydantic.Field(default_factory=dict)

    return_type: Optional[ClassicalType] = pydantic.Field(
        description="The type of the classical value that is returned by the function (for classical functions)",
        default=None,
    )

    operand_declarations: Dict[str, OperandDeclaration] = pydantic.Field(
        description="The expected interface of the quantum function operands",
        default_factory=dict,
    )

    BUILTIN_FUNCTION_DECLARATIONS: ClassVar[Dict[str, "FunctionDeclaration"]] = {}

    @property
    def base_operand_declarations(self) -> List["FunctionDeclaration"]:
        return [
            _get_base_declaration(operand_declaration)
            for operand_declaration in self.operand_declarations.values()
        ]

    @property
    def input_set(self) -> Set[IOName]:
        return set(self.inputs.keys())

    @property
    def output_set(self) -> Set[IOName]:
        return set(self.outputs.keys())

    @property
    def inputs(self) -> ArithmeticIODict:
        return _ports_to_registers(self.port_declarations, PortDirection.Input)

    @property
    def outputs(self) -> ArithmeticIODict:
        return _ports_to_registers(self.port_declarations, PortDirection.Output)

    @staticmethod
    def _are_classical_port_declarations(port_declarations: Dict[str, PortDeclaration]):
        return len(port_declarations) == 0

    @property
    def is_classical(self) -> bool:
        return self._are_classical_port_declarations(self.port_declarations)

    def update_logic_flow(
        self, function_dict: Mapping[str, "FunctionDeclaration"]
    ) -> None:
        pass

    @pydantic.validator("name")
    def _validate_name(cls, name: str) -> str:
        validate_name_end_not_newline(name=name)
        return name

    @classmethod
    def _validate_declaration_names(
        cls,
        declarations: Mapping[str, Union[OperandDeclaration, PortDeclaration]],
        declaration_name: str,
    ) -> None:
        if not all(
            [
                name == _get_name(declaration)
                for (name, declaration) in declarations.items()
            ]
        ):
            raise ValueError(
                f"{declaration_name} declaration names should match the keys of their names."
            )

    @pydantic.validator("operand_declarations")
    def _validate_operand_declarations_names(
        cls, operand_declarations: Dict[str, OperandDeclaration]
    ) -> Dict[str, OperandDeclaration]:
        cls._validate_declaration_names(operand_declarations, "Operand")
        return operand_declarations

    @pydantic.validator("port_declarations")
    def _validate_port_declarations_names(
        cls, port_declarations: Dict[IOName, PortDeclaration]
    ) -> Dict[IOName, PortDeclaration]:
        cls._validate_declaration_names(port_declarations, "Port")
        return port_declarations

    @pydantic.root_validator()
    def _validate_params_and_operands_uniqueness(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        operand_declarations = values.get("operand_declarations")
        parameter_declarations = values.get("param_decl")
        if operand_declarations is None or parameter_declarations is None:
            return values
        if len(operand_declarations.keys() & parameter_declarations.keys()):
            raise ValueError(
                "A function's operand and parameter cannot have the same name."
            )
        return values

    @pydantic.root_validator()
    def _validate_return_for_classical(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        port_declarations = values.get("port_declarations")
        if port_declarations is None:
            return values
        if values.get(
            "return_type"
        ) is not None and not cls._are_classical_port_declarations(port_declarations):
            raise ValueError(
                "Only classical functions may return a classical value (and have a return type)."
            )
        return values

    class Config:
        frozen = True
        extra = pydantic.Extra.forbid


def validate_name_end_not_newline(name: str) -> None:
    _new_line = "\n"
    if name.endswith(_new_line):
        raise ValueError("Function name cannot end in a newline character")


def _ports_to_registers(
    port_declarations: Dict[IOName, PortDeclaration], direction: PortDirection
) -> ArithmeticIODict:
    return {
        name: RegisterUserInput(
            name=name,
            size=(
                port_decl.size.to_int_value()
                if port_decl.size.is_int_constant()
                else UNRESOLVED_SIZE
            ),
        )
        for name, port_decl in port_declarations.items()
        if port_decl.direction.includes_port_direction(direction)
    }


def _get_name(declaration: Union[OperandDeclaration, PortDeclaration]) -> str:
    return (
        declaration.name
        if isinstance(declaration, (PortDeclaration, FunctionDeclaration))
        else declaration.element_declaration.name
    )


def _get_base_declaration(
    operand_declaration: OperandDeclaration,
) -> FunctionDeclaration:
    return (
        operand_declaration.element_declaration
        if isinstance(operand_declaration, FunctionDeclarationList)
        else operand_declaration
    )


FunctionDeclarationList.update_forward_refs()
