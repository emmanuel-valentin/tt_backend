from enum import Enum


class Role(Enum):
    PATIENT = "patient"
    PHYSIOTHERAPIST = "physiotherapist"
    
    @classmethod
    def choices(cls):
        return [(role.value, role.name) for role in cls]
    
    def __str__(self):
        return self.value
    
    def to_json(self):
        return self.value
    
    @classmethod
    def from_json(cls, value):
        for role in cls:
            if role.value == value:
                return role
        raise ValueError(f"'{value}' is not a valid {cls.__name__}")
