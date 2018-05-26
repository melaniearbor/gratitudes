"""
Interactive program to record and recall gratitude.
"""

import csv
from datetime import datetime
import random


def initiate_gratitude():
    """Create a CSV file to record gratitudes."""
    with open('user_gratitudes.csv', 'w', newline="\n") as user_gratitudes:
        csv.writer(user_gratitudes, delimiter=",")


def record_gratitude():
    """Take user input and saves to a gratitude user_gratitudes.csv."""
    affirmations = ["That's wonderful!", "Well done.", "Great progress!"]
    keep_going = True
    with open('user_gratitudes.csv', 'a', newline="\n") as user_gratitudes:
        while keep_going is True:
            new_gratitude = input("What are you grateful for? ")
            gratitude_writer = csv.writer(user_gratitudes, delimiter=",")
            time = datetime.now().date()
            gratitude_writer.writerow([new_gratitude, str(time), 'no'])
            print(random.choice(affirmations))
            go_or_stop = input("Would you like to record another? ")
            if go_or_stop.lower() in ["no", "not now"]:
                keep_going = False
                print("\nGreat job! Be sure to come back soon.\n")


def reset_read_gratitudes():
    """Resets read status when all have been read."""
    with open('user_gratitudes.csv') as user_gratitudes:
        reader = csv.reader(user_gratitudes)
        lines = [row for row in reader]
        for line in lines:
            line[2] = 'no'
    with open('user_gratitudes.csv', 'w') as user_gratitudes:
        writer = csv.writer(user_gratitudes, delimiter=",")
        for line in lines:
            writer.writerow(line)


def get_current_gratitudes():
    """Returns a list of current gratitudes."""
    with open('user_gratitudes.csv', newline="\n") as user_gratitudes:
        gratitude_reader = csv.reader(user_gratitudes, delimiter=',')
        lines = [row for row in gratitude_reader]
        unread = [
            line for line in lines
            if 'no' in line
            ]
        if not unread:
            reset_read_gratitudes()
            gratitude_reader = csv.reader(user_gratitudes, delimiter=',')
            lines = [row for row in gratitude_reader]
            unread = [
                line for line in lines
                if 'no' in line
                ]
            gratitude = random.choice(unread)
            gratitude_index = lines.index(gratitude)
            date = gratitude[1]
            return lines, gratitude, date, gratitude_index
        else:
            gratitude = random.choice(unread)
            gratitude_index = lines.index(gratitude)
            date = gratitude[1]
            return lines, gratitude, date, gratitude_index


def retrieve_gratitude():
    """Choose and print a gratitude from the gratitudes file."""
    lines, gratitude, date, gratitude_index = get_current_gratitudes()
    print(f"On {date} you were grateful for {gratitude[0]}.")
    with open('user_gratitudes.csv', 'w') as user_gratitudes:
        gratitude_writer = csv.writer(user_gratitudes, delimiter=",")
        lines[gratitude_index][2] = 'yes'
        for line in lines:
            gratitude_writer.writerow(line)


def check_for_existing_gratitudes():
    """Check to see if the user has already recorded gratitudes."""
    try:
        with open('user_gratitudes.csv'):
            return True
    except:
        return False


def ask_for_action():
    """Ask user for action and then execute the action."""
    record_words = ["record", "new", "make", "create"]
    recall_words = ["remember", "recall", "recollect", "old", "previous"]
    answered = False
    while answered is False:
        chosen_action = input("""
Would you like to record a new gratitude,
or remember an previous gratitude?
""")
        if chosen_action in record_words:
            answered = True
            record_gratitude()
        elif chosen_action in recall_words:
            answered = True
            retrieve_gratitude()
        else:
            print("I'm sorry, I don't understand.")


def greet():
    """Greet the user and prompt for desired actions."""
    if check_for_existing_gratitudes() is True:
        print("Welcome back!\n")
        ask_for_action()
    else:
        print("""

Hi! Welcome to the Gratitude Tracker and congratulations on your choice to
record more gratitude in your life.

Let's get your gratitudes going!

        """)
        record_gratitude()

greet()
