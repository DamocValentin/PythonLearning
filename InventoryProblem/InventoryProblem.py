

def __main__():
    delete = str(input('Do you want to delete another item record? (yes/no) '))

    while (delete == "yes") or (delete == "y"):

        with open('inventory.txt', 'r') as f:
            initial_lines = f.readlines()

        to_delete = input('What record do you want to delete?').strip()

        with open('inventory.txt', 'w') as f:
            deleting = 0
            for line in initial_lines:
                if line.strip('\n') == to_delete:
                    deleting = 1  # started deletion part
                    counter = 0
                if deleting:
                    counter += 1
                    if counter == 10:
                        deleting = 0   # finished deletion part
                else:
                    f.write(line)
        print('\nUpdated inventory list.\n')

        delete = str(input('Do you want to delete another item record? (yes/no) '))


__main__()