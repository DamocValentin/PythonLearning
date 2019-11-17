# Write a programme where the computer randomly generates a number between 0 and 20.
# The user needs to guess what the number is. If the user guesses wrong, tell them their
# guess is either too high, or too low.

import random


def __main__():

    random_number = random.randint(0, 20)
    number_found = 0

    while not number_found:

        guessed_number = input("What's the number? : ")
        try:
            if random_number == int(guessed_number):
                number_found = 1
                print(f"You found it. the number is {random_number}")
        except ValueError:
            print("This is not a number")


__main__()
