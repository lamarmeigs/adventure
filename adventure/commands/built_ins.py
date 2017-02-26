from adventure.commands.registry import command
from adventure.display import outputter
from adventure.display.helpers import concatenate_items, guess_article
from adventure.models import Item, Person


@command('look')
def look(game):
    """Describe the player's current location."""
    location = game.player.location
    outputter.display_location_name(location.name)
    outputter.display_game_text(location.description)

    if location.items:
        item_names = [item.full_name for item in location.items]
        item_text = 'You see {}.'.format(concatenate_items(item_names))
        outputter.display_game_text(item_text)
    if location.people:
        people_names = [person.name for person in location.people]
        people_text = '{people} {verb} here.'.format(
            people=concatenate_items(people_names),
            verb='is' if len(location.people) == 1 else 'are'
        )
        outputter.display_game_text(people_text)


@command('examine')
def examine(target_name, game):
    """Describe a particular item or person in detail."""
    obj = game.player.find_visible_object(target_name)
    if obj:
        outputter.display_game_text(obj.description)
    else:
        outputter.display_game_text("You don't see anything like that here.")


@command('move')
def move(direction, game):
    """Move the player in the specified direction."""
    destination = None
    for exit in game.player.location.exits:
        if direction in (exit.direction.name, exit.direction.abbrev):
            destination = exit.destination

    if destination:
        game.player.location = destination
        look(game)
    else:
        outputter.display_game_text("You can't go that way.")


@command('talk')
def talk(person_name, game):
    """Start a conversation with another person."""
    person = game.player.find_visible_object(person_name)
    if person:
        outputter.display_person_reaction(person.name, person.talk())
    else:
        outputter.display_game_text(
            "You don't see {} here.".format(person_name)
        )


@command('inventory')
def inventory(game):
    """List the items in the player's inventory."""
    inventory = game.player.inventory
    if not len(inventory):
        outputter.display_game_text("You aren't carrying anything.")
    else:
        item_names = [item.full_name for item in inventory]
        items_list = concatenate_items(item_names)
        outputter.display_game_text('You are carrying {}.'.format(items_list))


@command('get')
def get(item_name, game):
    """Move an item from the player's current location to their inventory."""
    item = game.player.find_visible_object(item_name)
    if item in game.player.location.items:
        game.player.location.items.remove(item)
        game.player.inventory.append(item)
        outputter.display_game_text('You pick up the {}.'.format(item.name))
    elif item in game.player.location.people:
        outputter.display_game_text("{} ignores you.".format(item.name))
    elif item in game.player.inventory:
        outputter.display_game_text(
            'You already have the {}.'.format(item.name)
        )
    else:
        outputter.display_game_text(
            "You don't see {article} {name} here.".format(
                article=guess_article(item_name),
                name=item_name
            )
        )


@command('drop')
@command('discard')
@command('throw')
@command('leave')
def drop(item_name, game):
    """Move an item from the player's inventory to the current location."""
    item = game.player.find_visible_object(item_name)
    if item in game.player.inventory:
        game.player.location.items.append(item)
        game.player.inventory.remove(item)
        outputter.display_game_text('You drop the {}.'.format(item.name))
    elif item in game.player.location.items:
        outputter.display_game_text("You don't have the {}.".format(item.name))
    elif item in game.player.location.people:
        outputter.display_game_text('{} ignores you.'.format(item.name))
    else:
        outputter.display_game_text(
            "You don't see {article} {name} here.".format(
                article=guess_article(item_name),
                name=item_name
            )
        )


@command('sleep')
@command('wait')
def wait(game):
    """Do nothing."""
    outputter.display_game_text('You doze off for a while. Nothing happens.')


@command('kill')
@command('punch')
@command('kick')
@command('hit')
@command('attack')
def attack(target_name, game):
    """Attack another person or object."""
    target = game.player.find_visible_object(target_name)
    if isinstance(target, Person):
        outputter.display_game_text(
            'You take a swing, but {} ducks it.'.format(target.name)
        )
    elif isinstance(target, Item):
        outputter.display_game_text('Why? What has it ever done to you?')
    else:
        outputter.display_game_text(
            "You don't see {article} {name} here.".format(
                article=guess_article(target_name),
                name=target_name
            )
        )
