from Field import Field
import re


class Phone(Field):

    def __init__(self, phone_number: str):
        self.validate(phone_number)
        super().__init__(phone_number)

    def validate(self, phone_number: str):
        if re.match(r"[^0-9\s\-+]", phone_number):
            raise ValueError(f"{phone_number} is not a valid phone number.")

        phone_number_stripped = re.sub('[^0-9]', '', phone_number)
        if len(phone_number_stripped) != 10:
            raise ValueError(f"{phone_number} is not a valid phone number.")
