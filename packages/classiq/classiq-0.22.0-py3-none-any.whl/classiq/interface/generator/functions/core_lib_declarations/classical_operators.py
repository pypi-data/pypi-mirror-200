from classiq.interface.generator.functions.classical_type import Integer
from classiq.interface.generator.functions.function_declaration import (
    FunctionDeclaration,
)

CLASSICAL_REPEAT_OPERATOR = FunctionDeclaration(
    name="classical_repeat",
    param_decls={"count": Integer()},
    operand_declarations={
        "iteration": FunctionDeclaration(
            name="iteration",
        )
    },
)

FunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.update(
    {
        "classical_repeat": CLASSICAL_REPEAT_OPERATOR,
    }
)
