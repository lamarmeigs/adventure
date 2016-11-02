def concatenate_items(items, conjunction='and'):
    """Format a human-readable description of an iterable.

    Arguments:
        items (iterable): list of items to format
        conjunction (str): a conjunction for use in combining items

    Return:
        A text description of items, with appropriate comma and conjunctions
    """
    text = ''
    if not items:
        text = ''
    elif len(items) == 1:
        text = items[0]
    elif len(items) == 2:
        text = '{} {} {}'.format(items[0], conjunction, items[1])
    else:
        text = ', '.join(items[:-1])
        text += ', {} {}'.format(conjunction, items[-1])
    return text
