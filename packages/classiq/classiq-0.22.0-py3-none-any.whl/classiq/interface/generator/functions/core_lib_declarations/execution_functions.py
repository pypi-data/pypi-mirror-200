from classiq.interface.generator.functions.classical_type import Integer
from classiq.interface.generator.functions.function_declaration import (
    FunctionDeclaration,
)

SAMPLE_OPERATOR = FunctionDeclaration(
    name="sample",
    param_decls={"num_shots": Integer()},
    operand_declarations={
        "qfunc_call": FunctionDeclaration(
            name="qfunc_call",
        )
    },
)

FunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.update(
    {
        "sample": SAMPLE_OPERATOR,
    }
)
