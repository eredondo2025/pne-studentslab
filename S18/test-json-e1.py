import json
import termcolor
from pathlib import Path

# 1. Read the JSON file
json_path = Path("people-e1.json")
jsonstring = json_path.read_text()

# 2. Load the data. Now 'people' is a LIST of dictionaries.
people = json.loads(jsonstring)

# 3. Print the total number of people
print(f"Total people in the database:  {len(people)}")

# 4. Iterate over each person in the list
for person in people:
    print()  # Blank line between people

    # Print Firstname and Lastname
    termcolor.cprint("Name: ", 'green', end="")
    print(f"{person['Firstname']} {person['Lastname']}")

    # Print Age
    termcolor.cprint("Age: ", 'green', end="")
    print(person['age'])

    # Get the phone numbers list
    phoneNumbers = person['phoneNumber']

    # Print the count of phone numbers
    termcolor.cprint("Phone numbers: ", 'green', end='')
    print(len(phoneNumbers))

    # Iterate over the phone numbers for this person
    for i, dictnum in enumerate(phoneNumbers):
        # The index starts at 0 as requested in the exercise (Phone 0, Phone 1...)
        termcolor.cprint(f"  Phone {i}:", 'blue')

        # Print Type and Number with indentation
        termcolor.cprint("    Type: ", 'red', end='')
        print(dictnum['type'])
        termcolor.cprint("    Number: ", 'red', end='')
        print(dictnum['number'])
