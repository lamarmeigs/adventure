from unittest import TestCase

from adventure.commands.registry import command, CommandRegistry, registry


class CommandRegistryTestCase(TestCase):
    def test_commands(self):
        test_registry = CommandRegistry()
        test_registry.update({
            'run': lambda x: x,
            'jump': lambda x: x,
            'dance': lambda x: x,
        })
        self.assertEqual(len(test_registry.commands), 3)
        self.assertIn('run', test_registry.commands)
        self.assertIn('jump', test_registry.commands)
        self.assertIn('dance', test_registry.commands)

    def test_add_command(self):
        test_registry = CommandRegistry()
        self.assertEqual(test_registry, {})
        sleep_fn = lambda x: 'zzz'
        test_registry.add_command('sleep', sleep_fn)
        self.assertEqual(test_registry, {'sleep': sleep_fn})


class RegistryInstanceTestCase(TestCase):
    def test_registry_type(self):
        self.assertIsInstance(registry, CommandRegistry)


class CommandDecoratorTestCase(TestCase):
    def test_decorated_function_added_to_registry(self):
        command_verb = lambda x: x
        talk = command('talk')(command_verb)
        self.assertIn('talk', registry.commands)
        self.assertEqual(registry['talk'], command_verb)
        self.assertEqual(command_verb('foo'), talk('foo'))
