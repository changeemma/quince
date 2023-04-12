from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Contact:
    name: str
    phone: str = field(compare=False)
