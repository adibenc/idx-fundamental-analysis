from dataclasses import asdict

from attr import dataclass


@dataclass
class BaseDataClass:
    def to_dict(self):
        return asdict(self)
