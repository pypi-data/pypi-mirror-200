from typing import Dict

from classiq.interface.generator.expressions import Expression
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)


class SlicedWire(HashablePydanticBaseModel):
    name: str
    start: Expression
    end: Expression

    def substitute(self, substitutions: Dict[str, Expression]) -> "SlicedWire":
        return self.copy(
            update={
                "start": self.start.substitute(substitutions),
                "end": self.end.substitute(substitutions),
            }
        )

    def add_prefix(self, prefix: str) -> "SlicedWire":
        return self.copy(update={"name": prefix + self.name})

    class Config:
        frozen = True
