# General Error

class MoriError(Exception):
    """Base class for errors raised by Mori."""

    def __init__(
        self,
        *message
    ):
        """Set the error message."""
        super().__init__(" ".join(message))
        self.message = " ".join(message)

    def __str__(self):
        """Return the message."""
        return repr(self.message)


# General Warning
class MoriWarning(Warning):
    """Base class for warning raised by Mori."""

    def __init__(
        self,
        *message
    ):
        """Set the error message."""
        super().__init__(" ".join(message))
        self.message = " ".join(message)

    def __str__(self):
        """Return the message."""
        return repr(self.message)
