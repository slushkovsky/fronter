import re

LOWER_AFTER_HIGHER_RE = re.compile('([a-z0-9])([A-Z])')
HIGHER_AFTER_LOWER_RE = re.compile('([^_])([A-Z][a-z]+)')

def to_snake_case(name: str) -> str:
    ''' Converts @name from CamelCase to snake_case '''

    assert isinstance(name, str)

    return re.sub(HIGHER_AFTER_LOWER_RE, r'\1_\2', 
                  re.sub(LOWER_AFTER_HIGHER_RE, r'\1_\2', name)).lower()