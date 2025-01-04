from datetime import datetime, timedelta, date

from address_book import AddressBook
from record import Record
from fields import DATE_FORMAT

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me the command and arguments."
        except KeyError:
            return "This contact does not exist."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return inner


def parse_input(user_input: str):
    """Parse user input into command and arguments."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide both name and phone.")
    name, phone, *_ = args
    record = book.find(name)
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        return f"Contact {name} added with phone {phone}."
    else:
        record.add_phone(phone)
        return f"Phone {phone} added to existing contact {name}."


@input_error
def change_contact(args, book: AddressBook):
    """Change an existing contact's phone number."""
    name, old_phone, new_phone = args

    if len(args) != 3:
        raise ValueError('To change contact specify: <name>, <old_phone>, <new_phone>')

    existing_contact = book.find(name)
    if not existing_contact:
        return f"Contact with name {name} does not exist."
    
    try:
        existing_contact.edit_phone(old_phone, new_phone)
        return f"Old phone {old_phone} was replaced by new phone {new_phone} for contact {name}."
    except Exception as e:
        return f"Error while changing phone: {e}"


@input_error
def show_phone(args, book: AddressBook):
    """Show a contact's phone number."""
    name, *_ = args

    if not name:
        raise ValueError('Please enter contact name')
    
    contact = book.find(name)

    if not contact:
        return f"Contact with name {name} does not exist."

    return f"Phone number for contact {name}: {contact}"


@input_error
def show_all(book: AddressBook):
    """Show all contacts."""
    if not book.data.keys():
        return "There are no contacts in the list."
    result = []

    for contact in book.data.values():
        result.append(f"{contact}")

    return "\n".join(result)


@input_error
def add_birthday(args, book: AddressBook):
    name, birthdate = args
    if not name or not birthdate:
        raise ValueError('You need to specify name and birthdate')

    existing_contact = book.find(name)
    if not existing_contact:
        return f'There is no contact with name {name}'
    
    existing_contact.add_birthday(birthdate)
    return f'birthday {birthdate} successfully added to contact {name}'


@input_error
def show_birthday(args, book):
    name, *_ = args
    if not name:
        raise ValueError('You need to specify name')

    existing_contact = book.find(name)
    if not existing_contact:
        return f'There is no contact with name {name}'
    
    birthdate = existing_contact.get_birthday()
    if not birthdate:
        return f"{name}'s birthdate is not set"

    birthdate = datetime.strftime(existing_contact.get_birthday(), DATE_FORMAT)
    return f"{name}'s birthday is {birthdate}"

@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if len(upcoming_birthdays) == 0:
        return 'No contacts with upcoming birthdays'
    
    result_strings = []
    for item in upcoming_birthdays:
        result_strings.append(f"name {item['name']}, congratulation date: {item['congratulation_date']}")
    
    return '\n'.join(result_strings)

def main():
    print("Welcome to the assistant bot!")
    book = AddressBook()

# test
    """ print('Add contact')
    args = 'Maria', '0123456789'
    print(add_contact(args, book))
    print(show_all(book))
    print()
    
    print('Update contact if there is such already')
    args = 'Maria', '0505555555', 
    print(add_contact(args, book))
    print(show_all(book))
    print()

    print('Update contact if there is such already')
    args = 'Maria', '0505555555', '1111111111'
    print(change_contact(args, book))
    print(show_all(book))
    print()

    print('Update contact if there is no such contact')
    args = 'Mari', '0505555555', '1111111111'
    print(change_contact(args, book))
    print(show_all(book))
    print()

    print('Show existing contact')
    args = 'Maria',
    print(show_phone(args, book))
    print(show_all(book))
    print()

    print('Show non existing contact')
    args = 'Mari',
    print(show_phone(args, book))
    print(show_all(book))
    print()

    print('Add birthdate to existing contact')
    args = 'Maria', '1985.01.04'
    print(add_birthday(args, book))
    print(show_all(book))
    print()

    print('Add birthdate to existing contact in incoorect format')
    marias_birthdate = date.today() + timedelta(days=2)
    args = 'Maria', datetime.strftime(marias_birthdate, DATE_FORMAT)
    print(add_birthday(args, book))
    print(show_all(book))
    print()

    print('Add birthdate to non existing contact')
    args = 'Mari', '1990.01.27'
    print(add_birthday(args, book))
    print(show_all(book))
    print()

    print('Show birthdate of non existing contact')
    args = 'Mari',
    print(show_birthday(args, book))
    print(show_all(book))
    print()

    print('Show birthdate of it is not set for the contact')
    args = 'Anton', '0505555555'
    print(add_contact(args, book))
    args = 'Anton',
    print(show_birthday(args, book))
    print(show_all(book))
    print()
    
    print('Show future birthdays')
    print(birthdays(book)) """


    while True:
        user_input = input("Enter command: ").strip()
        if not user_input:
            continue  

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(add_contact(args,  book))
        elif command == 'change':
            print(change_contact(args,  book))
        elif command == 'phone':
            print(show_phone(args,  book))
        elif command == 'all':
            print(show_all( book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()