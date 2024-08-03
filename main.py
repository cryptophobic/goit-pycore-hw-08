import argparse
import sys
from colorama import Fore

from AddressBook import AddressBook
from Record import Record
import config
import pickle


def input_error(func):
    def inner(*input_args, **kwargs):
        try:
            return func(*input_args, **kwargs)
        except (KeyError, ValueError, IndexError) as err:
            return str(err)

    return inner


@input_error
def parse_input(user_input):
    cmd, *input_args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *input_args


@input_error
def add_contact_details(input_args: list, book: AddressBook) -> str:
    name, phone_number = input_args
    record = book.find(name)
    if record is not None:
        record.add_phone_number(phone_number)
    else:
        record = Record(name)
        record.add_phone_number(phone_number)
        book.add_record(record)

    return "Contact added."


@input_error
def add_birthday(input_args: list, book: AddressBook) -> str:
    name, birthday = input_args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_birthday(birthday)

    return "Birthday added."


@input_error
def change_contact(input_args: list, book: AddressBook) -> str:
    name, old_phone, new_phone = input_args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def phone_contact(input_args: list, book: AddressBook) -> str:
    [name] = input_args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    return '; '.join(p.value for p in record.phones)


def load_data() -> AddressBook:
    try:
        with open(config.ADDRESS_BOOK_STATE_FILEPATH, "rb") as fh:
            return pickle.load(fh)
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {config.ADDRESS_BOOK_STATE_FILEPATH} .\n")
    except PermissionError:
        sys.stderr.write(f"Permission denied. File {config.ADDRESS_BOOK_STATE_FILEPATH} .\n")
    except pickle.UnpicklingError:
        sys.stderr.write(f"File corrupted: File {config.ADDRESS_BOOK_STATE_FILEPATH}: .\n")
    finally:
        return AddressBook()


def save_data(book: AddressBook):
    try:
        with open(config.ADDRESS_BOOK_STATE_FILEPATH, "wb") as fh:
            pickle.dump(book, fh)
    except PermissionError:
        sys.stderr.write(f"Permission denied. File {config.ADDRESS_BOOK_STATE_FILEPATH}\n")


def main(verbose=False):
    print("Welcome to the assistant bot!")
    book = load_data()

    close = False
    while not close:
        user_input = input(f"{Fore.GREEN}Enter a command: {Fore.RESET}")
        command, *input_args = parse_input(user_input)

        if verbose is True:
            print(command, *input_args)

        match command:
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact_details(input_args, book))
            case "change":
                print(change_contact(input_args, book))
            case "phone":
                print(phone_contact(input_args, book))
            case "birthday":
                print(add_birthday(input_args, book))
            case "greetings":
                print(book.get_upcoming_birthdays())
            case "all":
                print(book)
            case _ if command in ["close", "exit"]:
                close = True
            case _:
                sys.stderr.write("Invalid command.\n"
                                 "Available commands are: close, exit, hello, add, change, phone, all\n")

    print("Good bye!")
    save_data(book)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        help="Add extra debugging info",
        action="store_true")
    args = parser.parse_args()
    main(**vars(args))
