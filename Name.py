from Field import Field


class Name(Field):

    def __init__(self, name_str: str):
        self.validate(name_str)
        super().__init__(name_str)

    def validate(self, name: str):
        if len(name) <= 2:
            raise ValueError("Name greater or equal to 2")

