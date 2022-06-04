from dataclasses import dataclass, InitVar, field
from enum import Enum
from hashlib import sha3_256

def hash_password(password):
    encoded = password.encode()
    hashed = sha3_256(encoded)
    return hashed.hexdigest()


def check_password(hash, password):
    hashed_password = hash_password(password)
    return hash == hashed_password


class RoleEnum(Enum):
    ADMINISTRATOR = 1
    SECRETARY = 2
    MANAGER = 3


# custom user model for in-memory storage
@dataclass
class User:
    username: str
    password: InitVar[str]
    password_hash: str = field(init=False)
    role: "RoleEnum"

    def __post_init__(self, password):
        self.password_hash = hash_password(password)

    def __repr__(self):
        return f"({self.username}, {self.role.name})"


