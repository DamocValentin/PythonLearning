# Make a rock-paper-scissors game where it is the player vs the computer.
# The computer’s answer will be randomly generated, while the program
# will ask the user for their input.
import random


def __main__():

    possible_moves_list = ["rock", "paper", "scissors"]
    while True:

        player_move = input("What's your move? : ")
        if player_move not in possible_moves_list:
            print("Invalid command")
            continue

        computer_move = random.randint(0, 2)

        if player_move == "rock":
            if computer_move == 1:
                print("Computer won!")
                break
            elif computer_move == 2:
                print("You won!")
                break
            else:
                print("It's a tie!")
        elif player_move == "paper":
            if computer_move == 3:
                print("Computer won!")
                break
            elif computer_move == 0:
                print("You won!")
                break
            else:
                print("It's a tie!")
        else:
            if computer_move == 0:
                print("Computer won!")
                break
            elif computer_move == 1:
                print("You won!")
                break
            else:
                print("It's a tie!")


__main__()
