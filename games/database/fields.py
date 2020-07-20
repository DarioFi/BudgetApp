from django.db import models


class CardStack:  # custom field implemented in db as CHAR FIELD in order to have useful methods
    data = ""

    # both init and push can handle List of strings and a single string, with length validation
    def __init__(self, cards):
        if isinstance(cards, list):
            for j in cards:
                if len(j) != 2:
                    raise Exception("Validation error in push, length of objects is not 2")
            self.data = "".join(cards)
        else:
            if len(cards) % 2 != 0:
                raise Exception("Validation error in push, length of serialized string is not multiple of 2")
            self.data = cards

    def pop(self, num=1, delete=True) -> str:
        r = self.data[-2 * num:]
        if delete:
            self.data = self.data[:-2 * num]
        return r

    def push(self, value):
        if isinstance(value, list):
            for j in value:
                if len(j) != 2:
                    raise Exception("Validation error in push, length of objects is not 2")
                self.data += j
        else:
            if len(value) != 2:
                raise Exception("Validation error in push, length of object is not 2")
            self.data += value

    @property
    def all(self) -> list:
        return [self.data[x:x + 2] for x in range(0, len(self.data) - 1, 2)]

    def number_of_cards(self):
        return len(self.data) // 2

    def __str__(self):
        return str(self.all)

    def __repr__(self):
        return str(self.all)

    def __iter__(self):
        return iter(self.all)


class CardStackField(models.CharField):
    description = "A hand of cards, with some useful pop push and data validation"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        super(CardStackField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, CardStack):
            return value
        if value is None:
            return value
        return CardStack(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return CardStack(value)

    def get_prep_value(self, value: CardStack):
        return value.data
