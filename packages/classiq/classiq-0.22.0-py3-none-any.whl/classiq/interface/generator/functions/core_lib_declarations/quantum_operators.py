from classiq.interface.generator.expressions import Expression
from classiq.interface.generator.functions.classical_type import Integer
from classiq.interface.generator.functions.function_declaration import (
    FunctionDeclaration,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclaration,
    PortDeclarationDirection,
)

REPEAT_OPERATOR = FunctionDeclaration(
    name="repeat",
    param_decls={"count": Integer(), "port_size": Integer()},
    port_declarations={
        "qbv": PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="port_size"),
        )
    },
    operand_declarations={
        "iteration": FunctionDeclaration(
            name="iteration",
            param_decls={"index": Integer()},
            port_declarations={
                "qbv": PortDeclaration(
                    name="qbv",
                    direction=PortDeclarationDirection.Inout,
                    size=Expression(expr="port_size"),
                )
            },
        )
    },
)


INVERT_OPERATOR = FunctionDeclaration(
    name="invert",
    param_decls={"target_size": Integer()},
    port_declarations={
        "target": PortDeclaration(
            name="target", direction="inout", size=Expression(expr="target_size")
        ),
    },
    operand_declarations={
        "operand": FunctionDeclaration(
            name="operand",
            port_declarations={
                "target": PortDeclaration(
                    name="target",
                    direction="inout",
                    size=Expression(expr="target_size"),
                )
            },
        ),
    },
)


CONTROL_OPERATOR = FunctionDeclaration(
    name="control",
    param_decls={"ctrl_size": Integer(), "target_size": Integer()},
    port_declarations={
        "ctrl": PortDeclaration(
            name="ctrl", direction="inout", size=Expression(expr="ctrl_size")
        ),
        "target": PortDeclaration(
            name="target", direction="inout", size=Expression(expr="target_size")
        ),
    },
    operand_declarations={
        "operand": FunctionDeclaration(
            name="operand",
            port_declarations={
                "target": PortDeclaration(
                    name="target",
                    direction="inout",
                    size=Expression(expr="target_size"),
                )
            },
        )
    },
)

BUILTIN_QUANTUM_OPERATORS = {
    "repeat": REPEAT_OPERATOR,
    "invert": INVERT_OPERATOR,
    "control": CONTROL_OPERATOR,
}

FunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.update(BUILTIN_QUANTUM_OPERATORS)
