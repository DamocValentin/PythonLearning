# Create a random list of numbers between 0 and 100.
# Ask the user for a number between 0 and 100 to check whether their number is in the list.
# The programme should work like this. The programme will half the list of numbers and see whether
# the users number matches the middle element in the list. If they do not match, the programme
# will check which half the number lies in, and eliminate the other half. The search then continues
# on the remaining half, again checking whether the middle element in that half is equal to the
# user’s number. This process keeps on going until the programme finds the users number, or until
# the size of the subarray is 0, which means the users number isn't in the list


def __main__():
    found = 0
    numbers_list = []
    for i in range(0, 100):
        if i % 2 == 0:
            numbers_list.append(i)

    searched_number = int(input("What number do you want to search? "))

    left_head = 0
    right_head = len(numbers_list) - 1
    while left_head <= right_head:
        middle = int((left_head + right_head) / 2)
        if searched_number == numbers_list[middle]:
            print("Number found!")
            found = 1
            break
        elif searched_number > numbers_list[middle]:
            left_head = middle + 1
        else:
            right_head = middle - 1

    if not found:
        print("Number not found!")


__main__()
