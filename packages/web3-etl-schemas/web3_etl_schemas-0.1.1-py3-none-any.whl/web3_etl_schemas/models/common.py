class HexToInt(int):
    """Convert hex string to int."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return int(v, 16) if isinstance(v, str) else v
