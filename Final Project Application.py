import csv
from friend import Person
from birthday import Birthday


def load_friends_from_csv(filename="database.csv"):
    friends = [] # We'll start by storing each friend as a Person object in this list 
    try:
        with open(filename, newline='') as file:
            reader = csv.DictReader(file) # This turns each row into a dictionary with column names as keys
            for row in reader: # Make a new person using their first and last name
                p = Person(row['first_name'], row['last_name']) # Make a new person using their first and last name
                if row['birthday_month'] and row['birthday_day']: # If birthday info exists then we set the birthday
                    p.set_birthday(int(row['birthday_month']), int(row['birthday_day']))
                p.email_address = row['email_address']
                p.nickname = row['nickname']
                p.street_address = row['street_address']
                p.set_city(row['city'])
                p.state = row['state']
                p.zip = row['zip']
                p.phone = row['phone']
                friends.append(p)
    except FileNotFoundError: # If the file doesn't exist, then we start again fresh
        print(f"{filename} not found. Starting with an empty list.")
    return friends


def save_friends_to_csv(friends, filename="friends_database.csv"): # This saves your current list of friends back to the CSV file
    with open(filename, 'w', newline='') as file:
        fieldnames = ['first_name', 'last_name', 'birthday_month', 'birthday_day', 'email_address',
                      'nickname', 'street_address', 'city', 'state', 'zip', 'phone']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for f in friends: # Here we save each friend's data into a new row
            writer.writerow({
                'first_name': f.first_name,
                'last_name': f.last_name,
                'birthday_month': f.birthday.get_month() if f.birthday else "",
                'birthday_day': f.birthday.get_day() if f.birthday else "",
                'email_address': f.email_address,
                'nickname': f.nickname,
                'street_address': f.street_address,
                'city': f.city,
                'state': f.state,
                'zip': f.zip,
                'phone': f.phone
            })


def create_new_friend(): # This function lets you add a new friend manually by typing in their info
    first = input("First name: ")
    last = input("Last name: ")
    friend = Person(first, last) # Now we create the Person object

    try: # Try to set their birthday, but we skip this if the input is invalid
        month = int(input("Birthday month (1-12): "))
        day = int(input("Birthday day (1-31): "))
        friend.set_birthday(month, day)
    except ValueError:
        print("Invalid birthday. Skipping.")

    friend.email_address = input("Email: ") # Ask for all the other details and store them in the object
    friend.nickname = input("Nickname: ")
    friend.street_address = input("Street address: ")
    friend.set_city(input("City: "))
    friend.state = input("State: ")
    friend.zip = input("ZIP: ")
    friend.phone = input("Phone: ")

    return friend


def search_friend(friends): # This function lets you search for a friend by name and either update or delete them
    name = input("Enter first or last name to search: ").lower()
    matches = [f for f in friends if name in f.first_name.lower() or name in f.last_name.lower()] # Find all people whose first or last name contains the search text
    if not matches:
        print("No match found.")
        return

    for i, match in enumerate(matches): # Show the matches to the user with numbers
        print(f"{i + 1}. {match.first_name} {match.last_name}")

    choice = input("Select a number to edit/delete or press Enter to cancel: ") # Ask which one to edit or delete
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(matches):
            action = input("Type 'edit' to update or 'delete' to remove: ").lower()
            if action == "edit":
                updated = create_new_friend()
                friends[friends.index(matches[index])] = updated
            elif action == "delete":
                confirm = input("Are you sure? Type YES to confirm: ")
                if confirm.upper() == "YES":
                    friends.remove(matches[index])
                    print("Deleted.")
                else:
                    print("Canceled.")
            else:
                print("Invalid option.")


def report_menu(friends): # This menu shows us the different ways there is to view the friends list
    while True:
        print("\nReport Menu:")
        print("3.1 - List of friends alphabetically")
        print("3.2 - List of friends by upcoming birthdays")
        print("3.3 - Mailing labels")
        print("3.9 - Return to main menu")
        choice = input("Choose an option: ")

        if choice == "3.1": # Sort alphabetically by last name and then first name
            sorted_list = sorted(friends, key=lambda x: (x.last_name, x.first_name))
            for f in sorted_list:
                print(f"{f.first_name} {f.last_name}")
        elif choice == "3.2": # Show birthdays coming up soon
            with_birthdays = [f for f in friends if f.birthday]
            sorted_birthdays = sorted(with_birthdays, key=lambda f: f.birthday.days_until())
            for f in sorted_birthdays:
                print(f"{f.first_name} {f.last_name} - in {f.birthday.days_until()} days")
        elif choice == "3.3": # Print mailing label-style output for each friend
            for f in friends:
                print(f"{f.first_name} {f.last_name}")
                print(f"{f.street_address}")
                print(f"{f.city}, {f.state} {f.zip}")
                print()
        elif choice == "3.9": # Go back to the main menu
            break
        else:
            print("Invalid option.")


def main(): # This is the main function which is the core loop that keeps the app running
    friends = load_friends_from_csv()

    while True: # Show the menu over and over until the user chooses to exit
        print("\nMain Menu:")
        print("1 - Create new friend record")
        print("2 - Search for a friend")
        print("3 - Run reports")
        print("4 - Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            new_friend = create_new_friend()
            friends.append(new_friend)
        elif choice == "2":
            search_friend(friends)
        elif choice == "3":
            report_menu(friends)
        elif choice == "4": # Save everything before quitting
            save_friends_to_csv(friends)
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__": # This just tells Python to run the main if this file is executed directly
    main()

