"""scouts_auth.inuits.filters.helpers."""
def parse_choice_to_tuple(choice) -> tuple:
    return (choice.value, choice.label)
