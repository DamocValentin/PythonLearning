# Write a programme, in which you have a set of medicin
# and you can but dfferent quantities of them.


medicines = ['Zolid', 'Insulin', 'Neem', 'Panadol', 'Ponston', 'Pentral_gold', 'Methacbar', 'Neodiapar', 'Calpol', 'Glucophage']
medicines_prices = [20, 200, 20, 20, 30, 200, 30, 70, 70, 100]


def print_medicine():
    for i in range(0, 10):
        print(f'{i+1}. {medicines[i]} for {medicines_prices[i]}$')


def __main__():

    print('Hello Customer!')
    bill = 0

    while True:
        print('We have the following medicine')
        print_medicine()
        command = input("Do you need anything?(y/n)")
        if command == 'y':
            medicine = int(input("What medicine do you need?(1-10)"))
            quantity = int(input("How much?"))
            bill = bill + medicines_prices[medicine] * quantity
        elif command == 'n':
            break
        else:
            print('Wrong command')
            continue
    print
    print(f'You have to pay: {bill}$')


__main__()