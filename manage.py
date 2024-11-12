import subprocess

def quit_program():
    quit()

while True:
    operation = input('1. init the project \n2. update countries\n3. update ip-country table\n4. finding the list of countries for input perfix\n0. quit\n\nSelect an operation: ')
    if operation == '1':
        # Run main.py
        subprocess.run(["python", "main_mudules/main.py"])
        print('DateBase is created successfully\n')

        # Run add_update_countries.py
        print('Adding the countries to database.')
        subprocess.run(["python3", "main_mudules/add_update_countries.py"])
        print('Done\n')

        # Run add_ip_perfix.py
        print('Adding the ip perfixes to database.')
        subprocess.run(["python3", "main_mudules/add_ip_perfix.py"])
        print('Done\n')
    elif operation == '2':
        # Run add_update_countries.py
        print('updating the country table.')
        subprocess.run(["python3", "main_mudules/add_update_countries.py"])
        print('Done\n')
    elif operation == '3':
        # Run add_update_ip_country.py
        print('updating the ip_country table.')
        subprocess.run(["python3", "main_mudules/add_update_ip_country.py"])
        print('Done\n')
    elif operation == '4':
        # Run finding_countries.py
        while True:
            subprocess.run(["python3", "main_mudules/finding_countries.py"])
            mini_operation = input('\n1. finding for a new perfix\n00. back\n\nSelect an operation: ')
            if mini_operation == '1':
                continue
            else:
                break

    else:
        quit_program()





