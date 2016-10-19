class CommandRegistry(dict):
    """Registry to pair player commands with functions to handle those commands

    Note that any function should accept, at minimum a `game` kwarg, which will
    contain the instance of the Game being run. All other arguments passed in
    will be user input.
    """
    @property
    def commands(self):
        """Return a list of registered commands"""
        return list(self.keys())

    def add_command(self, command, function):
        """Add command verb / function pair to registry.

        Args:
            command (str): a single-word command (a verb, eg. move, get, talk)
            function (callable): a standalone function
        """
        self[command] = function


# Instantiate the CommandRegistry "singleton" to use throughout the package
registry = CommandRegistry()


def command(verb):
    """Decorator that registers a function to handle a given command verb

    Args:
        verb (str): a single-word command (a verb, eg. wait, drop, attack)
    """
    def _wrapped_function(command_function):
        registry.add_command(verb, command_function)

        def _run_command(*args, **kwargs):
            return command_function(*args, **kwargs)

        return _run_command
    return _wrapped_function
