from Name import Name
from Phone import Phone
from Birthday import Birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phones = []

    def __str__(self):
        return f"""Contact name: {self.name.value}
\tphones: {'; '.join(p.value for p in self.phones)}
\tbirthday: {self.birthday.value}"""

    def add_phone_number(self, phone_number: str) -> bool:
        return self.add_phone(Phone(phone_number))

    def add_phone(self, phone: Phone) -> bool:
        if self.find_phone(phone.value) is None:
            self.phones.append(phone)
            return True
        return False

    def remove_phone(self, phone_number) -> bool:
        phone = self.find_phone(phone_number)
        if phone is not None:
            self.phones.remove(phone)
            return True
        return False

    # We want to make sure new phone number is valid and the current phone number exists.
    # Creating new Phone instance make us sure phone_number is valid (it invokes def validate under the hood)
    # Checking the result of self.remove_phone to make sure previous phone number existed.
    # It's that simple, we're not able to modify something that not even existed
    def edit_phone(self, current_phone_number: str, new_phone_number: str) -> bool:
        new_phone = Phone(new_phone_number)
        if self.remove_phone(current_phone_number):
            self.add_phone(new_phone)
            return True
        return False

    def find_phone(self, phone_number: str) -> Phone:
        found_phone = list(filter(lambda phone: (phone.value == phone_number), self.phones))
        return found_phone[0] if len(found_phone) > 0 else None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
