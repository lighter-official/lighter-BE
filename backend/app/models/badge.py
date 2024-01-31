from dataclasses import dataclass

@dataclass
class BadgeRes:
    @dataclass
    class Badge:
        category: str
        name: str
        type: str
        created_at: str
    badges: list[Badge]