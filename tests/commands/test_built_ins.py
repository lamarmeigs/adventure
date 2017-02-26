from unittest import TestCase
from unittest.mock import patch

from adventure.commands.built_ins import (
    attack, drop, examine, get, inventory, look, move, outputter, talk, wait
)
from adventure.models import (
    Direction, Exit, Game, Item, Location, Person, Player
)


class CommandTestCase(TestCase):
    def setUp(self):
        # Mock outputter methods
        self.mock_display_location = patch.object(
            outputter,
            'display_location_name'
        ).start()
        self.mock_display_text = patch.object(
            outputter,
            'display_game_text'
        ).start()
        self.mock_display_person_reaction = patch.object(
            outputter,
            'display_person_reaction'
        ).start()

        # Create empty game with a player
        self.player = Player(location=None)
        self.game = Game(
            'Command Test',
            'This is a sandbox in which to test built-in commands',
            self.player,
            locations=[]
        )

    def doCleanups(self):
        self.mock_display_location.stop()
        self.mock_display_text.stop()
        self.mock_display_person_reaction.stop()


class LookTestCase(CommandTestCase):
    def test_empty_location(self):
        empty_location = Location(
            name='empty desert',
            description='Barren wastes as far as the eye can see'
        )
        self.player.location = empty_location
        look(self.game)
        self.mock_display_location.assert_called_once_with(empty_location.name)
        self.mock_display_text.assert_called_once_with(
            empty_location.description
        )

    def test_location_with_items(self):
        item = Item('rock', 'a')
        item_location = Location(
            name='almost-empty basement',
            description='This is a big room with little in it.',
            items=[item]
        )
        self.player.location = item_location
        look(self.game)
        self.mock_display_location.assert_called_once_with(item_location.name)
        self.mock_display_text.assert_any_call(item_location.description)
        self.mock_display_text.assert_any_call('You see a rock.')

    def test_location_with_person(self):
        person_1 = Person('Hamlet', '', None)
        person_location = Location(
            name='Elsinore',
            description='A drafty Danish castle.',
            people=[person_1]
        )
        self.player.location = person_location
        look(self.game)
        self.mock_display_location.assert_called_once_with(
            person_location.name
        )
        self.mock_display_text.assert_any_call(person_location.description)
        self.mock_display_text.assert_any_call('Hamlet is here.')

    def test_location_with_people(self):
        person_1 = Person('Macbeth', '', None)
        person_2 = Person('Lady Macbeth', '', None)
        people_location = Location(
            name='Inverness',
            description='A drafty Scottish castle',
            people=[person_1, person_2]
        )
        self.player.location = people_location
        look(self.game)
        self.mock_display_location.assert_called_once_with(
            people_location.name
        )
        self.mock_display_text.assert_any_call(people_location.description)
        self.mock_display_text.assert_any_call(
            'Macbeth and Lady Macbeth are here.'
        )


class ExamineTestCase(CommandTestCase):
    def test_describe_object(self):
        item = Item('thing', "Mostly amorphous and conceptual")
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=item
        ):
            examine(item.name, self.game)
        self.mock_display_text.assert_called_once_with(item.description)

    def test_nothing_to_examine(self):
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=None
        ):
            examine('not a thing', self.game)
        self.mock_display_text.assert_called_once_with(
            "You don't see anything like that here."
        )


class MoveTestCase(CommandTestCase):
    def setUp(self):
        super().setUp()
        self.direction = Direction('north', 'n')
        self.destination = Location('destination', '')
        self.exit = Exit(self.direction, self.destination)
        self.player.location = Location('source', '')

    def test_update_location_by_direction_name(self):
        self.player.location.exits = [self.exit]
        move(self.direction.name, self.game)
        self.assertEqual(self.player.location, self.destination)

    def test_update_location_by_direction_abbrev(self):
        self.player.location.exits = [self.exit]
        move(self.direction.abbrev, self.game)
        self.assertEqual(self.player.location, self.destination)

    def test_update_location_and_look(self):
        self.player.location.exits = [self.exit]
        with patch('adventure.commands.built_ins.look') as mock_look:
            move(self.direction.name, self.game)
        mock_look.assert_called_once_with(self.game)

    def test_no_exit(self):
        self.assertEqual(self.player.location.exits, [])
        move(self.direction.name, self.game)
        self.mock_display_text.assert_called_once_with(
            "You can't go that way."
        )

    def test_ignore_second_exit(self):
        other_direction = Direction('south', 's')
        other_destination = Location('other location', '')
        other_exit = Exit(other_direction, other_destination)
        self.player.location.exits = [other_exit, self.exit]

        move(self.direction.name, self.game)
        self.assertNotEqual(self.player.location, other_destination)
        self.assertEqual(self.player.location, self.destination)


