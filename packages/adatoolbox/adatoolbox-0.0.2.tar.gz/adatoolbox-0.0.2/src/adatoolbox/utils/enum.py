class StrEnum(str, Enum):
    """
    Base class of Enum whith str support
    """

    def __str__(self):
        return self.value


class EnvironmentSet(StrEnum):
    """Enum for the environment set."""

    PRODUCTION = 'production'
    DEVELOPMENT = 'development'
    STAGING = 'staging'
