class AdventureException(Exception):
    """Container for all exceptions raised by this package"""
    pass


class UnknownGenderError(AdventureException):
    """Raised when an unrecognized gender is assigned to a character."""

    def __init__(self, given_gender, context=None, allowed_genders=None):
        """Create a new `UnknownGenderError` instance.

        Arguments:
            given_gender (str): the given gender string that caused this error
            context (str): an optional description where this gender was given
            allowed_genders (list): an optional list of acceptable values
        """
        message = 'Unknown gender "{gender}" found{in_context}'.format(
            gender=given_gender,
            in_context=' in {}'.format(context) if context else ''
        )
        if allowed_genders:
            message = '{msg}. Expected gender to be one of {allowed}'.format(
                msg=message,
                allowed=allowed_genders
            )
        super().__init__(message)
