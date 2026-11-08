from functools import wraps


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.lower(), *args


def normalize_name(name: str) -> str:
    return name.capitalize()


@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[normalize_name(name)] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    name = normalize_name(name)
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    name = normalize_name(args[0])
    return contacts[name]


@input_error
def show_all(args, contacts):
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


COMMANDS = {
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
}


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command in COMMANDS:
            print(COMMANDS[command](args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()