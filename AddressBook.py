from datetime import datetime, timedelta

from Record import Record
from collections import UserDict


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        if self.find(record.name.value) is None:
            self.data[record.name.value] = record

    def find(self, name) -> Record:
        return self.data.get(name, None)

    def delete(self, name):
        del self.data[name]

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

    def get_upcoming_birthdays(self) -> str:
        greetings_list = []
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value
            greetings_day = datetime(birthday.year, birthday.month, birthday.day).date()

            if today > greetings_day:
                continue

            if greetings_day < birthday:
                continue
            if greetings_day - today <= timedelta(days=7):
                if greetings_day.weekday() > 4:
                    greetings_day = greetings_day + timedelta(days=7 - greetings_day.weekday())

                greetings_list.append({'name': record.name, 'congratulation_date': greetings_day.strftime("%Y.%m.%d")})

        return ('\n'.
                join(f"name: {p['name']}; Congratulation date: {p['congratulation_date']}"
                     for p in greetings_list))

