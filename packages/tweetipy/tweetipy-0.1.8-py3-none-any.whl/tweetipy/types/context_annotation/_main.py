from ._domain import Domain
from ._entity import Entity

class ContextAnnotation():
    def __init__(self, domain: Domain, entity: Entity) -> None:
        self.domain = Domain(**domain)
        self.entity = Entity(**entity)

    def json(self):
        return {
            "domain": self.domain,
            "entity": self.entity
        }

    def __str__(self) -> str:
        return '\n'.join([
            f"Domain: {self.domain.name} / ID: {self.domain.id}",
            f"Entity: {self.entity.name} / ID: {self.entity.id}",
        ])