class TalkTestCase(CommandTestCase):
    def setUp(self):
        super().setUp()
        self.location = Location('Empty Room', '')
        self.player.location = self.location

    def test_missing_person(self):
        person = Person('Killroy', '', None)
        talk(person.name, self.game)
        self.mock_display_text.assert_called_once_with(
            "You don't see Killroy here."
        )

    def test_talk_to_person(self):
        person = Person('Tonto', '', None)
        self.location.people = [person]
        talk(person.name, self.game)
        self.mock_display_person_reaction.assert_called_once_with(
            person.name,
            person.talk()
        )


class InventoryTestCase(CommandTestCase):
    def test_empty_inventory(self):
        self.player.inventory = []
        inventory(self.game)
        self.mock_display_text.assert_called_once_with(
            "You aren't carrying anything."
        )

    def test_inventory_items(self):
        item_1 = Item('thing')
        item_2 = Item('other thing')
        item_3 = Item('third thing')
        self.player.inventory = [item_1, item_2, item_3]
        inventory(self.game)
        self.mock_display_text.assert_called_once_with(
            'You are carrying {}, {}, and {}.'.format(
                item_1.full_name,
                item_2.full_name,
                item_3.full_name
            )
        )


class GetTestCase(CommandTestCase):
    def setUp(self):
        super().setUp()
        self.item = Item('thing')
        self.location = Location('Crossroads', 'Dull and dreary')
        self.player.location = self.location

    def test_get_location_item(self):
        self.location.items = [self.item]
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=self.item
        ):
            get(self.item.name, self.game)
        self.assertIn(self.item, self.player.inventory)
        self.assertNotIn(self.item, self.location.items)
        self.mock_display_text.assert_called_once_with(
            'You pick up the thing.'
        )

    def test_get_location_person(self):
        person = Person('Alice', '', None)
        self.location.people = [person]
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=person
        ):
            get(person.name, self.game)
        self.assertNotIn(person, self.player.inventory)
        self.assertIn(person, self.location.people)
        self.mock_display_text.assert_called_once_with('Alice ignores you.')

    def test_get_inventory_item(self):
        self.player.inventory = [self.item]
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=self.item
        ):
            get(self.item.name, self.game)
        self.assertIn(self.item, self.player.inventory)
        self.assertNotIn(self.item, self.location.items)
        self.mock_display_text.assert_called_once_with(
            'You already have the thing.'
        )

    def test_get_nothing(self):
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=None
        ):
            get('unobtainium', self.game)
        self.mock_display_text.assert_called_once_with(
            "You don't see an unobtainium here."
        )


class DropTestCase(CommandTestCase):
    def setUp(self):
        super().setUp()
        self.item = Item('thing')
        self.location = Location('Crossroads', 'Dull and dreary')
        self.player.location = self.location

    def test_drop_inventory_item(self):
        self.player.inventory = [self.item]
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=self.item
        ):
            drop(self.item.name, self.game)
        self.assertNotIn(self.item, self.player.inventory)
        self.assertIn(self.item, self.location.items)
        self.mock_display_text.assert_called_once_with('You drop the thing.')

    def test_drop_location_item(self):
        self.location.items = [self.item]
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=self.item
        ):
            drop(self.item.name, self.game)
        self.assertNotIn(self.item, self.player.inventory)
        self.assertIn(self.item, self.location.items)
        self.mock_display_text.assert_called_once_with(
            "You don't have the thing."
        )

    def test_drop_location_person(self):
        person = Person('Bob', '', None)
        self.location.people = [person]
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=person
        ):
            drop(person.name, self.game)
        self.assertNotIn(person, self.player.inventory)
        self.assertIn(person, self.location.people)
        self.mock_display_text.assert_called_once_with('Bob ignores you.')

    def test_drop_nothing(self):
        with patch.object(
            self.player,
            'find_visible_object',
            return_value=None
        ):
            drop('unobtanium', self.game)
        self.mock_display_text.assert_called_once_with(
            "You don't see an unobtanium here."
        )


class WaitTestCase(CommandTestCase):
    def test_wait(self):
        wait(self.game)
        self.mock_display_text.assert_called_once_with(
            'You doze off for a while. Nothing happens.'
        )


class AttackTestCase(CommandTestCase):
    def setUp(self):
        super().setUp()
        self.location = Location('Empty Room', '')
        self.player.location = self.location

    def test_person(self):
        person = Person('Muhammad Ali', '', None)
        self.location.people = [person]
        attack(person.name, self.game)
        self.mock_display_text.assert_called_once_with(
            'You take a swing, but Muhammad Ali ducks it.'
        )

    def test_item(self):
        item = Item('thing', '')
        self.location.items = [item]
        attack(item.name, self.game)
        self.mock_display_text.assert_called_once_with(
            'Why? What has it ever done to you?'
        )

    def test_nothing(self):
        attack('invisible object', self.game)
        self.mock_display_text.assert_called_once_with(
            "You don't see an invisible object here."
        )
