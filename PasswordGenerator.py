# Write a programme, which generates a random password for the user.
# Ask the user how long they want their password to be,
# and how many letters and numbers they want in their password.
# Have a mix of upper and lowercase letters, as well as numbers and symbols.
# The password should be a minimum of 6 characters long.
import random
import string


def __main__():

    while True:
        password_length = int(input("How many characters do you want in your password? "))
        if password_length >= 6:
            break
        print("Too short")

    characters = string.ascii_letters + string.digits + string.punctuation
    print(''.join(random.choice(characters) for i in range(password_length)))


__main__()
